// Banco Provincia Fee Updater
//
// Scrapes merchant acquiring fees from Banco Provincia's official adhesion page
// and updates data.json with current rates.
//
// Source: https://www.bancoprovincia.com.ar/web/adhesion_comercios
package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/jrusco/monitor-comisiones-bancarias/internal/common"
)

const baproID = "bapro"
const primaryFeeURL = "https://www.bancoprovincia.com.ar/web/adhesion_comercios"

// Fallback rates from research_spanish.md (Table 2)
var fallbackRates = map[string]string{
	"debito":    "0.8% + IVA",
	"credito":   "1.8% + IVA",
	"clave_dni": "0.6% + IVA",
	"qr_saldo":  "0.8% + IVA",
}

type baproMapping struct {
	jsonConcept   string
	jsonTerm      string
	ratePatterns  []string
	fallbackKey   string
	expectedMin   float64
	expectedMax   float64
}

// RE2 compatible patterns (no negative lookahead)
var feeMappings = []baproMapping{
	{
		jsonConcept: "Débito", jsonTerm: "48 hs",
		ratePatterns: []string{
			`(?i)tarjetas\s+de\s+d[ée]bito[^<]*<[^>]*>\s*[^:]*fiserv[^:]*:\s*(\d+[,.]\d+)\s*%`,
			`(?i)tarjetas\s+de\s+d[ée]bito.*?fiserv[^:]*:\s*(\d+[,.]\d+)\s*%`,
			`(?i)(?:débito|debito)[:\s]+(\d+[,.]\d+)\s*%`,
			`(?i)(\d+[,.]\d+)\s*%[^.]{0,40}(?:con\s+)?(?:tarjeta\s+de\s+)?d[ée]bito`,
		},
		fallbackKey: "debito", expectedMin: 0.7, expectedMax: 1.0,
	},
	{
		jsonConcept: "Crédito", jsonTerm: "8-10 días hábiles",
		ratePatterns: []string{
			`(?i)tarjetas\s+de\s+cr[ée]dito\s+en\s+un\s+pago[^:]*:\s*(\d+[,.]\d+)\s*%`,
			`(?i)(?:crédito|credito)[:\s]+(\d+[,.]\d+)\s*%`,
			`(?i)(\d+[,.]\d+)\s*%[^.]{0,40}(?:con\s+)?(?:tarjeta\s+de\s+)?cr[ée]dito`,
		},
		fallbackKey: "credito", expectedMin: 1.7, expectedMax: 2.0,
	},
	{
		jsonConcept: "Clave DNI (Token)", jsonTerm: "Inmediato",
		ratePatterns: []string{
			`(?i)clave\s+dni\s+token[:\s]*(\d+[,.]\d+)\s*%`,
			`(?i)clave\s+(?:dni\s+)?token[:\s]*(\d+[,.]\d+)\s*%`,
			`(?i)(?:clave\s+)?dni\s+(?:token|inmediata)[^.]{0,50}(\d+[,.]\d+)\s*%`,
		},
		fallbackKey: "clave_dni", expectedMin: 0.5, expectedMax: 0.7,
	},
	{
		jsonConcept: "QR (Saldo en Cuenta)", jsonTerm: "Inmediato",
		ratePatterns: []string{
			`(?i)qr\s+a\s+trav[ée]s\s+de\s+d[ée]bito\s+en\s+cuenta[^:]*:\s*(\d+[,.]\d+)\s*%`,
			`(?i)qr[:\s]+(\d+[,.]\d+)\s*%`,
			`(?i)(?:qr|transferencia).*?saldo[^.]{0,50}(\d+[,.]\d+)\s*%`,
			`(?i)saldo\s+en\s+cuenta[^.]{0,50}(\d+[,.]\d+)\s*%`,
		},
		fallbackKey: "qr_saldo", expectedMin: 0.7, expectedMax: 0.9,
	},
}

type scrapedFee struct {
	paymentType string
	fee         string
	source      string
	pattern     int
}

