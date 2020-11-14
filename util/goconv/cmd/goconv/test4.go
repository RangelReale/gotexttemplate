package main

import (
	"bytes"
	"fmt"
	"go/ast"
	"go/format"
	"go/token"
	"go/types"
	"golang.org/x/tools/go/packages"
	"log"
	"os"
	"sort"
	"strings"
)

func main4() {
	const loadmode packages.LoadMode = packages.NeedName |
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
	cfg := &packages.Config{Fset: fset, Mode: loadmode}
	pkgs, err := packages.Load(cfg, "text/template", "text/template/parse")
	if err != nil {
		log.Fatal(err)
	}

	if packages.PrintErrors(pkgs) > 0 {
		os.Exit(1)
	}

	for _, pkg := range pkgs {
		// Print package-level variables in initialization order.
		fmt.Printf("InitOrder: %v\n\n", pkg.TypesInfo.InitOrder)

		// For each named object, print the line and
		// column of its definition and each of its uses.
		fmt.Println("Defs and Uses of each named object:")
		usesByObj := make(map[types.Object][]string)
		for id, obj := range pkg.TypesInfo.Uses {
			posn := fset.Position(id.Pos())
			lineCol := fmt.Sprintf("%d:%d", posn.Line, posn.Column)
			usesByObj[obj] = append(usesByObj[obj], lineCol)
		}
		var items []string
		for obj, uses := range usesByObj {
			sort.Strings(uses)
			item := fmt.Sprintf("%s:\n  defined at %s\n  used at %s",
				types.ObjectString(obj, types.RelativeTo(pkg.Types)),
				fset.Position(obj.Pos()),
				strings.Join(uses, ", "))
			items = append(items, item)
		}
		sort.Strings(items) // sort by line:col, in effect
		fmt.Println(strings.Join(items, "\n"))
		fmt.Println()

		fmt.Println("Types and Values of each expression:")
		items = nil
		for expr, tv := range pkg.TypesInfo.Types {
			var buf bytes.Buffer
			posn := fset.Position(expr.Pos())
			tvstr := tv.Type.String()
			if tv.Value != nil {
				tvstr += " = " + tv.Value.String()
			}
			// line:col | expr | mode : type = value
			fmt.Fprintf(&buf, "%2d:%2d | %-19s | %-7s : %s",
				posn.Line, posn.Column, exprString(fset, expr),
				mode(tv), tvstr)
			items = append(items, buf.String())
		}
		sort.Strings(items)
		fmt.Println(strings.Join(items, "\n"))
	}
}

func mode(tv types.TypeAndValue) string {
	switch {
	case tv.IsVoid():
		return "void"
	case tv.IsType():
		return "type"
	case tv.IsBuiltin():
		return "builtin"
	case tv.IsNil():
		return "nil"
	case tv.Assignable():
		if tv.Addressable() {
			return "var"
		}
		return "mapindex"
	case tv.IsValue():
		return "value"
	default:
		return "unknown"
	}
}

func exprString(fset *token.FileSet, expr ast.Expr) string {
	var buf bytes.Buffer
	format.Node(&buf, fset, expr)
	return buf.String()
}
