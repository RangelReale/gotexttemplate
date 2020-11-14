package main

import (
	"bytes"
	"flag"
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"go/types"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"golang.org/x/tools/go/packages"
	"strings"
)

func main() {
	flag.Parse()
	if flag.NArg() < 2 {
		flag.Usage()
		os.Exit(1)
	}

	srcPath := filepath.Clean(path.Join(flag.Arg(0), "src", "text", "template"))
	outputPath := filepath.Clean(flag.Arg(1))

	fmt.Printf("Source path: %s...\n", srcPath)
	fmt.Printf("Output path: %s...\n", outputPath)

	if _, err := os.Stat(srcPath); os.IsNotExist(err) {
		fmt.Printf("File not found: %s", err)
	}

	const mode packages.LoadMode = packages.NeedName |
		packages.NeedFiles |
		packages.NeedCompiledGoFiles |
		packages.NeedImports |
		packages.NeedDeps |
		packages.NeedExportsFile |
		packages.NeedTypes |
		packages.NeedSyntax |
		packages.NeedTypesInfo |
		packages.NeedTypesInfo

	pattern := "./..."

	fset := token.NewFileSet()
	cfg := &packages.Config{Fset: fset, Mode: mode, Dir: srcPath}
	pkgs, err := packages.Load(cfg, pattern)
	if err != nil {
		log.Fatal(err)
	}

	for _, p := range pkgs {
		fmt.Printf("Package: %s\n", p.PkgPath)
		var pb strings.Builder
		//for _, s := range p.Imports {
		//	fmt.Printf("import %s\n", s.PkgPath)
		//}
		findInPackage(&pb, p, fset)
		err = ioutil.WriteFile(filepath.Join(outputPath, fmt.Sprintf("%s.py", p.Name)), []byte(pb.String()), 0644)
		if err != nil {
			panic(err)
		}
	}
}

func findInPackage(pb *strings.Builder, pkg *packages.Package, fset *token.FileSet) {
	for _, fileAst := range pkg.Syntax {
		var lastname string
		var err error
		ast.Inspect(fileAst, func(n ast.Node) bool {
			switch x := n.(type) {
			case *ast.Ident:
				lastname = x.Name
			case *ast.TypeSpec:
				if x.Type == nil {
					return true
				}
				switch xt := x.Type.(type) {
				case *ast.StructType:
					_, err = fmt.Fprintf(pb, "# %s\n", fset.Position(x.Pos()))
					if err != nil {
						panic(err)
					}

					bases := BaseClass(xt.Fields, n, pkg.TypesInfo, fset)
					baseclass := ""
					if len(bases) > 0 {
						baseclass = fmt.Sprintf("(%s)", strings.Join(bases, ", "))
					}

					fmt.Fprintf(pb, "class %s%s: \n", x.Name.Name, baseclass)
					fmt.Fprintf(pb, "    pass\n")
					fmt.Fprintf(pb, "\n")

					fmt.Printf("Struct: %s -- %s\n", x.Name.Name, fset.Position(x.Pos()))
					//fmt.Println(nodeString(x, fset))
					//ast.Print(fset, structTy)
					//findInFields(x.Fields, n, pkg.TypesInfo, fset)
				case *ast.InterfaceType:
					//fmt.Printf("Interface %s -- %s\n", lastname, fset.Position(x.Pos()))
					//fmt.Println(nodeString(x, fset))
					//ast.Print(fset, interfaceTy.Interface)
					//findInFields(interfaceTy.Methods, n, pkg.TypesInfo, fset)
				}
			case *ast.FuncDecl:
				//fmt.Printf("Function: %s -- %s\n", lastname, fset.Position(x.Pos()))
			}
			return true
		})
	}
}

func BaseClass(fl *ast.FieldList, n ast.Node, tinfo *types.Info, fset *token.FileSet) []string {
	//type FieldReport struct {
	//	Name string
	//	Type types.Type
	//}
	//var reps []FieldReport

	ret := []string{}

	for _, field := range fl.List {
		if field.Names == nil {
			tv, ok := tinfo.Types[field.Type]
			if !ok {
				log.Fatal("not found", field.Type)
			}

			embName := fmt.Sprintf("%v", field.Type)

			switch tv.Type.Underlying().(type) {
			case *types.Struct:
				ret = append(ret, embName)
			case *types.Interface:
				ret = append(ret, embName)
			default:
			}
		}
	}

	return ret
}

func findInFields(fl *ast.FieldList, n ast.Node, tinfo *types.Info, fset *token.FileSet) {
	type FieldReport struct {
		Name string
		Kind string
		Type types.Type
	}
	var reps []FieldReport

	for _, field := range fl.List {
		if field.Names == nil {
			tv, ok := tinfo.Types[field.Type]
			if !ok {
				log.Fatal("not found", field.Type)
			}

			embName := fmt.Sprintf("%v", field.Type)

			_, hostIsStruct := n.(*ast.StructType)
			var kind string

			switch typ := tv.Type.Underlying().(type) {
			case *types.Struct:
				if hostIsStruct {
					kind = "struct (s@s)"
				} else {
					kind = "struct (s@i)"
				}
				reps = append(reps, FieldReport{embName, kind, typ})
			case *types.Interface:
				if hostIsStruct {
					kind = "interface (i@s)"
				} else {
					kind = "interface (i@i)"
				}
				reps = append(reps, FieldReport{embName, kind, typ})
			default:
			}
		}
	}

	if len(reps) > 0 {
		fmt.Printf("Found at %v\n%v\n", fset.Position(n.Pos()), nodeString(n, fset))

		for _, report := range reps {
			fmt.Printf("--> field '%s' is embedded %s: %s\n", report.Name, report.Kind, report.Type)
		}
		fmt.Println("")
	}
}

// nodeString formats a syntax tree in the style of gofmt.
func nodeString(n ast.Node, fset *token.FileSet) string {
	var buf bytes.Buffer
	format.Node(&buf, fset, n)
	return buf.String()
}

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