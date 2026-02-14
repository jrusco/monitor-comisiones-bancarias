package common

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

const (
	DataFile  = "data.json"
	IndexFile = "index.html"
)

// Fee represents a single fee entry in an entity.
type Fee struct {
	Concept string `json:"concept"`
	Term    string `json:"term"`
	Rate    string `json:"rate"`
}

// Entity represents a financial entity in data.json.
type Entity struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Type        string `json:"type"`
	Color       string `json:"color"`
	TextColor   string `json:"textColor"`
	Logo        string `json:"logo"`
	FeeURL      string `json:"feeUrl"`
	APIURL      string `json:"apiUrl"`
	APIDocs     string `json:"apiDocs,omitempty"`
	HasAPI      bool   `json:"hasApi"`
	LastUpdated string `json:"lastUpdated,omitempty"`
	Fees        []Fee  `json:"fees"`
}

// LoadData reads and parses data.json.
func LoadData() ([]Entity, error) {
	raw, err := os.ReadFile(DataFile)
	if err != nil {
		return nil, fmt.Errorf("reading %s: %w", DataFile, err)
	}
	var data []Entity
	if err := json.Unmarshal(raw, &data); err != nil {
		return nil, fmt.Errorf("parsing %s: %w", DataFile, err)
	}
	return data, nil
}

// SaveData writes entities back to data.json with indentation.
func SaveData(data []Entity) error {
	raw, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		return fmt.Errorf("marshalling data: %w", err)
	}
	// Unescape HTML entities that json.Marshal escapes (e.g. & < >)
	output := strings.ReplaceAll(string(raw), "\\u0026", "&")
	output = strings.ReplaceAll(output, "\\u003c", "<")
	output = strings.ReplaceAll(output, "\\u003e", ">")
	if err := os.WriteFile(DataFile, []byte(output+"\n"), 0644); err != nil {
		return fmt.Errorf("writing %s: %w", DataFile, err)
	}
	return nil
}

// FindEntityByID returns a pointer to the entity with the given ID, or nil.
func FindEntityByID(data []Entity, id string) *Entity {
	for i := range data {
		if data[i].ID == id {
			return &data[i]
		}
	}
	return nil
}

// FindFee returns a pointer to the fee matching concept and term, or nil.
func FindFee(fees []Fee, concept, term string) *Fee {
	for i := range fees {
		if fees[i].Concept == concept && fees[i].Term == term {
			return &fees[i]
		}
	}
	return nil
}

// UpdateFee updates a fee's rate if it changed. Returns true if updated.
func UpdateFee(fee *Fee, newRate string) bool {
	if fee.Rate != newRate {
		fmt.Printf("  Updating '%s' (%s): '%s' -> '%s'\n", fee.Concept, fee.Term, fee.Rate, newRate)
		fee.Rate = newRate
		return true
	}
	fmt.Printf("  Fee '%s' (%s) already current: '%s'\n", fee.Concept, fee.Term, fee.Rate)
	return false
}

// NormalizeDecimalSeparator converts Argentine comma to international dot.
func NormalizeDecimalSeparator(s string) string {
	return strings.ReplaceAll(s, ",", ".")
}
