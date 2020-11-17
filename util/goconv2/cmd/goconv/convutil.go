package main

import (
	"fmt"
	"go/ast"
	"go/token"
	"go/types"
	"strings"

	"golang.org/x/tools/go/packages"
	"golang.org/x/tools/go/types/typeutil"
)

//extract what we care about from scope.
func (c *Conv) extract(s *types.Scope) (consts []*types.Const, funcs []*types.Func,
	vars []*types.Var, allTypes []*types.TypeName) {
	for _, nm := range s.Names() {
		switch o := s.Lookup(nm).(type) {
		case *types.Const:
			consts = append(consts, o)
		case *types.Var:
			vars = append(vars, o)
		case *types.Func:
			funcs = append(funcs, o)
		case *types.TypeName:
			allTypes = append(allTypes, o)
		default:
			fmt.Printf("Unknown type: %T\n", o)
			//discard
		}
	}
	return
}

func (c *Conv) findTypes(ts []*types.TypeName) (typs []*types.TypeName) {
	for _, t := range ts {
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Struct:
			case *types.Interface:
			default:
				typs = append(typs, t)
			}
		} else {
			typs = append(typs, t)
		}
	}
	return
}

func (c *Conv) findInterfaces(ts []*types.TypeName) (interfaces []*types.TypeName) {
	for _, t := range ts {
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Interface:
				interfaces = append(interfaces, t)
			}
		}
	}
	return
}

func (c *Conv) findStructs(ts []*types.TypeName) (structs []*types.TypeName) {
	for _, t := range ts {
		found := false
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Struct:
				structs = append(structs, t)
				found = true
			case *types.Interface:
				found = true
			}
		}

		if !found {
			imset := typeutil.IntuitiveMethodSet(t.Type(), nil)
			if len(imset) > 0 {
				// type with methods
				structs = append(structs, t)
			}
		}
	}
	return
}

func (c *Conv) sortStructs(pkg *packages.Package, ts []*types.TypeName) (structs []*types.TypeName) {
	switch pkg.PkgPath {
	case "text/template":
		for _, t := range ts {
			if t.Name() == "common" {
				structs = append([]*types.TypeName{t}, structs...) // prepend
			} else {
				structs = append(structs, t)
			}
		}
	default:
		return ts
	}
	return
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
