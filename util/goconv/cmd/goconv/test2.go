package main

import (
	"flag"
	"fmt"
	"go/parser"
	"go/token"
	"os"
	"path"
	"path/filepath"
)

func main2() {
	flag.Parse()
	if flag.NArg() == 0 {
		flag.Usage()
		os.Exit(1)
	}

	srcPath := filepath.Clean(path.Join(flag.Arg(0), "src", "text", "template"))
	fmt.Printf("Source path: %s...\n", srcPath)

	if _, err := os.Stat(srcPath); os.IsNotExist(err) {
		fmt.Printf("File not found: %s", err)
	}

	fset := token.NewFileSet()
	template_dir, err := parser.ParseDir(fset, path.Join(srcPath), nil, parser.ParseComments)
	// f is of type *ast.File
	if err != nil {
		panic(err)
	}

	parse_dir, err := parser.ParseDir(fset, path.Join(srcPath, "parse"), nil, parser.ParseComments)
	// f is of type *ast.File
	if err != nil {
		panic(err)
	}

	fmt.Println("Found imports:")

	for pname, p := range template_dir {
		for fname, f := range p.Files {
			for _, s := range f.Imports {
				fmt.Printf("%s -- %s: %s\n", fname, pname, s.Path.Value)
			}
		}
	}

	for pname, p := range parse_dir {
		for fname, f := range p.Files {
			for _, s := range f.Imports {
				fmt.Printf("%s -- %s: %s\n", fname, pname, s.Path.Value)
			}
		}

	}
}
