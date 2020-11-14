package main

import (
	"flag"
	"fmt"
	"go/token"
	"go/types"
	"golang.org/x/tools/go/packages"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	realmain()
}

func realmain() {
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

	flag.Parse()
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	outputPath := filepath.Clean(flag.Arg(0))

	fmt.Printf("Output path: %s...\n", outputPath)

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
		processPackage(pkg, fset, outputPath)
	}
}

type GenFile struct {
	Fset   *token.FileSet
	pb     strings.Builder
	indent int
}

func NewGenFile(fset *token.FileSet) *GenFile {
	return &GenFile{
		Fset: fset,
	}
}

func (g *GenFile) Append(format string, args ...interface{}) {
	_, err := fmt.Fprintf(&g.pb, format, args...)
	if err != nil {
		panic(err)
	}
}

func (g *GenFile) Line(format string, args ...interface{}) {
	if g.indent > 0 {
		g.Append(strings.Repeat("    ", g.indent))
	}
	g.Append(format, args...)
	g.Append("\n")
}

func (g *GenFile) NL() {
	g.Append("\n")
}

func (g *GenFile) I() {
	g.indent++
}

func (g *GenFile) D() {
	g.indent--
}

func (g *GenFile) WriteFile(filename string) {
	err := ioutil.WriteFile(filename, []byte(g.pb.String()), 0644)
	if err != nil {
		panic(err)
	}
}

func processPackage(pkg *packages.Package, fset *token.FileSet, outputPath string) {
	gf := NewGenFile(fset)

	gf.Line("# package: %s", pkg.PkgPath)
	gf.NL()

	if pkg.Types != nil {
		qual := types.RelativeTo(pkg.Types)
		scope := pkg.Types.Scope()
		for _, name := range scope.Names() {
			obj := scope.Lookup(name)

			WriteObject(gf, obj, qual)

			//scount := -1
			//
			//fmt.Printf("\t%s\n", types.ObjectString(obj, qual))
			//
			//var tname *types.TypeName
			//typ := obj.Type()
			//
			//switch obj := obj.(type) {
			//case *types.TypeName:
			//	tname = obj
			//}
			//
			//case *types.Struct:
			//	gf.Line("class %s:", obj.Name())
			//	gf.I()
			//	scount = 0
			//
			//	if scount == 0 {
			//		gf.Line("pass")
			//	}
			//	gf.D()
			//	gf.NL()
			//}

			//if _, ok := obj.(*types.TypeName); ok {
			//	for _, meth := range typeutil.IntuitiveMethodSet(obj.Type(), nil) {
			//		if meth.Kind() == types.MethodExpr {
			//			scount++
			//		}
			//		gf.Line("def %s():", meth.Obj().Name())
			//		gf.I()
			//		gf.Line("pass")
			//		gf.D()
			//
			//		//fmt.Printf("\t%s\n", types.SelectionString(meth, qual))
			//	}
			//}
		}
	}

	gf.WriteFile(filepath.Join(outputPath, fmt.Sprintf("%s.py", pkg.Name)))
}

func WriteObject(gf *GenFile, obj types.Object, qf types.Qualifier) {
	var tname *types.TypeName
	typ := obj.Type()

	switch tobj := obj.(type) {
	case *types.PkgName:
		//fmt.Fprintf(buf, "package %s", tobj.Name())
		//if path := tobj.imported.path; path != "" && path != tobj.name {
		//	fmt.Fprintf(buf, " (%q)", path)
		//}
		return

	case *types.Const:
		//buf.WriteString("const")

	case *types.TypeName:
		tname = tobj
		//buf.WriteString("type")

	case *types.Var:
		//if tobj.isField {
		//	buf.WriteString("field")
		//} else {
		//	buf.WriteString("var")
		//}

	case *types.Func:
		//buf.WriteString("func ")
		//writeFuncName(buf, tobj, qf)
		//if typ != nil {
		//	WriteSignature(buf, typ.(*Signature), qf)
		//}
		return

	case *types.Label:
		//buf.WriteString("label")
		typ = nil

	case *types.Builtin:
		//buf.WriteString("builtin")
		typ = nil

	case *types.Nil:
		//buf.WriteString("nil")
		return

	default:
		panic(fmt.Sprintf("writeObject(%T)", tobj))
	}

	//buf.WriteByte(' ')

	// For package-level objects, qualify the name.
	//if tobj.Pkg() != nil && tobj.Pkg().scope.Lookup(tobj.Name()) == tobj {
	//	writePackage(buf, tobj.Pkg(), qf)
	//}
	//buf.WriteString(tobj.Name())

	if typ == nil {
		return
	}

	if tname != nil {
		// We have a type object: Don't print anything more for
		// basic types since there's no more information (names
		// are the same; see also comment in TypeName.IsAlias).
		//if _, ok := typ.(*types.Basic); ok {
		//	return
		//}
		if tname.IsAlias() {
			//buf.WriteString(" =")
		} else {
			typ = typ.Underlying()
		}
	}

	//buf.WriteByte(' ')
	WriteType(gf, obj, typ, qf)
}

func WriteType(gf *GenFile, obj types.Object, typ types.Type, qf types.Qualifier) {
	writeType(gf, obj, typ, qf, make([]types.Type, 0, 8))
}

