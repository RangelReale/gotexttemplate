package main

import (
	"fmt"
	"github.com/jimmyfrasche/closed"
	"go/types"
	"strings"
)

func (c *Conv) outputEnum(gf *GenFile, enum *closed.Enum) {
	gf.NL()
	gf.Line("# %s", c.FileSet.Position(enum.Types()[0].Pos()))
	gf.Line("class %s(Enum):", enum.Types()[0].Name())
	gf.I()

	valueAmount := 0
	if !enum.NonZero && !ContainsLabeledZero(enum) {
		//ind()
		//fmt.Println("\t0")
	}
	for _, lbl := range enum.Labels {
		valueAmount++
		gf.StartLine()
		gf.Append(labels(lbl))
		gf.Append(c.ReturnLineComment(lbl[0]))
		gf.NL()
	}

	if valueAmount == 0 {
		gf.Line("pass")
	}
	gf.D()
}

func (c *Conv) outputConst(gf *GenFile, s *types.Const, qf types.Qualifier) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))

	gf.Append("%s", s.Name())
	gf.Append(" = %s", s.Val().String())
	gf.Append(c.ReturnLineComment(s))
	gf.NL()
}

func (c *Conv) outputTypes(gf *GenFile, s *types.TypeName, qf types.Qualifier) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))

	typ := s.Type()

	gf.StartLine()
	gf.Append("%s", s.Name())
	gf.Append(" = ")
	if !s.IsAlias() {
		typ = typ.Underlying()
	}
	gf.Append(c.typeName(typ, qf, false, false))
	gf.NL()
}

func (c *Conv) outputClass(gf *GenFile, s *types.TypeName, qf types.Qualifier, closedTypes []closed.Type) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))

	basetypes := c.baseTypes(s.Type())
	baseclasses := []string{}

	//var itftypes []*types.Interface
	var itftypes []types.Type

	for _, v := range closedTypes {
		switch v := v.(type) {
		case *closed.Interface:
EndLoop:
			for _, cm := range v.Members {
				for _, cmt := range cm.TypeName {
					if s == cmt {
						for _, ct := range v.Types() {
							//baseclasses = append(baseclasses, c.typeName(ct.Type(), qf, false, true))
							//itftypes = append(itftypes, ct.Type().Underlying().(*types.Interface))
							itftypes = append(itftypes, ct.Type())
						}
						break EndLoop
					}
				}
			}
		}
	}

	for _, bt := range basetypes {
		for ifi := len(itftypes)-1; ifi >= 0; ifi-- {
			if types.Implements(types.NewPointer(bt), itftypes[ifi].Underlying().(*types.Interface)) {
				itftypes = append(itftypes[:ifi], itftypes[ifi+1:]...) // remove item
				print("YES!")
			}
		}

		btn := c.typeName(bt, qf, false, true)
		if s.Pkg().Path() == "text/template/parse" && btn == "NodeType" {
			continue
		}
		baseclasses = append(baseclasses, btn)
	}

	for _, ifi := range itftypes {
		baseclasses = append([]string{c.typeName(ifi, qf, false, true)}, baseclasses...)
	}

	base := ""
	if len(baseclasses) > 0 {
		base = fmt.Sprintf("(%s)", strings.Join(baseclasses, ", "))
	}

	gf.StartLine()
	gf.Append("class %s%s:", s.Name(), base)
	gf.Append(c.ReturnLineComment(s))
	gf.NL()

	gf.I()

	fieldAmount := 0

	// Fields
	switch sx := s.Type().(type) {
	case *types.Named:
		switch st := sx.Underlying().(type) {
		case *types.Struct:
			for i := 0; i < st.NumFields(); i++ {
				f := st.Field(i)
				if f.Embedded() {
					continue
				}
				gf.StartLine()
				gf.Append("%s: ", c.pythonIdent(f.Name()))
				gf.Append(c.typeName(f.Type(), qf, true, false))
				gf.Append(c.ReturnLineComment(f))
				gf.NL()

				fieldAmount++
			}
		}
	}

	//hasFieldSpc := fieldAmount == 0

	// Methods
	switch sx := s.Type().(type) {
	case *types.Named:
		switch st := sx.Underlying().(type) {
		case *types.Interface:
			for i := 0; i < st.NumExplicitMethods(); i++ {
				gf.NL()
				//if !hasFieldSpc {
				//	gf.NL()
				//	hasFieldSpc = true
				//}

				f := st.ExplicitMethod(i)
				c.outputFunc(gf, f, qf, true)
				fieldAmount++
			}
		default:
			for i := 0; i < sx.NumMethods(); i++ {
				gf.NL()
				//if !hasFieldSpc {
				//	gf.NL()
				//	hasFieldSpc = true
				//}

				f := sx.Method(i)
				c.outputFunc(gf, f, qf, true)
				fieldAmount++
			}
		}
	}

	if fieldAmount == 0 {
		gf.Line("pass")
	}
	gf.D()
}

