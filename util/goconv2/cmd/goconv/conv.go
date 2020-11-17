package main

import (
	"fmt"
	"go/token"
	"strings"

	"github.com/hashicorp/go-multierror"
	"golang.org/x/tools/go/packages"
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

func (c *Conv) BaseFilename(pkg *packages.Package) string {
	return fmt.Sprintf("%s", strings.Replace(pkg.PkgPath, "/", "_", -1))
}

func (c *Conv) Filename(pkg *packages.Package) string {
	return fmt.Sprintf("%s.py", c.BaseFilename(pkg))
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

func (c *Conv) File(pkg *packages.Package) (*ConvFile, error) {
	return NewConvFile(c, pkg)
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
