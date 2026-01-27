// BNA Fee Updater - Fiserv Authoritative Source
//
// Scrapes BCRA-regulated merchant acquiring fees from Fiserv Argentina
// (the infrastructure provider for BNA) and updates data.json.
//
// Source: https://aranceles.fiservargentina.com/
package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/jrusco/monitor-comisiones-bancarias/internal/common"
)

const bnaID = "bna"
const fiservFeeURL = "https://aranceles.fiservargentina.com/"

type scrapedFee struct {
	paymentType string
	fee         string
	term        string
}

type feeMapping struct {
	jsonConcept     string
	jsonTerm        string
	pagePaymentType string
	staticRate      string
}

var feeMappings = []feeMapping{
	{jsonConcept: "Débito", jsonTerm: "24 hs", pagePaymentType: "Débito"},
	{jsonConcept: "Crédito", jsonTerm: "8-10 días hábiles", pagePaymentType: "Crédito"},
	{jsonConcept: "Mantenimiento Terminal", jsonTerm: "Mensual", staticRate: "Bonificado o Variable"},
}

func scrapeFiservFees(htmlContent string) []scrapedFee {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(htmlContent))
	if err != nil {
		return nil
	}

	text := doc.Text()
	percentRe := regexp.MustCompile(`(\d+[,.]?\d*)\s*%`)
	percentMatches := percentRe.FindAllStringSubmatchIndex(text, -1)

	if len(percentMatches) == 0 {
		return nil
	}

	// Find positions of Débito and Crédito labels
	debitoRe := regexp.MustCompile(`(?i)[Dd](?:Ã©|é)bito|[Dd]ebito`)
	creditoRe := regexp.MustCompile(`(?i)[Cc](?:rÃ©|ré)dito|[Cc]redito`)

	debitoPos := debitoRe.FindStringIndex(text)
	creditoPos := creditoRe.FindStringIndex(text)

	var fees []scrapedFee

	// Find percentage closest to Débito (< 1.0%)
	if debitoPos != nil {
		bestDist := math.MaxFloat64
		bestFee := ""
		for _, m := range percentMatches {
			dist := math.Abs(float64(m[0] - debitoPos[0]))
			if dist < 300 && dist < bestDist {
				numStr := strings.ReplaceAll(text[m[2]:m[3]], ",", ".")
				var v float64
				fmt.Sscanf(numStr, "%f", &v)
				if v < 1.0 {
					bestFee = text[m[2]:m[3]]
					bestDist = dist
				}
			}
		}
		if bestFee != "" {
			fees = append(fees, scrapedFee{paymentType: "Débito", fee: bestFee + "%", term: "24 horas hábiles"})
		}
	}

	// Find percentage closest to Crédito (> 1.0%)
	if creditoPos != nil {
		bestDist := math.MaxFloat64
		bestFee := ""
		for _, m := range percentMatches {
			dist := math.Abs(float64(m[0] - creditoPos[0]))
			if dist < 300 && dist < bestDist {
				numStr := strings.ReplaceAll(text[m[2]:m[3]], ",", ".")
				var v float64
				fmt.Sscanf(numStr, "%f", &v)
				if v > 1.0 {
					bestFee = text[m[2]:m[3]]
					bestDist = dist
				}
			}
		}
		if bestFee != "" {
			fees = append(fees, scrapedFee{paymentType: "Crédito", fee: bestFee + "%", term: "8-10 días hábiles"})
		}
	}

	return fees
}

func findScrapedFeeByType(fees []scrapedFee, paymentType string) string {
	pt := strings.ToLower(paymentType)
	for _, f := range fees {
		if strings.Contains(strings.ToLower(f.paymentType), pt) {
			return common.NormalizeDecimalSeparator(f.fee + " + IVA")
		}
	}
	return ""
}

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("BNA Fee Updater (Fiserv Authoritative Source)")
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println()

	// Load data
	fmt.Printf("1. Loading %s...\n", common.DataFile)
	data, err := common.LoadData()
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("   Successfully loaded %s\n\n", common.DataFile)

	// Fetch Fiserv
	fmt.Printf("2. Fetching Fiserv fees from: %s\n", fiservFeeURL)
	html, err := common.FetchPage(fiservFeeURL)
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("   Successfully fetched Fiserv page")
	fmt.Println()

	// Parse fees
	fmt.Println("3. Parsing BCRA-regulated rates from Fiserv...")
	scraped := scrapeFiservFees(html)
	if len(scraped) == 0 {
		fmt.Println("   ERROR: Could not extract any fees from Fiserv page.")
		os.Exit(1)
	}
	fmt.Printf("   Successfully scraped %d fee entries:\n", len(scraped))
	for _, f := range scraped {
		fmt.Printf("      - %s: %s (Settlement: %s)\n", f.paymentType, f.fee, f.term)
	}
	fmt.Println()

	// Update data.json
	fmt.Printf("4. Updating %s with scraped values...\n", common.DataFile)
	fmt.Println(strings.Repeat("-", 70))

	entity := common.FindEntityByID(data, bnaID)
	if entity == nil {
		fmt.Printf("ERROR: Entity '%s' not found in %s\n", bnaID, common.DataFile)
		os.Exit(1)
	}

	updated := false
	for _, m := range feeMappings {
		var newRate string

		if m.staticRate != "" {
			newRate = m.staticRate
			fmt.Printf("  Using static rate for %s: %s\n", m.jsonConcept, newRate)
		} else {
			newRate = findScrapedFeeByType(scraped, m.pagePaymentType)
			if newRate == "" {
				fmt.Printf("  WARN: Could not find %s rate from Fiserv. Skipping.\n", m.jsonConcept)
				continue
			}

			// Validate range
			valRe := regexp.MustCompile(`(\d+\.?\d*)`)
			if vm := valRe.FindStringSubmatch(newRate); vm != nil {
				var v float64
				fmt.Sscanf(vm[1], "%f", &v)
				if m.jsonConcept == "Débito" && (v < 0.5 || v > 1.1) {
					fmt.Printf("  Warning: Débito rate %.1f%% outside expected range (0.5-1.1%%)\n", v)
				} else if m.jsonConcept == "Crédito" && (v < 1.5 || v > 2.1) {
					fmt.Printf("  Warning: Crédito rate %.1f%% outside expected range (1.5-2.1%%)\n", v)
				}
			}
		}

		fee := common.FindFee(entity.Fees, m.jsonConcept, m.jsonTerm)
		if fee == nil {
			fmt.Printf("  WARN: Fee entry not found for '%s' (%s) in data.json\n", m.jsonConcept, m.jsonTerm)
			continue
		}

		if common.UpdateFee(fee, newRate) {
			updated = true
		}
	}

	fmt.Println(strings.Repeat("-", 70))
	fmt.Println()

	if updated {
		if err := common.SaveData(data); err != nil {
			fmt.Printf("ERROR: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("%s has been successfully updated.\n", common.DataFile)
	} else {
		fmt.Printf("No fee changes detected. %s remains unchanged.\n", common.DataFile)
	}

	fmt.Println()
	fmt.Printf("5. Updating date stamp in %s...\n", common.IndexFile)
	common.UpdateDateInHTML()

	fmt.Println()
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("Script finished successfully.")
}
