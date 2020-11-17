package main

import (
	"fmt"
	"github.com/jimmyfrasche/closed"
	"go/ast"
	"go/token"
	"go/types"
	"strings"
)

func (c *Conv) baseTypes(typ types.Type) (basetypes []types.Type) {
	switch t := typ.(type) {
	case *types.Named:
		return c.baseTypes(t.Underlying())
	case *types.Struct:
		for i := 0; i < t.NumFields(); i++ {
			f := t.Field(i)
			if f.Embedded() {
				//basetypes = append(basetypes, f)
				basetypes = append(basetypes, f.Type())
			}
		}
	case *types.Interface:
		for i := 0; i < t.NumEmbeddeds(); i++ {
			f := t.EmbeddedType(i)
			basetypes = append(basetypes, f)
		}
	}

	return
}

func (c *Conv) baseTypesFiltered(s *types.TypeName, closedTypes []closed.Type) (basetypes []types.Type) {
	basetypes = c.baseTypes(s.Type())

	itftypes := c.itfTypes(s, closedTypes)

	for _, bt := range basetypes {
		for ifi := len(itftypes) - 1; ifi >= 0; ifi-- {
			if types.Implements(types.NewPointer(bt), itftypes[ifi].Underlying().(*types.Interface)) {
				itftypes = append(itftypes[:ifi], itftypes[ifi+1:]...) // remove item
			}
		}
	}

	for _, ifi := range itftypes {
		basetypes = append([]types.Type{ifi}, basetypes...)
	}

	return
}


func (c *Conv) itfTypes(t *types.TypeName, closedTypes []closed.Type) (itftypes []types.Type) {
	for _, v := range closedTypes {
		switch v := v.(type) {
		case *closed.Interface:
		EndLoop:
			for _, cm := range v.Members {
				for _, cmt := range cm.TypeName {
					if t == cmt {
						for _, ct := range v.Types() {
							itftypes = append(itftypes, ct.Type())
						}
						break EndLoop
					}
				}
			}
		}
	}
	return
}

func (c *Conv) typeIsEnum(typ types.Object, closedTypes []closed.Type) bool {
	for _, v := range closedTypes {
		switch v := v.(type) {
		case *closed.Enum:
			for _, et := range v.Types() {
				if et == typ {
					return true
				}
			}
			for _, lbl := range v.Labels {
				for _, lbli := range lbl {
					if lbli == typ {
						return true
					}
				}
			}
		}
	}
	return false
}

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
