package main

import "go/types"

type CustomizeAction int

const (
	CustomizeAction_Default CustomizeAction = iota
	CustomizeAction_Finished
	CustomizeAction_FinishedAndDefault
	CustomizeAction_UseGenerated
)

func (cf *ConvFile) customizeClassBody(gf *GenFile, s *types.TypeName, qf types.Qualifier) bool {
	if cf.Package.PkgPath == "text/template/parse" {
		if s.Name() == "NodeType" {
			return cf.customizeClassBody_TTP_NodeType(gf, s, qf)
		} else if s.Name() == "Pos" {
				return cf.customizeClassBody_TTP_Pos(gf, s, qf)
		} else if s.Name() == "ActionNode" {
			return cf.customizeClassBody_TTP_ActionNode(gf, s, qf)
		}
	}

	return false
}

func (cf *ConvFile) customizeFuncSignature(gf *GenFile, s *types.Func, qf types.Qualifier, self bool) bool {
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
			if recvType == "NodeType" {
				if s.Name() == "Type" {
					return cf.customizeFuncSignature_TTP_NodeType_Type(gf, s, qf, self)
				}
			}
		}
	}
	return false
}

var customizeFuncBodyDefault = map[string]map[string][]string {
	"text/template/parse": map[string][]string {
		"ActionNode": []string{"tree"},
		"BoolNode": []string{"tree"},
		"BranchNode": []string{"tree"},
		"ChainNode": []string{"tree"},
		"CommandNode": []string{"tree"},
		"DotNode": []string{"tree", "String"},
		"FieldNode": []string{"tree"},
		"IdentifierNode": []string{"tree", "String"},
		"ListNode": []string{"tree", "Copy"},
		"NilNode": []string{"tree", "String"},
		"NumberNode": []string{"tree", "String"},
		"PipeNode": []string{"tree", "Copy"},
		"StringNode": []string{"tree", "String"},
		"TemplateNode": []string{"tree"},
		"TextNode": []string{"tree"},
	},
}

func (cf *ConvFile) customizeFuncBody(gf *GenFile, s *types.Func, qf types.Qualifier) CustomizeAction {
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

			if recvType != "" {
				if cd, cdok := customizeFuncBodyDefault[cf.Package.PkgPath]; cdok {
					if cdr, cdok := cd[recvType]; cdok {
						if stringInSlice(s.Name(), cdr) {
							return CustomizeAction_UseGenerated
						}
					}
				}
			}

			if recvType == "NodeType" {
				if s.Name() == "Type" {
					return cf.customizeFuncBody_TTP_NodeType_Type(gf, s, qf)
				}
			} else if recvType == "Pos" {
				if s.Name() == "Position" {
					return cf.customizeFuncBody_TTP_Pos_Position(gf, s, qf)
				}
			//} else if recvType == "ActionNode" {
			//	if s.Name() == "tree" {
			//		return cf.customizeFuncBody_TTP_ActionNode_tree(gf, s, qf)
			//	}
			}
		}
	}
	return CustomizeAction_Default
}

