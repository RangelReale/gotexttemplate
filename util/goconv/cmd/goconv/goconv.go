package main

import (
	"flag"
	"fmt"
	"go/ast"
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

	p := &Processor{
		Packages:   pkgs,
		Fset:       fset,
		OutputPath: outputPath,
	}

	p.process()
}

type GenFile struct {
	pb     strings.Builder
	indent int
}

func NewGenFile() *GenFile {
	return &GenFile{}
}

func (g *GenFile) Append(format string, args ...interface{}) {
	_, err := fmt.Fprintf(&g.pb, format, args...)
	if err != nil {
		panic(err)
	}
}

func (g *GenFile) StartLine() {
	if g.indent > 0 {
		g.Append(strings.Repeat("    ", g.indent))
	}
}

func (g *GenFile) Line(format string, args ...interface{}) {
	g.StartLine()
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

type Processor struct {
	Packages   []*packages.Package
	Fset       *token.FileSet
	OutputPath string
}

func (p *Processor) process() {
	if packages.PrintErrors(p.Packages) > 0 {
		os.Exit(1)
	}

	for _, pkg := range p.Packages {
		p.processPackage(pkg)
	}
}

func (p *Processor) processPackage(pkg *packages.Package) {
	gf := NewGenFile()

	gf.Line("# package: %s", pkg.PkgPath)
	gf.NL()

	if pkg.Types != nil {
		qual := types.RelativeTo(pkg.Types)
		scope := pkg.Types.Scope()
		for _, name := range scope.Names() {
			obj := scope.Lookup(name)

			p.WriteObject(gf, obj, qual)

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

	gf.WriteFile(filepath.Join(p.OutputPath, fmt.Sprintf("%s.py", pkg.Name)))
}

func (p *Processor) WriteObject(gf *GenFile, obj types.Object, qf types.Qualifier) {
	var tname *types.TypeName
	typ := obj.Type()

	gf.Line("# %s", p.Fset.Position(obj.Pos()))

	switch tobj := obj.(type) {
	case *types.PkgName:
		//fmt.Fprintf(buf, "package %s", tobj.Name())
		//if path := tobj.imported.path; path != "" && path != tobj.name {
		//	fmt.Fprintf(buf, " (%q)", path)
		//}
		return

	case *types.Const:
		gf.Append("const")
		//buf.WriteString("const")

	case *types.TypeName:
		tname = tobj
		gf.Append("type")
		//buf.WriteString("type")

	case *types.Var:
		if tobj.IsField() {
			gf.Append("field")
		} else {
			gf.Append("var")
		}

		//if tobj.isField {
		//	buf.WriteString("field")
		//} else {
		//	buf.WriteString("var")
		//}

	case *types.Func:
		gf.Append("def ")
		gf.Append(tobj.Name())

		gf.Line(":")
		gf.I()
		gf.Line("pass")
		gf.D()
		gf.NL()
		//writeFuncName(buf, tobj, qf)
		//if typ != nil {
		//	WriteSignature(buf, typ.(*Signature), qf)
		//}

		//buf.WriteString("func ")
		//writeFuncName(buf, tobj, qf)
		//if typ != nil {
		//	WriteSignature(buf, typ.(*Signature), qf)
		//}
		return

	case *types.Label:
		gf.Append("label")
		//buf.WriteString("label")
		typ = nil

	case *types.Builtin:
		gf.Append("builtin")
		//buf.WriteString("builtin")
		typ = nil

	case *types.Nil:
		gf.Append("nil")
		//buf.WriteString("nil")
		return

	default:
		panic(fmt.Sprintf("writeObject(%T)", tobj))
	}

	gf.Append(" ")
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
	p.WriteType(gf, obj, typ, qf)
	gf.NL()
}

func (p *Processor) WriteType(gf *GenFile, obj types.Object, typ types.Type, qf types.Qualifier) {
	p.writeType(gf, obj, typ, qf, make([]types.Type, 0, 8))
}

func (p *Processor) writeType(gf *GenFile, obj types.Object, typ types.Type, qf types.Qualifier, visited []types.Type) {
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
		if t.Kind() == types.UnsafePointer {
			//buf.WriteString("unsafe.")
		}
		gf.Append(t.Name())

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
		if obj != nil {
			gf.Append("Optional[")
		}
		gf.Append("List[")
		p.writeType(gf, nil, t.Elem(), qf, visited)
		gf.Append("]")
		if obj != nil {
			gf.Append("]")
		}

		//fmt.Fprintf(buf, "[%d]", t.len)
		//writeType(buf, t.elem, qf, visited)

	case *types.Slice:
		if obj != nil {
			gf.Append("Optional[")
		}
		gf.Append("List[")
		p.writeType(gf, nil, t.Elem(), qf, visited)
		gf.Append("]")
		if obj != nil {
			gf.Append("]")
		}

		//buf.WriteString("[]")
		//writeType(buf, t.elem, qf, visited)

	case *types.Struct:
		if obj == nil {
			panic("obj is nil")
		}

		gf.Line("class %s:", obj.Name())
		gf.I()
		gf.Line(`""""`)
		gf.Line("Source: %s", p.Fset.Position(obj.Pos()))
		gf.Line(`""""`)
		for i := 0; i < t.NumFields(); i++ {
			f := t.Field(i)
			fast := p.AstOf(f)
			gf.StartLine()
			gf.Append("%s: ", f.Name())
			p.writeType(gf, obj, f.Type(), qf, visited)
			if fast != nil {
				switch xfast := fast.(type) {
				case *ast.Field:
					if xfast.Comment != nil && len(xfast.Comment.List) > 0 {
						gf.Append("  # %s", strings.TrimLeft(xfast.Comment.List[0].Text, "/ "))
					}
				}
			}
			gf.NL()
		}
		if t.NumFields() == 0 {
			gf.Line("pass")
		}
		gf.D()

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
		gf.Append("Optional[")
		p.writeType(gf, nil, t.Elem(), qf, visited)
		gf.Append("]")

		//buf.WriteByte('*')
		//writeType(buf, t.base, qf, visited)

	case *types.Tuple:
		//writeTuple(buf, t, false, qf, visited)

	case *types.Signature:
		//buf.WriteString("func")
		//writeSignature(buf, t, qf, visited)

	case *types.Interface:
		gf.Append("Any")

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
		if obj != nil {
			gf.Append("Optional[")
		}
		gf.Append("Dict[")
		p.writeType(gf, nil, t.Key(), qf, visited)
		gf.Append(", ")
		p.writeType(gf, nil, t.Elem(), qf, visited)
		gf.Append("]")
		if obj != nil {
			gf.Append("]")
		}

		//buf.WriteString("map[")
		//writeType(buf, t.key, qf, visited)
		//buf.WriteByte(']')
		//writeType(buf, t.elem, qf, visited)

	case *types.Chan:
		gf.Append("UNSUPPORTED_CHAN")

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
		}
		gf.Append(s)

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

type Poser interface {
	Pos() token.Pos
}

func (p *Processor) FileOf(poser Poser) *ast.File {
	for _, pkg := range p.Packages {
		for _, file := range pkg.Syntax {
			if file.Pos() <= poser.Pos() && file.End() > poser.Pos() {
				return file
			}
		}
	}
	return nil
}

func (p *Processor) AstOf(typeFunc types.Object) (typeAst ast.Node) {
	ast.Inspect(p.FileOf(typeFunc), func(node ast.Node) bool {
		if node == nil {
			return true
		}

		switch node.(type) {
		case *ast.File:
			// ignore
		default:
			if node.Pos() == typeFunc.Pos() {
				//fmt.Printf("@@ OK! %d-%d || %d \n", node.Pos(), node.End(), typeFunc.Pos())
				typeAst = node
				return false
			}
		}
		return true
	})
	return
}