func (c *Conv) outputFunc(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) {
	c.outputFuncSig(gf, s, qf, self)

	gf.I()
	gf.Line("pass")
	gf.D()
}

func (c *Conv) outputFuncSig(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))
	gf.StartLine()
	gf.Append("def %s", c.pythonIdent(s.Name()))
	gf.Append(c.returnSignature(s.Type().(*types.Signature), qf, self))
	gf.Append(":")
	gf.Append(c.ReturnLineComment(s))
	gf.NL()
}

func (c *Conv) returnSignature(sig *types.Signature, qf types.Qualifier, self bool) string {
	var sb strings.Builder

	sb.WriteString("(")
	if self {
		sb.WriteString("self")
		if sig.Params() != nil && sig.Params().Len() > 0 {
			sb.WriteString(", ")
		}
	}

	sb.WriteString(c.returnTuple(sig.Params(), sig.Variadic(), qf, true))
	sb.WriteString(")")

	sb.WriteString(" -> ")

	n := sig.Results().Len()
	if n == 0 {
		sb.WriteString("None")
		// no result
		return sb.String()
	}

	// multiple or named result(s)
	if n > 1 {
		sb.WriteString("Tuple[")
	}
	sb.WriteString(c.returnTuple(sig.Results(), false, qf, false))
	if n > 1 {
		sb.WriteString("]")
	}
	return sb.String()
}

func (c *Conv) returnSignatureType(sig *types.Signature, qf types.Qualifier) string {
	var sb strings.Builder

	sb.WriteString("Callable[[")
	sb.WriteString(c.returnTuple(sig.Params(), sig.Variadic(), qf, false))
	sb.WriteString("], ")

	n := sig.Results().Len()
	if n == 0 {
		sb.WriteString("None")
		// no result
		return sb.String()
	} else {
		// multiple or named result(s)
		if n > 1 {
			sb.WriteString("Tuple[")
		}
		sb.WriteString(c.returnTuple(sig.Results(), false, qf, false))
		if n > 1 {
			sb.WriteString("]")
		}
	}

	sb.WriteString("]")

	return sb.String()
}

func (c *Conv) returnTuple(t *types.Tuple, variadic bool, qf types.Qualifier, named bool) string {
	var sb strings.Builder

	if t != nil {
		for i := 0; i < t.Len(); i++ {
			v := t.At(i)
			if i > 0 {
				sb.WriteString(", ")
			}
			if variadic && i == t.Len()-1 {
				if _, ok := v.Type().(*types.Slice); ok {
					sb.WriteString("*")
				}
			}
			if named {
				if v.Name() != "" {
					sb.WriteString(c.pythonIdent(v.Name()))
				} else {
					sb.WriteString(fmt.Sprintf("p%d", i))
				}
				sb.WriteString(": ")
			}
			typ := v.Type()
			if variadic && i == t.Len()-1 {
				if s, ok := typ.(*types.Slice); ok {
					//gf.Append("*")
					typ = s.Elem()
				} else {
					panic(fmt.Sprintf("Unuspported variadic type: %T", typ))
					//// special case:
					//// append(s, "foo"...) leads to signature func([]byte, string...)
					//if t, ok := typ.Underlying().(*types.Basic); !ok || t.Kind() != types.String {
					//	panic("internal error: string type expected")
					//}
					//gf.Append("**")
					//gf.Append(c.typeName(typ, qf, false))
					//continue
				}
			}
			sb.WriteString(c.typeName(typ, qf, false, false))
		}
	}
	return sb.String()
}

