package main

import (
	"github.com/jimmyfrasche/closed"
	"go/types"
)

func (cf *ConvFile) baseTypes(typ types.Type) (basetypes []types.Type) {
	switch t := typ.(type) {
	case *types.Named:
		return cf.baseTypes(t.Underlying())
	case *types.Struct:
		for i := 0; i < t.NumFields(); i++ {
			f := t.Field(i)
			if f.Embedded() {
				basetypes = append(basetypes, f.Type())
			}
		}
	case *types.Interface:
		for i := 0; i < t.NumEmbeddeds(); i++ {
			f := t.EmbeddedType(i)
			basetypes = append(basetypes, f)
		}
	}

	return
}

func (cf *ConvFile) baseTypesFiltered(s *types.TypeName, closedTypes []closed.Type) (basetypes []types.Type) {
	basetypes = cf.baseTypes(s.Type())

	itftypes := cf.itfTypes(s, closedTypes)

	for _, bt := range basetypes {
		for ifi := len(itftypes) - 1; ifi >= 0; ifi-- {
			if types.Implements(types.NewPointer(bt), itftypes[ifi].Underlying().(*types.Interface)) {
				itftypes = append(itftypes[:ifi], itftypes[ifi+1:]...) // remove item
			}
		}
	}

	for _, ifi := range itftypes {
		basetypes = append([]types.Type{ifi}, basetypes...)
	}

	return
}

func (cf *ConvFile) itfTypes(t *types.TypeName, closedTypes []closed.Type) (itftypes []types.Type) {
	for _, v := range closedTypes {
		switch v := v.(type) {
		case *closed.Interface:
		EndLoop:
			for _, cm := range v.Members {
				for _, cmt := range cm.TypeName {
					if t == cmt {
						for _, ct := range v.Types() {
							itftypes = append(itftypes, ct.Type())
						}
						break EndLoop
					}
				}
			}
		}
	}
	return
}

func (cf *ConvFile) typeIsEnum(typ types.Object) bool {
	for _, v := range cf.closedTypes {
		switch v := v.(type) {
		case *closed.Enum:
			for _, et := range v.Types() {
				if et == typ {
					return true
				}
			}
			for _, lbl := range v.Labels {
				for _, lbli := range lbl {
					if lbli == typ {
						return true
					}
				}
			}
		}
	}
	return false
}