func writeType(gf *GenFile, obj types.Object, typ types.Type, qf types.Qualifier, visited []types.Type) {
	// Theoretically, this is a quadratic lookup algorithm, but in
	// practice deeply nested composite types with unnamed component
	// types are uncommon. This code is likely more efficient than
	// using a map.
	//for _, t := range visited {
	//	if t == typ {
	//		fmt.Fprintf(buf, "○%T", typ) // cycle to typ
	//		return
	//	}
	//}
	visited = append(visited, typ)

	switch t := typ.(type) {
	case nil:
		//buf.WriteString("<nil>")

	case *types.Basic:
		//if t.kind == UnsafePointer {
		//	buf.WriteString("unsafe.")
		//}
		//if gcCompatibilityMode {
		//	// forget the alias names
		//	switch t.kind {
		//	case Byte:
		//		t = Typ[Uint8]
		//	case Rune:
		//		t = Typ[Int32]
		//	}
		//}
		//buf.WriteString(t.name)

	case *types.Array:
		//fmt.Fprintf(buf, "[%d]", t.len)
		//writeType(buf, t.elem, qf, visited)

	case *types.Slice:
		//buf.WriteString("[]")
		//writeType(buf, t.elem, qf, visited)

	case *types.Struct:
		if obj == nil {
			panic("obj is nil")
		}

		gf.Line("class %s:", obj.Name())
		gf.I()
		gf.Line(`""""`)
		gf.Line("Source: %s", gf.Fset.Position(obj.Pos()))
		gf.Line(`""""`)
		for i := 0; i < t.NumFields(); i++ {
			f := t.Field(i)
			writeType(gf, obj, f.Type(), qf, visited)
		}
		gf.Line("pass")
		gf.D()
		gf.NL()

		//buf.WriteString("struct{")
		//for i, f := range t.fields {
		//	if i > 0 {
		//		buf.WriteString("; ")
		//	}
		//	if !f.embedded {
		//		buf.WriteString(f.name)
		//		buf.WriteByte(' ')
		//	}
		//	writeType(buf, f.typ, qf, visited)
		//	if tag := t.Tag(i); tag != "" {
		//		fmt.Fprintf(buf, " %q", tag)
		//	}
		//}
		//buf.WriteByte('}')

	case *types.Pointer:
		//buf.WriteByte('*')
		//writeType(buf, t.base, qf, visited)

	case *types.Tuple:
		//writeTuple(buf, t, false, qf, visited)

	case *types.Signature:
		//buf.WriteString("func")
		//writeSignature(buf, t, qf, visited)

	case *types.Interface:
		// We write the source-level methods and embedded types rather
		// than the actual method set since resolved method signatures
		// may have non-printable cycles if parameters have embedded
		// interface types that (directly or indirectly) embed the
		// current interface. For instance, consider the result type
		// of m:
		//
		//     type T interface{
		//         m() interface{ T }
		//     }
		//

		//buf.WriteString("interface{")
		//empty := true
		//if gcCompatibilityMode {
		//	// print flattened interface
		//	// (useful to compare against gc-generated interfaces)
		//	for i, m := range t.allMethods {
		//		if i > 0 {
		//			buf.WriteString("; ")
		//		}
		//		buf.WriteString(m.name)
		//		writeSignature(buf, m.typ.(*Signature), qf, visited)
		//		empty = false
		//	}
		//} else {
		//	// print explicit interface methods and embedded types
		//	for i, m := range t.methods {
		//		if i > 0 {
		//			buf.WriteString("; ")
		//		}
		//		buf.WriteString(m.name)
		//		writeSignature(buf, m.typ.(*Signature), qf, visited)
		//		empty = false
		//	}
		//	for i, typ := range t.embeddeds {
		//		if i > 0 || len(t.methods) > 0 {
		//			buf.WriteString("; ")
		//		}
		//		writeType(buf, typ, qf, visited)
		//		empty = false
		//	}
		//}
		//if t.allMethods == nil || len(t.methods) > len(t.allMethods) {
		//	if !empty {
		//		buf.WriteByte(' ')
		//	}
		//	buf.WriteString("/* incomplete */")
		//}
		//buf.WriteByte('}')

	case *types.Map:
		//buf.WriteString("map[")
		//writeType(buf, t.key, qf, visited)
		//buf.WriteByte(']')
		//writeType(buf, t.elem, qf, visited)

	case *types.Chan:
		//var s string
		//var parens bool
		//switch t.dir {
		//case SendRecv:
		//	s = "chan "
		//	// chan (<-chan T) requires parentheses
		//	if c, _ := t.elem.(*Chan); c != nil && c.dir == RecvOnly {
		//		parens = true
		//	}
		//case SendOnly:
		//	s = "chan<- "
		//case RecvOnly:
		//	s = "<-chan "
		//default:
		//	panic("unreachable")
		//}
		//buf.WriteString(s)
		//if parens {
		//	buf.WriteByte('(')
		//}
		//writeType(buf, t.elem, qf, visited)
		//if parens {
		//	buf.WriteByte(')')
		//}

	case *types.Named:
		s := "<Named w/o object>"
		if xobj := t.Obj(); xobj != nil {
			//if xobj.Pkg() != nil {
			//	writePackage(buf, obj.pkg, qf)
			//}
			// TODO(gri): function-local named types should be displayed
			// differently from named types at package level to avoid
			// ambiguity.
			s = xobj.Name()
			gf.Line("# Source: %s", gf.Fset.Position(xobj.Pos()))
		}
		gf.Line(s)

		//s := "<Named w/o object>"
		//if obj := t.obj; obj != nil {
		//	if obj.pkg != nil {
		//		writePackage(buf, obj.pkg, qf)
		//	}
		//	// TODO(gri): function-local named types should be displayed
		//	// differently from named types at package level to avoid
		//	// ambiguity.
		//	s = obj.name
		//}
		//buf.WriteString(s)

	default:
		// For externally defined implementations of Type.
		//buf.WriteString(t.String())
	}
}
