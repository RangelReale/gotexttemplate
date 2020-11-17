package main

import "go/types"

func (cf *ConvFile) customizeClassBody(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	if cf.Package.PkgPath == "text/template/parse" {
		if s.Name() == "NodeType" {
			return cf.customizeClassBody_TTP_NodeType(gf, s, qf)
		}
	}

	return false
}

func (cf *ConvFile) customizeFuncBody(gf *GenFile, s *types.Func, qf types.Qualifier) bool {
	if cf.Package.PkgPath == "text/template/parse" {
		if s.Type().(*types.Signature).Recv() != nil {
			recv := s.Type().(*types.Signature).Recv().Type()
			if p, pok := recv.(*types.Pointer); pok {
				recv = p.Elem()
			}

			recvType := ""
			if nt, ntok := recv.(*types.Named); ntok {
				recvType = nt.Obj().Name()
			}
			//if recv.Type().String() == "NodeType" {
			if recvType == "NodeType" {
				if s.Name() == "Type" {
					return cf.customizeFuncBody_TTP_NodeType_Type(gf, s, qf)
				}
			}
		}
	}
	return true
}

