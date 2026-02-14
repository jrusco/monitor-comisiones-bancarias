// Ualá Bis Fee Updater
//
// Scrapes Ualá Bis (mPOS) fees from their product pages and updates data.json.
// Uses verified fallback rates for fees not published on their website.
//
// Source: https://mpos.ualabis.com.ar/productos/mpos/
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

const ualaID = "uala"
const primaryURL = "https://mpos.ualabis.com.ar/productos/mpos/"
const backupURL = "https://www.ualabis.com.ar/"

type ualaMapping struct {
	jsonConcept  string
	jsonTerm     string
	pageKeywords []string
	fallbackRate string
}

var feeMappings = []ualaMapping{
	{jsonConcept: "mPOS - Débito", jsonTerm: "En el momento", pageKeywords: []string{"débito", "debito"}, fallbackRate: "2.9% + IVA"},
	{jsonConcept: "mPOS - Crédito", jsonTerm: "En el momento", pageKeywords: []string{"crédito", "credito"}, fallbackRate: "4.4% + IVA"},
	{jsonConcept: "Link de Pago", jsonTerm: "En el momento", pageKeywords: []string{"link", "pago"}, fallbackRate: "4.4% + IVA"},
}

type scrapedFee struct {
	paymentType string
	fee         string
}

func normalizeFeeString(s string) string {
	s = regexp.MustCompile(`(?i)^desde\s+`).ReplaceAllString(strings.TrimSpace(s), "")
	s = strings.ReplaceAll(s, ",", ".")
	s = strings.ReplaceAll(s, "%", "")
	return strings.TrimSpace(s)
}

func scrapeFeesFromPage(htmlContent string) []scrapedFee {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(htmlContent))
	if err != nil {
		return nil
	}

	fullText := doc.Text()
	scriptText := ""
	doc.Find("script").Each(func(_ int, s *goquery.Selection) {
		scriptText += " " + s.Text()
	})
	searchable := fullText + " " + scriptText

	var fees []scrapedFee

	// Débito patterns
	debitPatterns := []string{
		`(\d+[,.]\d+)\s*%[^.]{0,50}(?:con\s+)?(?:tarjeta\s+de\s+)?d[ée]bito`,
		`(?i)d[ée]bito\s*:?\s*(\d+[,.]\d+)\s*%`,
		`(?i)["']?d[ée]bito["']?\s*:\s*["']?(\d+[,.]\d+)\s*%?["']?`,
	}
	for i, pat := range debitPatterns {
		re := regexp.MustCompile("(?i)" + pat)
		if m := re.FindStringSubmatch(searchable); m != nil {
			fee := normalizeFeeString(m[1])
			fees = append(fees, scrapedFee{paymentType: "débito", fee: fee})
			fmt.Printf("  Found débito fee: %s%% (pattern %d)\n", fee, i+1)
			break
		}
	}

	// Crédito patterns (RE2 compatible - no negative lookahead)
	creditPatterns := []string{
		`(\d+[,.]\d+)\s*%[^.]{0,50}(?:con\s+)?(?:tarjeta\s+de\s+)?cr[ée]dito`,
		`(?i)cr[ée]dito\s*:?\s*(\d+[,.]\d+)\s*%`,
		`(?i)cr[ée]dito\s+(?:en\s+(?:1|un)\s+pago|en\s+el\s+momento)[^.]{0,30}(\d+[,.]\d+)\s*%`,
		`(?i)["']?cr[ée]dito["']?\s*:\s*["']?(\d+[,.]\d+)\s*%?["']?`,
	}
	for i, pat := range creditPatterns {
		re := regexp.MustCompile("(?i)" + pat)
		if m := re.FindStringSubmatch(searchable); m != nil {
			fee := normalizeFeeString(m[1])
			fees = append(fees, scrapedFee{paymentType: "crédito", fee: fee})
			fmt.Printf("  Found crédito fee: %s%% (pattern %d)\n", fee, i+1)
			break
		}
	}

	// Link de pago patterns
	linkPatterns := []string{
		`(?i)link\s+de\s+pago[^.]{0,30}(\d+[,.]\d+)\s*%`,
		`(?i)(?:pago\s+online|e-commerce|ecommerce)[^.]{0,30}(\d+[,.]\d+)\s*%`,
		`(?i)["']?link[_\s]?(?:de[_\s])?pago["']?\s*:\s*["']?(\d+[,.]\d+)\s*%?["']?`,
	}
	for i, pat := range linkPatterns {
		re := regexp.MustCompile(pat)
		if m := re.FindStringSubmatch(searchable); m != nil {
			fee := normalizeFeeString(m[1])
			fees = append(fees, scrapedFee{paymentType: "link", fee: fee})
			fmt.Printf("  Found link de pago fee: %s%% (pattern %d)\n", fee, i+1)
			break
		}
	}

	return fees
}

