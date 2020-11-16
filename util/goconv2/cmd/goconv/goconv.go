package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	flag.Parse()
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	outputPath := filepath.Clean(flag.Arg(0))

	fmt.Printf("Output path: %s...\n", outputPath)

	conv, err := NewConv()
	if err != nil {
		panic(err)
	}

	for _, pv := range conv.Packages {
		filename := filepath.Join(outputPath, fmt.Sprintf("%s.py", strings.Replace(pv.PkgPath, "/", ".", -1)))
		err = conv.OutputFile(pv, filename)
		if err != nil {
			panic(err)
		}
	}
}
