package utils

import (
	"html/template"
	"log"
	"os"
	"strings"
)

func MakeURLSafe(d string) string {
	return strings.ReplaceAll(d, " ", "+")
}

func UnMakeURLSafe(d string) string {
	return strings.ReplaceAll(d, "+", " ")
}

// Minimal writer that appends to a byte slice
type bufferWriter struct {
	buf *[]byte
}

func (w *bufferWriter) Write(p []byte) (int, error) {
	*w.buf = append(*w.buf, p...)
	return len(p), nil
}

func RenderTemplate(filename string, data any) string {
	wd, _ := os.Getwd()
	filename = wd + "/" + filename
	filename = strings.Replace(filename, "src/tests", "", 1)

	tmpl, err := template.ParseFiles(filename)
	if err != nil {
		// return "", err
		log.Panic(err)
	}

	var buf []byte
	w := &bufferWriter{&buf}

	if err := tmpl.Execute(w, data); err != nil {
		log.Panic(err)
	}

	return string(buf)
}
