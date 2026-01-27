// Mercado Pago Fee Updater
//
// Scrapes the official Mercado Pago fees pages for Buenos Aires province
// and updates the corresponding entries in data.json.
//
// Sources:
//   - Point fees: https://www.mercadopago.com.ar/ayuda/2779
//   - QR fees: https://www.mercadopago.com.ar/ayuda/3605
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

const mpID = "mercadopago"

const (
	pointFeeURL = "https://www.mercadopago.com.ar/ayuda/2779"
	qrFeeURL    = "https://www.mercadopago.com.ar/ayuda/3605"
)

type scrapedFee struct {
	paymentType string
	fee         string
	term        string
}

type feeMapping struct {
	source          string // "point" or "qr"
	jsonConcept     string
	jsonTerm        string
	pagePaymentType string
	pageTerm        string
	parseAsRange    bool
}

var feeMappings = []feeMapping{
	{source: "point", jsonConcept: "Point - Débito", jsonTerm: "En el momento", pagePaymentType: "Tarjeta de débito", pageTerm: "Al instante"},
	{source: "point", jsonConcept: "Point - Crédito", jsonTerm: "En el momento", pagePaymentType: "Tarjeta de crédito", pageTerm: "Al instante"},
	{source: "point", jsonConcept: "Point - Crédito", jsonTerm: "14 días", pagePaymentType: "Tarjeta de crédito", pageTerm: "10 días"},
	{source: "qr", jsonConcept: "QR", jsonTerm: "En el momento", parseAsRange: true},
}

func scrapeFeesFromPage(htmlContent string) []scrapedFee {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(htmlContent))
	if err != nil {
		fmt.Println("WARN: Could not parse HTML")
		return nil
	}

	tableDiv := doc.Find("div#tabla1")
	if tableDiv.Length() == 0 {
		fmt.Println("WARN: Could not find the fees table (id='tabla1')")
		return nil
	}

	table := tableDiv.Find("table")
	if table.Length() == 0 {
		fmt.Println("WARN: Found the table div but no table inside")
		return nil
	}

	var fees []scrapedFee
	var currentPaymentType string

	table.Find("tbody tr").Each(func(_ int, row *goquery.Selection) {
		cells := row.Find("td")
		var fee, term string

		switch cells.Length() {
		case 3:
			currentPaymentType = strings.TrimSpace(cells.Eq(0).Text())
			fee = strings.TrimSpace(cells.Eq(1).Text())
			term = strings.TrimSpace(cells.Eq(2).Text())
		case 2:
			fee = strings.TrimSpace(cells.Eq(0).Text())
			term = strings.TrimSpace(cells.Eq(1).Text())
		default:
			return
		}

		if currentPaymentType != "" && strings.Contains(fee, "%") {
			fees = append(fees, scrapedFee{
				paymentType: currentPaymentType,
				fee:         fee,
				term:        term,
			})
		}
	})

	return fees
}

func findScrapedFee(fees []scrapedFee, paymentType, term string) string {
	for _, f := range fees {
		if strings.Contains(f.paymentType, paymentType) && f.term == term {
			rate := f.fee + " + IVA"
			return common.NormalizeDecimalSeparator(rate)
		}
	}
	return ""
}

func constructQRFeeRange(fees []scrapedFee) string {
	if len(fees) == 0 {
		return ""
	}

	re := regexp.MustCompile(`(\d+[,.]?\d*)\s*%`)
	type feeVal struct {
		value float64
		text  string
	}
	var values []feeVal

	for _, f := range fees {
		m := re.FindStringSubmatch(f.fee)
		if m != nil {
			numStr := strings.ReplaceAll(m[1], ",", ".")
			var v float64
			fmt.Sscanf(numStr, "%f", &v)
			values = append(values, feeVal{v, f.fee})
		}
	}

	if len(values) == 0 {
		return ""
	}

	minFee := values[0]
	maxFee := values[0]
	for _, v := range values[1:] {
		if v.value < minFee.value {
			minFee = v
		}
		if v.value > maxFee.value {
			maxFee = v
		}
	}

	var result string
	if math.Abs(minFee.value-maxFee.value) < 0.001 {
		result = minFee.text + " + IVA"
	} else {
		result = minFee.text + " - " + maxFee.text + " + IVA (según medio)"
	}

	return common.NormalizeDecimalSeparator(result)
}

