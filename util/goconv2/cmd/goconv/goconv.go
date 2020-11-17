package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	flag.Parse()
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	outputPath := filepath.Clean(flag.Arg(0))

	fmt.Printf("Output path: %s...\n", outputPath)

	conv, err := NewConv(true)
	if err != nil {
		panic(err)
	}

	for _, pv := range conv.Packages {
		cf, err := conv.File(pv)
		if err != nil {
			panic(err)
		}

		filename := filepath.Join(outputPath, cf.Filename())
		err = cf.OutputFile(filename)
		if err != nil {
			panic(err)
		}
	}
}