func scrapeBaproFees(htmlContent string) []scrapedFee {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(htmlContent))
	if err != nil {
		return nil
	}
	text := doc.Text()

	var fees []scrapedFee

	for _, m := range feeMappings {
		found := false
		for pi, pat := range m.ratePatterns {
			re, err := regexp.Compile(pat)
			if err != nil {
				fmt.Printf("  Regex error in pattern %d: %v\n", pi+1, err)
				continue
			}
			matches := re.FindAllStringSubmatch(text, -1)
			if len(matches) == 0 {
				continue
			}

			feeText := strings.TrimSpace(matches[0][1])
			// Validate
			numStr := strings.ReplaceAll(feeText, ",", ".")
			var v float64
			fmt.Sscanf(numStr, "%f", &v)
			if v < m.expectedMin || v > m.expectedMax {
				continue
			}

			if !strings.HasSuffix(feeText, "%") {
				feeText += "%"
			}
			if !strings.Contains(feeText, "IVA") {
				feeText += " + IVA"
			}

			fees = append(fees, scrapedFee{
				paymentType: m.jsonConcept,
				fee:         feeText,
				source:      "scraped",
				pattern:     pi + 1,
			})
			fmt.Printf("  Found %s: %s (pattern %d)\n", m.jsonConcept, feeText, pi+1)
			found = true
			break
		}
		if !found {
			fmt.Printf("  Could not scrape %s fee (will use fallback)\n", m.jsonConcept)
		}
	}

	return fees
}

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("Banco Provincia Fee Updater")
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

	// Fetch page
	fmt.Printf("2. Fetching Banco Provincia fees from:\n   %s\n", primaryFeeURL)
	html, err := common.FetchPage(primaryFeeURL)
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("   Successfully fetched page")
	fmt.Println()

	// Scrape
	fmt.Println("3. Parsing fees from page...")
	scraped := scrapeBaproFees(html)
	if len(scraped) == 0 {
		fmt.Println("   No fees scraped from page (will use verified fallback rates)")
	} else {
		fmt.Printf("   Scraped %d fee entries\n", len(scraped))
	}
	fmt.Println()

	// Update
	fmt.Printf("4. Updating %s...\n", common.DataFile)
	fmt.Println(strings.Repeat("-", 70))

	entity := common.FindEntityByID(data, baproID)
	if entity == nil {
		fmt.Printf("ERROR: Entity '%s' not found in %s\n", baproID, common.DataFile)
		os.Exit(1)
	}

	updated := false
	for _, m := range feeMappings {
		var newRate, source string

		// Try scraped
		for _, sf := range scraped {
			if sf.paymentType == m.jsonConcept {
				newRate = common.NormalizeDecimalSeparator(sf.fee)
				source = "scraped"
				fmt.Printf("  Using scraped rate for '%s': %s\n", m.jsonConcept, newRate)
				break
			}
		}

		// Fallback
		if newRate == "" {
			newRate = fallbackRates[m.fallbackKey]
			source = "fallback"
			fmt.Printf("  Using verified fallback for '%s': %s\n", m.jsonConcept, newRate)
		}
		_ = source

		fee := common.FindFee(entity.Fees, m.jsonConcept, m.jsonTerm)
		if fee == nil {
			fmt.Printf("  Fee entry not found for '%s' in data.json\n", m.jsonConcept)
			continue
		}

		if common.UpdateFee(fee, newRate) {
			updated = true
		}
	}

	fmt.Println(strings.Repeat("-", 70))
	fmt.Println()

	// Update lastUpdated timestamp (even if fees unchanged - shows "last verified")
	entity.LastUpdated = time.Now().UTC().Format(time.RFC3339)
	fmt.Printf("  Updated lastUpdated timestamp: %s\n", entity.LastUpdated)

	if err := common.SaveData(data); err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	if updated {
		fmt.Printf("\n%s has been successfully updated with new fee data.\n", common.DataFile)
	} else {
		fmt.Printf("\nNo fee changes detected, but lastUpdated timestamp refreshed.\n")
	}

	fmt.Println()
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("Script finished successfully.")
}
