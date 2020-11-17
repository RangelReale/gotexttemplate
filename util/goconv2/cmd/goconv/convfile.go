package main

import (
	"go/types"
	"io"
	"os"

	"github.com/jimmyfrasche/closed"
	"golang.org/x/tools/go/packages"
)

type ConvFile struct {
	Conv *Conv
	Package *packages.Package

	gf *GenFile
	consts []*types.Const
	funcs []*types.Func
	vars []*types.Var
	allTypes []*types.TypeName
	typs []*types.TypeName
	interfaces []*types.TypeName
	structs []*types.TypeName
	closedTypes []closed.Type
}

func NewConvFile(conv *Conv, pkg *packages.Package) (*ConvFile, error) {
	ret := &ConvFile{
		Conv: conv,
		Package: pkg,
	}

	err := ret.initialize()
	if err != nil {
		return nil, err
	}

	return ret, nil
}

func (cf *ConvFile) initialize() error {
	cf.consts, cf.funcs, cf.vars, cf.allTypes = cf.Conv.extract(cf.Package.Types.Scope())
	cf.typs = cf.Conv.findTypes(cf.allTypes)
	cf.structs = cf.Conv.findStructs(cf.allTypes)
	cf.interfaces = cf.Conv.findInterfaces(cf.allTypes)

	var err error
	cf.closedTypes, err = closed.InPackage(cf.Conv.FileSet, cf.Package.Syntax, cf.Package.Types)
	if err != nil {
		panic(err)
	}

	return nil
}

func (cf *ConvFile) BaseFilename() string {
	return cf.Conv.BaseFilename(cf.Package)
}

func (cf *ConvFile) Filename() string {
	return cf.Conv.Filename(cf.Package)
}

func (cf *ConvFile) Output(out io.Writer) error {
	if cf.Package.Types != nil {
		qual := types.RelativeTo(cf.Package.Types)

		gf := NewGenFile()

		gf.Line("# type: ignore")
		gf.Line("# package: %s", cf.Package.PkgPath)
		gf.NL()

		gf.Line("from enum import Enum")
		gf.Line("from typing import Callable, Optional, List, Dict, Any, Tuple")
		gf.Line("import queue")
		gf.Line("from . import goext")

		for _, pi := range cf.Package.Imports {
			for _, pc := range cf.Conv.Packages {
				if pc == cf.Package {
					continue
				}
				if pi == pc {
					gf.Line("from . import %s", cf.Conv.BaseFilename(pi))
				}
			}
		}

		gf.NL()

		// Enums
		gf.NL()
		gf.Line("#")
		gf.Line("# ENUMS")
		gf.Line("#")
		gf.NL()
		for _, v := range cf.closedTypes {
			switch v := v.(type) {
			case *closed.Enum:
				gf.NL()
				cf.outputEnum(gf, v, qual)
				gf.NL()
			}
		}

		// Consts
		gf.NL()
		gf.Line("#")
		gf.Line("# CONSTS")
		gf.Line("#")
		gf.NL()
		for _, s := range cf.consts {
			if cf.typeIsEnum(s) {
				continue
			}
			gf.NL()
			cf.outputConst(gf, s, qual)
			gf.NL()
		}

		// Types
		gf.Line("#")
		gf.Line("# TYPES")
		gf.Line("#")
		gf.NL()
		for _, s := range cf.typs {
			if cf.typeIsEnum(s) {
				continue
			}
			gf.NL()
			cf.outputTypes(gf, s, qual)
			gf.NL()
		}

		// Interfaces
		gf.NL()
		gf.Line("#")
		gf.Line("# INTERFACES")
		gf.Line("#")
		gf.NL()
		for _, s := range cf.interfaces {
			if cf.typeIsEnum(s) {
				continue
			}
			gf.NL()
			cf.outputClass(gf, s, qual)
			gf.NL()
		}

		// Structs
		gf.NL()
		gf.Line("#")
		gf.Line("# STRUCTS")
		gf.Line("#")
		gf.NL()
		for _, s := range cf.Conv.sortStructs(cf.Package, cf.structs) {
			if cf.typeIsEnum(s) {
				continue
			}
			gf.NL()
			cf.outputClass(gf, s, qual)
			gf.NL()
		}

		// Funcs
		gf.NL()
		gf.Line("#")
		gf.Line("# FUNCS")
		gf.Line("#")
		gf.NL()
		for _, s := range cf.funcs {
			gf.NL()
			cf.outputFunc(gf, s, qual, false)
			gf.NL()
		}

		return gf.Output(out)
	}
	return nil
}

func (cf *ConvFile) OutputFile(filename string) error {
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	if err = cf.Output(f); err != nil {
		_ = f.Close()
		return err
	}
	return f.Close()
}
