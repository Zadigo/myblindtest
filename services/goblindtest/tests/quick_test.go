package tests

import (
	"fmt"
	"regexp"
	"strings"
)

func TestGoogle() {
	text := "Hello, hello! How are you doing today? Today is a great day."
	wordCount := map[string]int{}

	if r, err := regexp.Compile(`\W`); err != nil {
		return
	} else {
		r.ReplaceAll([]byte(text), []byte(" "))
	}

	for t := range strings.SplitSeq(text, " ") {
		wordCount[strings.Trim(strings.ToLower(t), " ")]++
	}

	fmt.Print(wordCount)
}
