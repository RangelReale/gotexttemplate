package main

import (
	"fmt"
	"go/ast"
	"go/token"
	"go/types"
	"sort"
	"strings"

	"golang.org/x/tools/go/ast/astutil"
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

func (c *Conv) findTypes(ts []*types.TypeName) []*types.TypeName {
	var rt []*types.TypeName

	for _, t := range ts {
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Struct:
			case *types.Interface:
			default:
				rt = append(rt, t)
			}
		} else {
			rt = append(rt, t)
		}
	}

	return c.sortTypes(rt)
}

func (c *Conv) findInterfaces(ts []*types.TypeName) []*types.TypeName {
	var rt []*types.TypeName

	for _, t := range ts {
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Interface:
				rt = append(rt, t)
			}
		}
	}

	return c.sortTypes(rt)
}

func (c *Conv) findStructs(ts []*types.TypeName) []*types.TypeName {
	var rt []*types.TypeName

	for _, t := range ts {
		found := false
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Struct:
				rt = append(rt, t)
				found = true
			case *types.Interface:
				found = true
			}
		}

		if !found {
			imset := typeutil.IntuitiveMethodSet(t.Type(), nil)
			if len(imset) > 0 {
				// type with methods
				rt = append(rt, t)
			}
		}
	}

	return c.sortTypes(rt)
}

func (c *Conv) sortStructs(pkg *packages.Package, ts []*types.TypeName) []*types.TypeName {
	var prt []*types.TypeName
	var rt []*types.TypeName

	switch pkg.PkgPath {
	case "text/template":
		for _, t := range ts {
			if t.Name() == "common" {
				prt = append(prt, t)
				//structs = append([]*types.TypeName{t}, structs...) // prepend
			} else {
				rt = append(rt, t)
				//structs = append(structs, t)
			}
		}
	case "text/template/parse":
		for _, t := range ts {
			if t.Name() == "Pos" {
				prt = append(prt, t)
				//structs = append([]*types.TypeName{t}, structs...) // prepend
			} else {
				rt = append(rt, t)
				//structs = append(structs, t)
			}
		}
	default:
		return ts
	}

	return append(prt, c.sortTypes(rt)...)
}

func (c *Conv) sortTypes(ts []*types.TypeName) []*types.TypeName {
	var ret []*types.TypeName

	rts := map[string]*types.TypeName{}
	for _, t := range ts {
		rts[t.Name()] = t
	}

	keys := make([]string, 0, len(rts))
	for k := range rts {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, k := range keys {
		ret = append(ret, rts[k])
	}

	return ret
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
	for _, fast := range c.AstOf(typeObj) {
		switch xfast := fast.(type) {
		case *ast.ImportSpec:
			if xfast.Comment != nil {
				return c.ReturnComments(xfast.Comment, false)
			}
		case *ast.Field:
			if xfast.Comment != nil {
				return c.ReturnComments(xfast.Comment, false)
			}
		case *ast.ValueSpec:
			if xfast.Comment != nil {
				return c.ReturnComments(xfast.Comment, false)
			}
		case *ast.TypeSpec:
			if xfast.Comment != nil {
				return c.ReturnComments(xfast.Comment, false)
			}
		}
	}

	return ""
}

func (c *Conv) ReturnLineDoc(typeObj types.Object) string {
	for _, fast := range c.AstOf(typeObj) {
		switch xfast := fast.(type) {
		case *ast.ImportSpec:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		case *ast.Field:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		case *ast.ValueSpec:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		case *ast.TypeSpec:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		case *ast.GenDecl:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		case *ast.FuncDecl:
			if xfast.Doc != nil {
				return c.ReturnComments(xfast.Doc, true)
			}
		}
	}

	return ""
}

func (c *Conv) ReturnComments(comment *ast.CommentGroup, multiline bool) string {
	if comment != nil && len(comment.List) > 0 {
		var cb strings.Builder
		if multiline {
			cb.WriteString("\"\"\"\n")
		}
		for slinect, sline := range strings.Split(comment.Text(), "\n") {
			if multiline {
				if slinect > 0 {
					cb.WriteString("\n")
				}
				//cb.WriteString("# ")
			} else {
				if slinect == 0 {
					cb.WriteString("  # ")
				} else {
					cb.WriteString(" ")
				}
			}
			cb.WriteString(sline)
		}
		if multiline {
			cb.WriteString("\"\"\"")
		}
		return cb.String()
	}
	return ""
}

func (c *Conv) AstOf(typeObj types.Object) []ast.Node {
	r, _ := astutil.PathEnclosingInterval(c.FileOf(typeObj), typeObj.Pos(), typeObj.Pos())
	return r
}
