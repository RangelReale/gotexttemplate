package main

import (
	"fmt"
	"go/ast"
	"go/token"
	"go/types"
	"strings"
)







func (c *Conv) isExternalImport(pkg *types.Package) bool {
	for _, pc := range c.Packages {
		if pc.Types == pkg {
			return false
		}
	}
	return true
}

type Poser interface {
	Pos() token.Pos
}

func (c *Conv) FileOf(poser Poser) *ast.File {
	for _, pkg := range c.Packages {
		for _, file := range pkg.Syntax {
			if file.Pos() <= poser.Pos() && file.End() > poser.Pos() {
				return file
			}
		}
	}
	return nil
}

func (c *Conv) ReturnLineComment(typeObj types.Object) string {
	fast := c.AstOf(typeObj)
	if fast != nil {
		switch xfast := fast.(type) {
		case *ast.Field:
			if xfast.Comment != nil && len(xfast.Comment.List) > 0 {
				return fmt.Sprintf("  # %s", strings.TrimSpace(xfast.Comment.Text()))
			}
		case *ast.ValueSpec:
			if xfast.Comment != nil && len(xfast.Comment.List) > 0 {
				return fmt.Sprintf("  # %s", strings.TrimSpace(xfast.Comment.Text()))
			}
		case *ast.TypeSpec:
			if xfast.Comment != nil && len(xfast.Comment.List) > 0 {
				return fmt.Sprintf("  # %s", strings.TrimSpace(xfast.Comment.Text()))
			}
		}
	}

	return ""
}

func (c *Conv) AstOf(typeObj types.Object) (typeAst ast.Node) {
	ast.Inspect(c.FileOf(typeObj), func(node ast.Node) bool {
		if node == nil {
			return true
		}

		switch node.(type) {
		case *ast.File:
			// ignore
		default:
			if node.Pos() == typeObj.Pos() {
				typeAst = node
				return false
			}
		}
		return true
	})
	return
}