func (c *Conv) typeName(typ types.Type, qf types.Qualifier, topLevel bool, typeDecl bool) string {
	var tb strings.Builder

	switch t := typ.(type) {
	case nil:
		tb.WriteString("None")
	case *types.Basic:
		tb.WriteString(c.pythonType(t))
	case *types.Array:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("List[")
		tb.WriteString(c.typeName(t.Elem(), qf, false, typeDecl))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Slice:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("List[")
		tb.WriteString(c.typeName(t.Elem(), qf, false, typeDecl))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Struct:
		panic("TODO")
	case *types.Pointer:
		if !typeDecl {
			tb.WriteString("Optional[")
		}
		tb.WriteString(c.typeName(t.Elem(), qf, false, typeDecl))
		if !typeDecl {
			tb.WriteString("]")
		}
	case *types.Tuple:
		panic("TODO")
	case *types.Signature:
		tb.WriteString(c.returnSignatureType(t, qf))
	case *types.Interface:
		tb.WriteString("Any")
	case *types.Map:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("Dict[")
		tb.WriteString(c.typeName(t.Key(), qf, false, typeDecl))
		tb.WriteString(", ")
		tb.WriteString(c.typeName(t.Elem(), qf, false, typeDecl))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Chan:
		tb.WriteString("queue.LifoQueue")
	case *types.Named:
		s := "<Named w/o object>"
		pkg := ""
		if xobj := t.Obj(); xobj != nil {
			if xobj.Pkg() != nil {
				pkg = c.returnPackage(xobj.Pkg(), qf)
				tb.WriteString(pkg)
			}
			//TODO(gri): function-local named types should be displayed
			//differently from named types at package level to avoid
			//ambiguity.
			s = xobj.Name()
		}
		if pkg == "" && !typeDecl {
			tb.WriteString("'")
		}
		if s == "error" && t.Obj().Pkg() == nil {
			tb.WriteString("goext.error")
		} else {
			tb.WriteString(s)
		}
		if pkg == "" && !typeDecl {
			tb.WriteString("'")
		}
	default:
		panic("TODO")
	}

	return tb.String()
}

func (c *Conv) returnPackage(pkg *types.Package, qf types.Qualifier) string {
	if pkg == nil {
		return ""
	}
	var s string
	if qf != nil {
		s = qf(pkg)
	} else {
		s = pkg.Path()
	}
	if s != "" {
		if c.isExternalImport(pkg) {
			return fmt.Sprintf("goext.%s_", strings.Replace(s, "/", "_", -1))
		} else {
			return fmt.Sprintf("%s.", strings.Replace(s, "/", "_", -1))
		}
	}
	return ""
}

func (c *Conv) pythonIdent(ident string) string {
	switch ident {
	case "True", "False", "in", "or", "not", "and":
		return fmt.Sprintf("%s_", ident)
	}

	return ident
}

func (c *Conv) pythonType(ptype *types.Basic) string {
	switch ptype.Kind() {
	case types.UntypedBool, types.Bool:
		return "bool"
	case types.UntypedInt, types.Int, types.Int8, types.Int16, types.Int32, types.Int64, types.Uint, types.Uint8,
		types.Uint16, types.Uint32, types.Uint64:
		return "int"
	case types.Uintptr:
		return "Optional[int]"
	case types.UntypedFloat, types.Float32, types.Float64:
		return "float"
	case types.UntypedComplex, types.Complex64, types.Complex128:
		return "complex"
	case types.UntypedString, types.UntypedRune, types.String:
		return "str"
	case types.UntypedNil:
		return "None"
	case types.Invalid, types.UnsafePointer:
		return "Optional[Any]"
	}

	return ptype.Name()
}
