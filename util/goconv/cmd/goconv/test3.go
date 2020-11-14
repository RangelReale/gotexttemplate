package main

import (
	"bytes"
	"flag"
	"fmt"
	"go/ast"
	"go/format"
	"go/token"
	"go/types"
	"golang.org/x/tools/go/packages"
	"golang.org/x/tools/go/types/typeutil"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func main3() {
	flag.Parse()
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	outputPath := filepath.Clean(flag.Arg(0))

	fmt.Printf("Output path: %s...\n", outputPath)

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

	fset := token.NewFileSet()
	cfg := &packages.Config{Fset: fset, Mode: mode}
	pkgs, err := packages.Load(cfg, "text/template", "text/template/parse")
	if err != nil {
		log.Fatal(err)
	}

	if packages.PrintErrors(pkgs) > 0 {
		os.Exit(1)
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
	// package members (TypeCheck or WholeProgram mode)
	if pkg.Types != nil {
		qual := types.RelativeTo(pkg.Types)
		scope := pkg.Types.Scope()
		for _, name := range scope.Names() {
			obj := scope.Lookup(name)
			//if !obj.Exported() && !app.Private {
			//	continue // skip unexported names
			//}

			fmt.Printf("\t%s\n", types.ObjectString(obj, qual))
			if _, ok := obj.(*types.TypeName); ok {
				for _, meth := range typeutil.IntuitiveMethodSet(obj.Type(), nil) {
					//if !meth.Obj().Exported() && !app.Private {
					//	continue // skip unexported names
					//}
					fmt.Printf("\t%s\n", types.SelectionString(meth, qual))
				}
			}
		}
	}

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
				if x.Recv != nil {
					fmt.Printf("Function (%s): %s -- %s\n", typeName(x.Recv.List[0].Type), x.Name, fset.Position(x.Pos()))
				} else {
					fmt.Printf("Function: %s -- %s\n", x.Name, fset.Position(x.Pos()))
				}
			}
			return true
		})
	}
}

// Return the name of the type as string.  This routine is borrowed from the
// error.go file of the gofix command.
func typeName(typ ast.Expr) string {
	if p, ok := typ.(*ast.StarExpr); ok {
		typ = p.X
	}
	id, ok := typ.(*ast.Ident)
	if ok {
		return id.Name
	}
	sel, ok := typ.(*ast.SelectorExpr)
	if ok {
		return typeName(sel.X) + "." + sel.Sel.Name
	}
	return ""
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
