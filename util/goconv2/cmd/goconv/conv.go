package main

import (
	"fmt"
	"github.com/hashicorp/go-multierror"
	"github.com/jimmyfrasche/closed"
	"go/token"
	"go/types"
	"golang.org/x/tools/go/packages"
	"io"
	"os"
)

type Conv struct {
	FileSet  *token.FileSet
	Packages []*packages.Package
}

func NewConv() (*Conv, error) {
	ret := &Conv{
		FileSet: token.NewFileSet(),
	}

	err := ret.initialize()
	if err != nil {
		return nil, err
	}

	return ret, nil
}

func (c *Conv) initialize() error {
	cfg := &packages.Config{Fset: c.FileSet, Mode: PackagesLoadMode}
	var err error
	c.Packages, err = packages.Load(cfg, "text/template", "text/template/parse")
	if err != nil {
		return err
	}
	if err = c.checkPackageErrors(c.Packages); err != nil {
		return err
	}
	return nil
}

func (c *Conv) Output(pkg *packages.Package, out io.Writer) error {
	if pkg.Types != nil {
		qual := types.RelativeTo(pkg.Types)

		gf := NewGenFile()

		gf.Line("# type: ignore")
		gf.Line("# package: %s", pkg.PkgPath)
		gf.NL()

		consts, funcs, _, allTypes := c.extract(pkg.Types.Scope())
		structs := c.findStructs(allTypes)
		interfaces := c.findInterfaces(allTypes)

		ct, err := closed.InPackage(c.FileSet, pkg.Syntax, pkg.Types)
		if err != nil {
			panic(err)
		}

		// Enums
		gf.Line("#")
		gf.Line("# ENUMS")
		gf.Line("#")
		gf.NL()
		for _, v := range ct {
			switch v := v.(type) {
			case *closed.Enum:
				c.outputEnum(gf, v)
				gf.NL()
			}
		}

		// Consts
		gf.Line("#")
		gf.Line("# CONSTS")
		gf.Line("#")
		gf.NL()
		for _, s := range consts {
			if c.typeIsEnum(s, ct) {
				continue
			}
			c.outputConst(gf, s, qual)
			gf.NL()
		}

		// Interfaces
		gf.Line("#")
		gf.Line("# INTERFACES")
		gf.Line("#")
		gf.NL()
		for _, s := range interfaces {
			c.outputInterface(gf, s, qual)
			gf.NL()
		}

		// Structs
		gf.Line("#")
		gf.Line("# STRUCTS")
		gf.Line("#")
		gf.NL()
		for _, s := range structs {
			c.outputStruct(gf, s, qual)
			gf.NL()
		}

		gf.Line("#")
		gf.Line("# FUNCS")
		gf.Line("#")
		gf.NL()
		for _, s := range funcs {
			c.outputFunc(gf, s, qual, false)
			gf.NL()
		}

		return gf.Output(out)
	}
	return nil
}

func (c *Conv) OutputFile(pkg *packages.Package, filename string) error {
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	if err = c.Output(pkg, f); err != nil {
		_ = f.Close()
		return err
	}
	return f.Close()
}

func (c *Conv) checkPackageErrors(pkgs []*packages.Package) error {
	var errorList error
	packages.Visit(pkgs, nil, func(pkg *packages.Package) {
		for _, err := range pkg.Errors {
			errorList = multierror.Append(errorList, err)
		}
	})
	return errorList
}

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
		if !t.IsAlias() {
			switch t.Type().Underlying().(type) {
			case *types.Struct:
				structs = append(structs, t)
			}
		}
	}
	return
}

const PackagesLoadMode packages.LoadMode = packages.NeedName |
	packages.NeedFiles |
	packages.NeedCompiledGoFiles |
	packages.NeedImports |
	packages.NeedDeps |
	packages.NeedExportsFile |
	packages.NeedTypes |
	packages.NeedSyntax |
	packages.NeedTypesInfo |
	packages.NeedTypesInfo
