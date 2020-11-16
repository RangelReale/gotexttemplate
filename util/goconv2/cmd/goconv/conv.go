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
	gf := NewGenFile()

	gf.Line("# package: %s", pkg.PkgPath)

	c.extract(pkg.Types.Scope())

	ct, err := closed.InPackage(c.FileSet, pkg.Syntax, pkg.Types)
	if err != nil {
		panic(err)
	}
	for _, v := range ct {
		switch v := v.(type) {
		case *closed.Enum:
			err = c.outputEnum(gf, v)
			if err != nil {
				return err
			}
			gf.NL()
		}
	}

	return gf.Output(out)
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
