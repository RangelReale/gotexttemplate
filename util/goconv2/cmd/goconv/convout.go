package main

import (
	"fmt"
	"github.com/jimmyfrasche/closed"
	"go/types"
	"golang.org/x/tools/go/types/typeutil"
	"strings"
)

func (c *Conv) outputEnum(gf *GenFile, enum *closed.Enum) {
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

func (c *Conv) outputInterface(gf *GenFile, s *types.TypeName, qf types.Qualifier) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))

	basetypes := c.baseTypes(s.Type())
	baseclasses := []string{}

	for _, bt := range basetypes {
		baseclasses = append(baseclasses, c.typeName(bt, qf, false))
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

	itf := s.Type().Underlying().(*types.Interface)

	fieldAmount := 0

	for i := 0; i < itf.NumMethods(); i++ {
		f := itf.Method(i)

		c.outputFunc(gf, f, qf, true)

		//gf.Line("# %s", c.FileSet.Position(f.Pos()))
		//gf.StartLine()
		//gf.Append("def %s", c.pythonIdent(f.Name()))
		//c.outputSignature(gf, f.Type().(*types.Signature), qf, true)
		//gf.Append(":")
		//gf.Append(c.ReturnLineComment(f))
		//gf.NL()
		//
		//gf.I()
		//gf.Line("pass")
		//gf.D()

		fieldAmount++
	}

	if fieldAmount == 0 {
		gf.Line("pass")
	}
	gf.D()

}

func (c *Conv) outputStruct(gf *GenFile, s *types.TypeName, qf types.Qualifier) {
	gf.Line("# %s", c.FileSet.Position(s.Pos()))

	basetypes := c.baseTypes(s.Type())
	baseclasses := []string{}

	for _, bt := range basetypes {
		baseclasses = append(baseclasses, c.typeName(bt, qf, false))
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

	st := s.Type().Underlying().(*types.Struct)

	fieldAmount := 0

	for i := 0; i < st.NumFields(); i++ {
		f := st.Field(i)
		if f.Embedded() {
			continue
		}
		gf.StartLine()
		gf.Append("%s: ", c.pythonIdent(f.Name()))
		gf.Append(c.typeName(f.Type(), qf, true))
		gf.Append(c.ReturnLineComment(f))
		gf.NL()

		fieldAmount++
	}
	hasFieldSpc := fieldAmount == 0

	for _, meth := range typeutil.IntuitiveMethodSet(s.Type(), nil) {
		//if !meth.Obj().Exported() && !app.Private {
		//	continue // skip unexported names
		//}

		if !hasFieldSpc {
			gf.NL()
			hasFieldSpc = true
		}

		switch meth.Kind() {
		case types.MethodVal:
			c.outputFunc(gf, meth.Obj().(*types.Func), qf, true)
		case types.MethodExpr:
			c.outputFunc(gf, meth.Obj().(*types.Func), qf, true)
		default:
			panic(fmt.Sprintf("unsupported selector(%T)", meth))
		}

		//gf.Line("# %s", c.FileSet.Position(meth.Obj().Pos()))
		//gf.StartLine()
		//gf.Append("def %s", c.pythonIdent(meth.Obj().Name()))
		//switch meth.Kind() {
		//case types.MethodVal:
		//	c.outputSignature(gf, meth.Obj().(*types.Func).Type().(*types.Signature), qf, true)
		//case types.MethodExpr:
		//	c.outputSignature(gf, meth.Obj().(*types.Func).Type().(*types.Signature), qf, true)
		//default:
		//	panic(fmt.Sprintf("unsupported selector(%T)", meth))
		//}
		//gf.Append(":")
		//gf.Append(c.ReturnLineComment(meth.Obj()))
		//
		//gf.NL()
		//gf.I()
		//gf.Line("pass")
		//gf.D()

		fieldAmount++
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
	c.outputSignature(gf, s.Type().(*types.Signature), qf, self)
	gf.Append(":")
	gf.Append(c.ReturnLineComment(s))
	gf.NL()
}

func (c *Conv) outputSignature(gf *GenFile, sig *types.Signature, qf types.Qualifier, self bool) {
	gf.Append("(")
	if self {
		gf.Append("self")
		if sig.Params() != nil && sig.Params().Len() > 0 {
			gf.Append(", ")
		}
	}

	c.outputTuple(gf, sig.Params(), sig.Variadic(), qf)
	gf.Append(")")

	gf.Append(" -> ")

	n := sig.Results().Len()
	if n == 0 {
		gf.Append("None")
		// no result
		return
	}

	// multiple or named result(s)
	if n > 1 {
		gf.Append("Tuple[")
	}
	c.outputTuple(gf, sig.Results(), false, qf)
	if n > 1 {
		gf.Append("]")
	}
}

func (c *Conv) outputTuple(gf *GenFile, t *types.Tuple, variadic bool, qf types.Qualifier) {
	if t != nil {
		for i := 0; i < t.Len(); i++ {
			v := t.At(i)
			if i > 0 {
				gf.Append(", ")
			}
			if _, ok := v.Type().(*types.Slice); ok {
				gf.Append("*")
			}
			if v.Name() != "" {
				gf.Append(v.Name())
				gf.Append(": ")
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
			gf.Append(c.typeName(typ, qf, false))
		}
	}
}

func (c *Conv) typeName(typ types.Type, qf types.Qualifier, topLevel bool) string {
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
		tb.WriteString(c.typeName(t.Elem(), qf, false))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Slice:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("List[")
		tb.WriteString(c.typeName(t.Elem(), qf, false))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Struct:
		panic("TODO")
	case *types.Pointer:
		tb.WriteString("Optional[")
		tb.WriteString(c.typeName(t.Elem(), qf, false))
		tb.WriteString("]")
	case *types.Tuple:
		panic("TODO")
	case *types.Signature:
		panic("TODO")
	case *types.Interface:
		tb.WriteString("Any")
	case *types.Map:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("Dict[")
		tb.WriteString(c.typeName(t.Key(), qf, false))
		tb.WriteString(", ")
		tb.WriteString(c.typeName(t.Elem(), qf, false))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Chan:
		tb.WriteString("queue.LifoQueue")
	case *types.Named:
		s := "<Named w/o object>"
		if xobj := t.Obj(); xobj != nil {
			if xobj.Pkg() != nil {
				tb.WriteString(c.returnPackage(xobj.Pkg(), qf))
			}
			//TODO(gri): function-local named types should be displayed
			//differently from named types at package level to avoid
			//ambiguity.
			s = xobj.Name()
		}
		tb.WriteString(s)
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
		return fmt.Sprintf("%s.", s)
	}
	return ""
}

func (c *Conv) pythonIdent(ident string) string {
	if ident == "True" || ident == "False" {
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