func main() {
	fmt.Println("Starting Mercado Pago fee update...")
	fmt.Println(strings.Repeat("=", 70))

	// Scrape Point fees
	fmt.Printf("\n1. Fetching Point fees from: %s\n", pointFeeURL)
	pointHTML, err := common.FetchPage(pointFeeURL)
	if err != nil {
		fmt.Printf("\nERROR: Failed to fetch Point URL: %v\n", err)
		os.Exit(1)
	}
	pointFees := scrapeFeesFromPage(pointHTML)
	if len(pointFees) == 0 {
		fmt.Println("WARNING: Could not extract any Point fees from the page.")
	} else {
		fmt.Printf("Successfully scraped %d Point fee entries\n", len(pointFees))
	}

	// Scrape QR fees
	fmt.Printf("\n2. Fetching QR fees from: %s\n", qrFeeURL)
	qrHTML, err := common.FetchPage(qrFeeURL)
	if err != nil {
		fmt.Printf("\nERROR: Failed to fetch QR URL: %v\n", err)
		os.Exit(1)
	}
	qrFees := scrapeFeesFromPage(qrHTML)
	if len(qrFees) == 0 {
		fmt.Println("WARNING: Could not extract any QR fees from the page.")
	} else {
		fmt.Printf("Successfully scraped %d QR fee entries\n", len(qrFees))
	}

	if len(pointFees) == 0 && len(qrFees) == 0 {
		fmt.Println("\nERROR: Could not extract any fees from either page. No changes were made.")
		os.Exit(1)
	}

	// Load and update data.json
	fmt.Printf("\n3. Updating %s...\n", common.DataFile)
	fmt.Println(strings.Repeat("-", 70))

	data, err := common.LoadData()
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	mp := common.FindEntityByID(data, mpID)
	if mp == nil {
		fmt.Printf("ERROR: Entity '%s' not found in %s\n", mpID, common.DataFile)
		os.Exit(1)
	}

	updated := false
	for _, m := range feeMappings {
		var newRate string
		var scraped []scrapedFee

		if m.source == "qr" {
			scraped = qrFees
		} else {
			scraped = pointFees
		}

		if m.parseAsRange {
			newRate = constructQRFeeRange(scraped)
			if newRate == "" {
				fmt.Println("WARN: Could not construct QR fee range from scraped data. Skipping.")
				continue
			}
		} else {
			newRate = findScrapedFee(scraped, m.pagePaymentType, m.pageTerm)
			if newRate == "" {
				fmt.Printf("WARN: Could not find a matching scraped fee for %s - %s. Skipping.\n", m.jsonConcept, m.jsonTerm)
				continue
			}
		}

		fee := common.FindFee(mp.Fees, m.jsonConcept, m.jsonTerm)
		if fee == nil {
			fmt.Printf("WARN: Could not find fee in data.json for '%s' (%s)\n", m.jsonConcept, m.jsonTerm)
			continue
		}

		if common.UpdateFee(fee, newRate) {
			updated = true
		}
	}

	fmt.Println(strings.Repeat("-", 70))

	if updated {
		if err := common.SaveData(data); err != nil {
			fmt.Printf("ERROR: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("\n%s has been successfully updated.\n", common.DataFile)
	} else {
		fmt.Printf("\nNo fee changes detected. %s remains unchanged.\n", common.DataFile)
	}

	// Update date stamp
	fmt.Printf("\n4. Updating date stamp in %s...\n", common.IndexFile)
	common.UpdateDateInHTML()

	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("Script finished successfully.")
}
