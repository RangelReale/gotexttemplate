package main

import (
	"fmt"
	"github.com/jimmyfrasche/closed"
	"go/types"
	"strings"
)

func (cf *ConvFile) outputEnum(gf *GenFile, enum *closed.Enum) {
	gf.NL()
	gf.Line("# %s", cf.Conv.FileSet.Position(enum.Types()[0].Pos()))
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
		gf.Append(cf.Conv.ReturnLineComment(lbl[0]))
		gf.NL()
	}

	if valueAmount == 0 {
		gf.Line("pass")
	}
	gf.D()
}

func (cf *ConvFile) outputConst(gf *GenFile, s *types.Const, qf types.Qualifier) {
	gf.Line("# %s", cf.Conv.FileSet.Position(s.Pos()))

	gf.Append("%s", s.Name())
	gf.Append(" = %s", s.Val().String())
	gf.Append(cf.Conv.ReturnLineComment(s))
	gf.NL()
}

func (cf *ConvFile) outputTypes(gf *GenFile, s *types.TypeName, qf types.Qualifier) {
	gf.Line("# %s", cf.Conv.FileSet.Position(s.Pos()))

	typ := s.Type()

	gf.StartLine()
	gf.Append("%s", s.Name())
	gf.Append(" = ")
	if !s.IsAlias() {
		typ = typ.Underlying()
	}
	gf.Append(cf.typeName(typ, qf, false, false))
	gf.NL()
}

func (cf *ConvFile) outputClass(gf *GenFile, s *types.TypeName, qf types.Qualifier) {
	gf.Line("# %s", cf.Conv.FileSet.Position(s.Pos()))

	basetypes := cf.baseTypesFiltered(s, cf.closedTypes)
	baseclasses := []string{}

	for _, bt := range basetypes {
		btn := cf.typeName(bt, qf, false, true)
		if s.Pkg().Path() == "text/template/parse" && btn == "NodeType" {
			continue
		}
		baseclasses = append(baseclasses, btn)
	}

	base := ""
	if len(baseclasses) > 0 {
		base = fmt.Sprintf("(%s)", strings.Join(baseclasses, ", "))
	}

	gf.StartLine()
	gf.Append("class %s%s:", s.Name(), base)
	gf.Append(cf.Conv.ReturnLineComment(s))
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
				gf.Append("%s: ", cf.pythonIdent(f.Name()))
				gf.Append(cf.typeName(f.Type(), qf, true, false))
				gf.Append(cf.Conv.ReturnLineComment(f))
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
				cf.outputFunc(gf, f, qf, true)
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
				cf.outputFunc(gf, f, qf, true)
				fieldAmount++
			}
		}
	}

	if fieldAmount == 0 {
		gf.Line("pass")
	}
	gf.D()
}

func (cf *ConvFile) outputFunc(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) {
	cf.outputFuncSig(gf, s, qf, self)

	gf.I()
	gf.Line("pass")
	gf.D()
}

func (cf *ConvFile) outputFuncSig(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) {
	gf.Line("# %s", cf.Conv.FileSet.Position(s.Pos()))
	gf.StartLine()
	gf.Append("def %s", cf.pythonIdent(s.Name()))
	gf.Append(cf.returnSignature(s.Type().(*types.Signature), qf, self))
	gf.Append(":")
	gf.Append(cf.Conv.ReturnLineComment(s))
	gf.NL()
}

func (cf *ConvFile) returnSignature(sig *types.Signature, qf types.Qualifier, self bool) string {
	var sb strings.Builder

	sb.WriteString("(")
	if self {
		sb.WriteString("self")
		if sig.Params() != nil && sig.Params().Len() > 0 {
			sb.WriteString(", ")
		}
	}

	sb.WriteString(cf.returnTuple(sig.Params(), sig.Variadic(), qf, true))
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
	sb.WriteString(cf.returnTuple(sig.Results(), false, qf, false))
	if n > 1 {
		sb.WriteString("]")
	}
	return sb.String()
}

func (cf *ConvFile) returnSignatureType(sig *types.Signature, qf types.Qualifier) string {
	var sb strings.Builder

	sb.WriteString("Callable[[")
	sb.WriteString(cf.returnTuple(sig.Params(), sig.Variadic(), qf, false))
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
		sb.WriteString(cf.returnTuple(sig.Results(), false, qf, false))
		if n > 1 {
			sb.WriteString("]")
		}
	}

	sb.WriteString("]")

	return sb.String()
}

func (cf *ConvFile) returnTuple(t *types.Tuple, variadic bool, qf types.Qualifier, named bool) string {
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
					sb.WriteString(cf.pythonIdent(v.Name()))
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
			sb.WriteString(cf.typeName(typ, qf, false, false))
		}
	}
	return sb.String()
}

func (cf *ConvFile) typeName(typ types.Type, qf types.Qualifier, topLevel bool, typeDecl bool) string {
	var tb strings.Builder

	switch t := typ.(type) {
	case nil:
		tb.WriteString("None")
	case *types.Basic:
		tb.WriteString(cf.pythonType(t))
	case *types.Array:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("List[")
		tb.WriteString(cf.typeName(t.Elem(), qf, false, typeDecl))
		tb.WriteString("]")
		if topLevel {
			tb.WriteString("]")
		}
	case *types.Slice:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("List[")
		tb.WriteString(cf.typeName(t.Elem(), qf, false, typeDecl))
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
		tb.WriteString(cf.typeName(t.Elem(), qf, false, typeDecl))
		if !typeDecl {
			tb.WriteString("]")
		}
	case *types.Tuple:
		panic("TODO")
	case *types.Signature:
		tb.WriteString(cf.returnSignatureType(t, qf))
	case *types.Interface:
		tb.WriteString("Any")
	case *types.Map:
		if topLevel {
			tb.WriteString("Optional[")
		}
		tb.WriteString("Dict[")
		tb.WriteString(cf.typeName(t.Key(), qf, false, typeDecl))
		tb.WriteString(", ")
		tb.WriteString(cf.typeName(t.Elem(), qf, false, typeDecl))
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
				pkg = cf.returnPackage(xobj.Pkg(), qf)
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

func (cf *ConvFile) returnPackage(pkg *types.Package, qf types.Qualifier) string {
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
		if cf.Conv.isExternalImport(pkg) {
			return fmt.Sprintf("goext.%s_", strings.Replace(s, "/", "_", -1))
		} else {
			return fmt.Sprintf("%s.", strings.Replace(s, "/", "_", -1))
		}
	}
	return ""
}

func (cf *ConvFile) pythonIdent(ident string) string {
	switch ident {
	case "True", "False", "in", "or", "not", "and":
		return fmt.Sprintf("%s_", ident)
	}

	return ident
}

func (cf *ConvFile) pythonType(ptype *types.Basic) string {
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
