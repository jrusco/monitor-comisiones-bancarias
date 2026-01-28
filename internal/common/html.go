package common

import (
	"fmt"
	"os"
	"regexp"
	"time"
)

// UpdateDateInHTML updates the "Actualizado: DD/MM/YY" date stamp in index.html.
func UpdateDateInHTML() bool {
	fmt.Printf("Updating date stamp in %s...\n", IndexFile)

	content, err := os.ReadFile(IndexFile)
	if err != nil {
		fmt.Printf("  Warning: %s not found, skipping date update\n", IndexFile)
		return false
	}

	currentDate := time.Now().Format("02/01/06")
	pattern := regexp.MustCompile(`(Actualizado:\s*)\d{2}/\d{2}/\d{2}`)

	if !pattern.Match(content) {
		fmt.Printf("  Warning: Could not find date pattern in %s\n", IndexFile)
		return false
	}

	updated := pattern.ReplaceAllString(string(content), "${1}"+currentDate)

	if updated != string(content) {
		if err := os.WriteFile(IndexFile, []byte(updated), 0644); err != nil {
			fmt.Printf("  Warning: Failed to update date in %s: %v\n", IndexFile, err)
			return false
		}
		fmt.Printf("  Updated date stamp to: %s\n", currentDate)
		return true
	}

	fmt.Printf("  Date stamp already current: %s\n", currentDate)
	return false
}
