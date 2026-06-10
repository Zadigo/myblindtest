package models

import (
	"fmt"
	"strings"
)

// Returns a key for Redis by concatenating the base key with the provided values
func GetKey(values ...string) string {
	baseKey := "gojoker"
	value := strings.Join(values, ":")
	return fmt.Sprintf("%s:%s", baseKey, value)
}