func main() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Ualá Bis Fee Update Script")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println()

	// Fetch primary URL
	fmt.Printf("Fetching data from: %s\n", primaryURL)
	html, err := common.FetchPage(primaryURL)
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	scraped := scrapeFeesFromPage(html)

	// Try backup if few results
	if len(scraped) < 2 {
		fmt.Printf("\nPrimary source found %d fee(s). Trying backup: %s\n", len(scraped), backupURL)
		if backupHTML, err := common.FetchPage(backupURL); err == nil {
			backupFees := scrapeFeesFromPage(backupHTML)
			for _, bf := range backupFees {
				found := false
				for _, sf := range scraped {
					if sf.paymentType == bf.paymentType {
						found = true
						break
					}
				}
				if !found {
					scraped = append(scraped, bf)
					fmt.Printf("  Added %s fee from backup source\n", bf.paymentType)
				}
			}
		} else {
			fmt.Printf("  Backup URL failed: %v\n", err)
		}
	}

	fmt.Println()
	fmt.Println(strings.Repeat("-", 60))
	if len(scraped) > 0 {
		fmt.Printf("Scraping complete: %d fee(s) found\n", len(scraped))
		for _, f := range scraped {
			fmt.Printf("  - %s: %s%%\n", f.paymentType, f.fee)
		}
	} else {
		fmt.Println("INFO: No fees scraped from website (expected for Ualá)")
		fmt.Println("      Will use verified fallback rates")
	}
	fmt.Println(strings.Repeat("-", 60))
	fmt.Println()

	// Load data
	data, err := common.LoadData()
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Updating fees in data.json...")
	fmt.Println()

	entity := common.FindEntityByID(data, ualaID)
	if entity == nil {
		fmt.Printf("ERROR: Entity '%s' not found in %s\n", ualaID, common.DataFile)
		os.Exit(1)
	}

	updated := false
	scrapedCount := 0
	fallbackCount := 0

	for _, m := range feeMappings {
		var newRate, source string

		// Try scraped
		for _, sf := range scraped {
			for _, kw := range m.pageKeywords {
				if strings.Contains(strings.ToLower(sf.paymentType), kw) {
					newRate = sf.fee + "% + IVA"
					source = "scraped"
					scrapedCount++
					goto found
				}
			}
		}

		// Fallback
		newRate = m.fallbackRate
		source = "fallback"
		fallbackCount++
		if m.jsonConcept == "mPOS - Crédito" || m.jsonConcept == "Link de Pago" {
			fmt.Printf("INFO: Using verified fallback for '%s': %s (not published on website)\n", m.jsonConcept, newRate)
		} else {
			fmt.Printf("WARN: Could not scrape '%s' fee. Using fallback: %s\n", m.jsonConcept, newRate)
		}

	found:
		// Validate rate (2-6% range)
		valRe := regexp.MustCompile(`(\d+\.?\d*)`)
		if vm := valRe.FindStringSubmatch(newRate); vm != nil {
			var v float64
			fmt.Sscanf(vm[1], "%f", &v)
			if v < 2.0 || v > 6.0 {
				fmt.Printf("WARN: Unusual rate %.1f%% for '%s' (expected 2-6%%)\n", v, m.jsonConcept)
			}
		}

		fee := common.FindFee(entity.Fees, m.jsonConcept, m.jsonTerm)
		if fee == nil {
			fmt.Printf("WARN: Could not find fee in data.json for '%s' (%s)\n", m.jsonConcept, m.jsonTerm)
			continue
		}

		if common.UpdateFee(fee, newRate) {
			updated = true
		} else {
			fmt.Printf("  '%s' (%s): '%s' (source: %s)\n", fee.Concept, fee.Term, fee.Rate, source)
		}
	}

	fmt.Printf("\nSummary: %d fee(s) scraped, %d fallback(s) used\n", scrapedCount, fallbackCount)

	// Update feeUrl if needed
	newFeeURL := "https://mpos.ualabis.com.ar/productos/mpos/"
	urlUpdated := false
	if entity.FeeURL != newFeeURL {
		fmt.Printf("Updating feeUrl: '%s' -> '%s'\n", entity.FeeURL, newFeeURL)
		entity.FeeURL = newFeeURL
		urlUpdated = true
	}

	// Update lastUpdated timestamp (even if fees unchanged - shows "last verified")
	entity.LastUpdated = time.Now().UTC().Format(time.RFC3339)
	fmt.Printf("\nUpdated lastUpdated timestamp: %s\n", entity.LastUpdated)

	fmt.Println()
	fmt.Println(strings.Repeat("=", 60))

	if err := common.SaveData(data); err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	if updated || urlUpdated {
		fmt.Println("data.json has been successfully updated with new fee data")
	} else {
		fmt.Println("No fee changes detected, but lastUpdated timestamp refreshed")
	}

	fmt.Println(strings.Repeat("=", 60))
	fmt.Println()
	fmt.Println("Update complete!")
}
