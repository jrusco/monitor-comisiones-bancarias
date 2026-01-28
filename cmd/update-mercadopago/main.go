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

// fetchAndScrapeFees fetches a page and extracts fee data from it.
// Returns the scraped fees and any fetch error.
func fetchAndScrapeFees(name, url string) ([]scrapedFee, error) {
	html, err := common.FetchPage(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch %s URL: %w", name, err)
	}
	fees := scrapeFeesFromPage(html)
	if len(fees) == 0 {
		fmt.Printf("WARNING: Could not extract any %s fees from the page.\n", name)
	} else {
		fmt.Printf("Successfully scraped %d %s fee entries\n", len(fees), name)
	}
	return fees, nil
}

// getRateForMapping looks up the rate for a fee mapping from scraped data.
func getRateForMapping(m feeMapping, pointFees, qrFees []scrapedFee) string {
	var scraped []scrapedFee
	if m.source == "qr" {
		scraped = qrFees
	} else {
		scraped = pointFees
	}

	if m.parseAsRange {
		return constructQRFeeRange(scraped)
	}
	return findScrapedFee(scraped, m.pagePaymentType, m.pageTerm)
}

// processFeeMapping processes a single fee mapping and returns whether an update occurred.
func processFeeMapping(m feeMapping, mp *common.Entity, pointFees, qrFees []scrapedFee) bool {
	newRate := getRateForMapping(m, pointFees, qrFees)
	if newRate == "" {
		if m.parseAsRange {
			fmt.Println("WARN: Could not construct QR fee range from scraped data. Skipping.")
		} else {
			fmt.Printf("WARN: Could not find a matching scraped fee for %s - %s. Skipping.\n", m.jsonConcept, m.jsonTerm)
		}
		return false
	}

	fee := common.FindFee(mp.Fees, m.jsonConcept, m.jsonTerm)
	if fee == nil {
		fmt.Printf("WARN: Could not find fee in data.json for '%s' (%s)\n", m.jsonConcept, m.jsonTerm)
		return false
	}

	return common.UpdateFee(fee, newRate)
}

// saveIfUpdated saves data.json if updates were made, otherwise reports no changes.
func saveIfUpdated(data []common.Entity, updated bool) error {
	if updated {
		if err := common.SaveData(data); err != nil {
			return err
		}
		fmt.Printf("\n%s has been successfully updated.\n", common.DataFile)
	} else {
		fmt.Printf("\nNo fee changes detected. %s remains unchanged.\n", common.DataFile)
	}
	return nil
}

func main() {
	fmt.Println("Starting Mercado Pago fee update...")
	fmt.Println(strings.Repeat("=", 70))

	// 1. Scrape Point fees
	fmt.Printf("\n1. Fetching Point fees from: %s\n", pointFeeURL)
	pointFees, err := fetchAndScrapeFees("Point", pointFeeURL)
	if err != nil {
		fmt.Printf("\nERROR: %v\n", err)
		os.Exit(1)
	}

	// 2. Scrape QR fees
	fmt.Printf("\n2. Fetching QR fees from: %s\n", qrFeeURL)
	qrFees, err := fetchAndScrapeFees("QR", qrFeeURL)
	if err != nil {
		fmt.Printf("\nERROR: %v\n", err)
		os.Exit(1)
	}

	if len(pointFees) == 0 && len(qrFees) == 0 {
		fmt.Println("\nERROR: Could not extract any fees from either page. No changes were made.")
		os.Exit(1)
	}

	// 3. Load and update data.json
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
		if processFeeMapping(m, mp, pointFees, qrFees) {
			updated = true
		}
	}

	fmt.Println(strings.Repeat("-", 70))

	if err := saveIfUpdated(data, updated); err != nil {
		fmt.Printf("ERROR: %v\n", err)
		os.Exit(1)
	}

	// 4. Update date stamp
	fmt.Printf("\n4. Updating date stamp in %s...\n", common.IndexFile)
	common.UpdateDateInHTML()

	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("Script finished successfully.")
}
