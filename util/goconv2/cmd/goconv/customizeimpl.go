package main

import "go/types"

//
// text/template/parse.NodeType
//
func (cf *ConvFile) customizeClassBody_TTP_NodeType(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	gf.NL()
	gf.Line("def __init__(self, nodetype: int):")
	gf.I()
	gf.Line("self.nodetype = nodetype")
	gf.D()
	return true
}

func (cf *ConvFile) customizeFuncSignature_TTP_NodeType_Type(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) bool {
	gf.Line("def Type(self) -> int:")
	return true
}

func (cf *ConvFile) customizeFuncBody_TTP_NodeType_Type(gf *GenFile, s *types.Func, qf types.Qualifier) CustomizeAction {
	gf.Line("return self.nodetype")
	return CustomizeAction_FinishedAndDefault
}

//
// text/template/parse.Pos
//
func (cf *ConvFile) customizeClassBody_TTP_Pos(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	gf.NL()
	gf.Line("def __init__(self, pos):")
	gf.I()
	gf.Line("self.pos = pos")
	gf.D()
	return true
}

func (cf *ConvFile) customizeFuncBody_TTP_Pos_Position(gf *GenFile, s *types.Func, qf types.Qualifier) CustomizeAction {
	gf.Line("return self.pos")
	return CustomizeAction_FinishedAndDefault
}

//
// text/template/parse.ActionNode
//
func (cf *ConvFile) customizeClassBody_TTP_ActionNode(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	gf.NL()
	gf.Line("def __init__(self, tr, line, pipe, pos):")
	gf.I()
	gf.Line("NodeType.__init__(self, NodeType.NodeAction)")
	gf.Line("Pos.__init__(self, pos)")
	gf.Line("self.tr = tr")
	gf.Line("self.Line = line")
	gf.Line("self.Pipe = pipe")
	gf.D()
	return true
}

//func (cf *ConvFile) customizeFuncBody_TTP_ActionNode_tree(gf *GenFile, s *types.Func, qf types.Qualifier) CustomizeAction {
//	gf.Line("return self.tr")
//	return CustomizeAction_FinishedAndDefault
//}
