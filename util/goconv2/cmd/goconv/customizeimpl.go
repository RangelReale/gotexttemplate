package main

import "go/types"

func (cf *ConvFile) customizeClassBody_TTP_NodeType(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	gf.NL()
	gf.Line("def __init__(self, nodetype = None):")
	gf.I()
	gf.Line("self.nodetype = nodetype")
	gf.D()
	return true
}

func (cf *ConvFile) customizeFuncBody_TTP_NodeType_Type(gf *GenFile, s *types.Func, qf types.Qualifier) bool {
	gf.Line("return self.nodetype")
	return true
}