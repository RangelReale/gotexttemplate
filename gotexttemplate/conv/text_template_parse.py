# type: ignore
# package: text/template/parse

from enum import Enum
from typing import Callable, Optional, List, Dict, Any, Tuple
import queue
from . import goext


#
# ENUMS
#


# c:\go\src\text\template\parse\node.go:36:6
class NodeType:
    NodeText = 0  # Plain text.
    NodeAction = 1  # A non-control action such as a field evaluation.
    NodeBool = 2  # A boolean constant.
    NodeChain = 3  # A sequence of field accesses.
    NodeCommand = 4  # An element of a pipeline.
    NodeDot = 5  # The cursor, dot.
    nodeElse = 6  # An else action. Not added to tree.
    nodeEnd = 7  # An end action. Not added to tree.
    NodeField = 8  # A field or method name.
    NodeIdentifier = 9  # An identifier; always a function name.
    NodeIf = 10  # An if action.
    NodeList = 11  # A list of Nodes.
    NodeNil = 12  # An untyped nil constant.
    NodeNumber = 13  # A numerical constant.
    NodePipe = 14  # A pipeline of commands.
    NodeRange = 15  # A range action.
    NodeString = 16  # A string constant.
    NodeTemplate = 17  # A template invocation action.
    NodeVariable = 18  # A $ variable.
    NodeWith = 19  # A with action.

    # c:\go\src\text\template\parse\node.go:48:19
    def Type(self) -> 'NodeType':
        #         {
        #         	return t
        #         }
        pass


# c:\go\src\text\template\parse\lex.go:37:6
class itemType:
    itemError = 0  # error occurred; value is text of error
    itemBool = 1  # boolean constant
    itemChar = 2  # printable ASCII character; grab bag for comma etc.
    itemCharConstant = 3  # character constant
    itemComplex = 4  # complex constant (1+2i); imaginary is just a number
    itemAssign = 5  # equals ('=') introducing an assignment
    itemDeclare = 6  # colon-equals (':=') introducing a declaration
    itemEOF = 7
    itemField = 8  # alphanumeric identifier starting with '.'
    itemIdentifier = 9  # alphanumeric identifier not starting with '.'
    itemLeftDelim = 10  # left action delimiter
    itemLeftParen = 11  # '(' inside action
    itemNumber = 12  # simple number, including imaginary
    itemPipe = 13  # pipe symbol
    itemRawString = 14  # raw quoted string (includes quotes)
    itemRightDelim = 15  # right action delimiter
    itemRightParen = 16  # ')' inside action
    itemSpace = 17  # run of spaces separating arguments
    itemString = 18  # quoted string (includes quotes)
    itemText = 19  # plain text
    itemVariable = 20  # variable starting with '$', such as '$' or  '$1' or '$hello'
    itemKeyword = 21  # used only to delimit the keywords
    itemBlock = 22  # block keyword
    itemDot = 23  # the cursor, spelled '.'
    itemDefine = 24  # define keyword
    itemElse = 25  # else keyword
    itemEnd = 26  # end keyword
    itemIf = 27  # if keyword
    itemNil = 28  # the untyped nil constant, easiest to treat as a keyword
    itemRange = 29  # range keyword
    itemTemplate = 30  # template keyword
    itemWith = 31  # with keyword


#
# CONSTS
#


# c:\go\src\text\template\parse\lex.go:88:7
eof: int = -1


# c:\go\src\text\template\parse\lex.go:240:2
leftComment: str = "/*"


# c:\go\src\text\template\parse\lex.go:238:2
leftDelim: str = "{{"


# c:\go\src\text\template\parse\lex.go:100:2
leftTrimMarker: str = "- "  # Attached to left delimiter, trims trailing spaces from preceding text.


# c:\go\src\text\template\parse\lex.go:241:2
rightComment: str = "*/"


# c:\go\src\text\template\parse\lex.go:239:2
rightDelim: str = "}}"


# c:\go\src\text\template\parse\lex.go:101:2
rightTrimMarker: str = " -"  # Attached to right delimiter, trims leading spaces from following text.


# c:\go\src\text\template\parse\lex.go:99:2
spaceChars: str = " \t\r\n"  # These are the space characters defined by Go itself.


# c:\go\src\text\template\parse\lex.go:102:2
trimMarkerLen: 'Pos' = 2

#
# TYPES
#




# c:\go\src\text\template\parse\lex.go:106:6
stateFn = Callable[[Optional['lexer']], 'stateFn']


#
# INTERFACES
#


# c:\go\src\text\template\parse\node.go:20:6
class Node:

    # c:\go\src\text\template\parse\node.go:26:2
    def Copy(self) -> 'Node':
        # Function body not found
        pass

    # c:\go\src\text\template\parse\node.go:27:2
    def Position(self) -> 'Pos':  # byte position of start of node in full original input string
        # Function body not found
        pass

    # c:\go\src\text\template\parse\node.go:22:2
    def String(self) -> str:
        # Function body not found
        pass

    # c:\go\src\text\template\parse\node.go:21:2
    def Type(self) -> 'NodeType':
        # Function body not found
        pass

    # c:\go\src\text\template\parse\node.go:30:2
    def tree(self) -> Optional['Tree']:
        # Function body not found
        pass

    # c:\go\src\text\template\parse\node.go:32:2
    def writeTo(self, p0: Optional[goext.strings_Builder]) -> None:
        # Function body not found
        pass


#
# STRUCTS
#


# c:\go\src\text\template\parse\node.go:40:6
class Pos:

    # c:\go\src\text\template\parse\node.go:42:14
    def Position(self) -> 'Pos':
        #         {
        #         	return p
        #         }
        pass


# c:\go\src\text\template\parse\node.go:222:6
class ActionNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    Pipe: Optional['PipeNode']  # The pipeline in the action.

    # c:\go\src\text\template\parse\node.go:234:22
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	a.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:240:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString("{{")
        #         	a.Pipe.writeTo(sb)
        #         	sb.WriteString("}}")
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:246:22
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return a.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:250:22
    def Copy(self) -> 'Node':
        #         {
        #         	return a.tr.newAction(a.Pos, a.Line, a.Pipe.CopyPipe())
        #         
        #         }
        pass


# c:\go\src\text\template\parse\node.go:547:6
class BoolNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    True_: bool  # The value of the boolean constant.

    # c:\go\src\text\template\parse\node.go:558:20
    def String(self) -> str:
        #         {
        #         	if b.True {
        #         		return "true"
        #         	}
        #         	return "false"
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:565:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(b.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:569:20
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return b.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:573:20
    def Copy(self) -> 'Node':
        #         {
        #         	return b.tr.newBool(b.Pos, b.True)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:806:6
class BranchNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    Pipe: Optional['PipeNode']  # The pipeline to be evaluated.
    List: Optional['ListNode']  # What to execute if the value is non-empty.
    ElseList: Optional['ListNode']  # What to execute if the value is empty (nil if absent).

    # c:\go\src\text\template\parse\node.go:816:22
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	b.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:822:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	name := ""
        #         	switch b.NodeType {
        #         	case NodeIf:
        #         		name = "if"
        #         	case NodeRange:
        #         		name = "range"
        #         	case NodeWith:
        #         		name = "with"
        #         	default:
        #         		panic("unknown branch type")
        #         	}
        #         	sb.WriteString("{{")
        #         	sb.WriteString(name)
        #         	sb.WriteByte(' ')
        #         	b.Pipe.writeTo(sb)
        #         	sb.WriteString("}}")
        #         	b.List.writeTo(sb)
        #         	if b.ElseList != nil {
        #         		sb.WriteString("{{else}}")
        #         		b.ElseList.writeTo(sb)
        #         	}
        #         	sb.WriteString("{{end}}")
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:847:22
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return b.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:851:22
    def Copy(self) -> 'Node':
        #         {
        #         	switch b.NodeType {
        #         	case NodeIf:
        #         		return b.tr.newIf(b.Pos, b.Line, b.Pipe, b.List, b.ElseList)
        #         	case NodeRange:
        #         		return b.tr.newRange(b.Pos, b.Line, b.Pipe, b.List, b.ElseList)
        #         	case NodeWith:
        #         		return b.tr.newWith(b.Pos, b.Line, b.Pipe, b.List, b.ElseList)
        #         	default:
        #         		panic("unknown branch type")
        #         	}
        #         }
        pass


# c:\go\src\text\template\parse\node.go:494:6
class ChainNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Node: 'Node'
    Field: Optional[List[str]]  # The identifiers in lexical order.

    # c:\go\src\text\template\parse\node.go:507:21
    def Add(self, field: str) -> None:
        #         {
        #         	if len(field) == 0 || field[0] != '.' {
        #         		panic("no dot in field")
        #         	}
        #         	field = field[1:]
        #         	if field == "" {
        #         		panic("empty field")
        #         	}
        #         	c.Field = append(c.Field, field)
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:518:21
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	c.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:524:21
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	if _, ok := c.Node.(*PipeNode); ok {
        #         		sb.WriteByte('(')
        #         		c.Node.writeTo(sb)
        #         		sb.WriteByte(')')
        #         	} else {
        #         		c.Node.writeTo(sb)
        #         	}
        #         	for _, field := range c.Field {
        #         		sb.WriteByte('.')
        #         		sb.WriteString(field)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:538:21
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return c.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:542:21
    def Copy(self) -> 'Node':
        #         {
        #         	return &ChainNode{tr: c.tr, NodeType: NodeChain, Pos: c.Pos, Node: c.Node, Field: append([]string{}, c.Field...)}
        #         }
        pass


# c:\go\src\text\template\parse\node.go:256:6
class CommandNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Args: Optional[List['Node']]  # Arguments in lexical order: Identifier, field, or constant.

    # c:\go\src\text\template\parse\node.go:267:23
    def append(self, arg: 'Node') -> None:
        #         {
        #         	c.Args = append(c.Args, arg)
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:271:23
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	c.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:277:23
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	for i, arg := range c.Args {
        #         		if i > 0 {
        #         			sb.WriteByte(' ')
        #         		}
        #         		if arg, ok := arg.(*PipeNode); ok {
        #         			sb.WriteByte('(')
        #         			arg.writeTo(sb)
        #         			sb.WriteByte(')')
        #         			continue
        #         		}
        #         		arg.writeTo(sb)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:292:23
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return c.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:296:23
    def Copy(self) -> 'Node':
        #         {
        #         	if c == nil {
        #         		return c
        #         	}
        #         	n := c.tr.newCommand(c.Pos)
        #         	for _, c := range c.Args {
        #         		n.append(c.Copy())
        #         	}
        #         	return n
        #         }
        pass


# c:\go\src\text\template\parse\node.go:389:6
class DotNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:399:19
    def Type(self) -> 'NodeType':
        #         {
        #         
        #         	return NodeDot
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:406:19
    def String(self) -> str:
        #         {
        #         	return "."
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:410:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(d.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:414:19
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return d.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:418:19
    def Copy(self) -> 'Node':
        #         {
        #         	return d.tr.newDot(d.Pos)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:459:6
class FieldNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: Optional[List[str]]  # The identifiers in lexical order.

    # c:\go\src\text\template\parse\node.go:470:21
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	f.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:476:21
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	for _, id := range f.Ident {
        #         		sb.WriteByte('.')
        #         		sb.WriteString(id)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:483:21
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return f.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:487:21
    def Copy(self) -> 'Node':
        #         {
        #         	return &FieldNode{tr: f.tr, NodeType: NodeField, Pos: f.Pos, Ident: append([]string{}, f.Ident...)}
        #         }
        pass


# c:\go\src\text\template\parse\node.go:308:6
class IdentifierNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: str  # The identifier's name.

    # c:\go\src\text\template\parse\node.go:323:26
    def SetPos(self, pos: 'Pos') -> Optional['IdentifierNode']:
        #         {
        #         	i.Pos = pos
        #         	return i
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:331:26
    def SetTree(self, t: Optional['Tree']) -> Optional['IdentifierNode']:
        #         {
        #         	i.tr = t
        #         	return i
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:336:26
    def String(self) -> str:
        #         {
        #         	return i.Ident
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:340:26
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(i.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:344:26
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return i.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:348:26
    def Copy(self) -> 'Node':
        #         {
        #         	return NewIdentifier(i.Ident).SetTree(i.tr).SetPos(i.Pos)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:865:6
class IfNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:873:18
    def Copy(self) -> 'Node':
        #         {
        #         	return i.tr.newIf(i.Pos, i.Line, i.Pipe.CopyPipe(), i.List.CopyList(), i.ElseList.CopyList())
        #         }
        pass


# c:\go\src\text\template\parse\node.go:78:6
class ListNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Nodes: Optional[List['Node']]  # The element nodes in lexical order.

    # c:\go\src\text\template\parse\node.go:89:20
    def append(self, n: 'Node') -> None:
        #         {
        #         	l.Nodes = append(l.Nodes, n)
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:93:20
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return l.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:97:20
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	l.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:103:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	for _, n := range l.Nodes {
        #         		n.writeTo(sb)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:109:20
    def CopyList(self) -> Optional['ListNode']:
        #         {
        #         	if l == nil {
        #         		return l
        #         	}
        #         	n := l.tr.newList(l.Pos)
        #         	for _, elem := range l.Nodes {
        #         		n.append(elem.Copy())
        #         	}
        #         	return n
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:120:20
    def Copy(self) -> 'Node':
        #         {
        #         	return l.CopyList()
        #         }
        pass


# c:\go\src\text\template\parse\node.go:423:6
class NilNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:433:19
    def Type(self) -> 'NodeType':
        #         {
        #         
        #         	return NodeNil
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:440:19
    def String(self) -> str:
        #         {
        #         	return "nil"
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:444:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(n.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:448:19
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return n.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:452:19
    def Copy(self) -> 'Node':
        #         {
        #         	return n.tr.newNil(n.Pos)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:580:6
class NumberNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    IsInt: bool  # Number has an integral value.
    IsUint: bool  # Number has an unsigned integral value.
    IsFloat: bool  # Number has a floating-point value.
    IsComplex: bool  # Number is complex.
    Int64: int  # The signed integer value.
    Uint64: int  # The unsigned integer value.
    Float64: float  # The floating-point value.
    Complex128: complex  # The complex value.
    Text: str  # The original textual representation from the input.

    # c:\go\src\text\template\parse\node.go:683:22
    def simplifyComplex(self) -> None:
        #         {
        #         	n.IsFloat = imag(n.Complex128) == 0
        #         	if n.IsFloat {
        #         		n.Float64 = real(n.Complex128)
        #         		n.IsInt = float64(int64(n.Float64)) == n.Float64
        #         		if n.IsInt {
        #         			n.Int64 = int64(n.Float64)
        #         		}
        #         		n.IsUint = float64(uint64(n.Float64)) == n.Float64
        #         		if n.IsUint {
        #         			n.Uint64 = uint64(n.Float64)
        #         		}
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:698:22
    def String(self) -> str:
        #         {
        #         	return n.Text
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:702:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(n.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:706:22
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return n.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:710:22
    def Copy(self) -> 'Node':
        #         {
        #         	nn := new(NumberNode)
        #         	*nn = *n
        #         	return nn
        #         }
        pass


# c:\go\src\text\template\parse\node.go:153:6
class PipeNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    IsAssign: bool  # The variables are being assigned, not declared.
    Decl: Optional[List[Optional['VariableNode']]]  # Variables in lexical order.
    Cmds: Optional[List[Optional['CommandNode']]]  # The commands in lexical order.

    # c:\go\src\text\template\parse\node.go:167:20
    def append(self, command: Optional['CommandNode']) -> None:
        #         {
        #         	p.Cmds = append(p.Cmds, command)
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:171:20
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	p.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:177:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	if len(p.Decl) > 0 {
        #         		for i, v := range p.Decl {
        #         			if i > 0 {
        #         				sb.WriteString(", ")
        #         			}
        #         			v.writeTo(sb)
        #         		}
        #         		sb.WriteString(" := ")
        #         	}
        #         	for i, c := range p.Cmds {
        #         		if i > 0 {
        #         			sb.WriteString(" | ")
        #         		}
        #         		c.writeTo(sb)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:195:20
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return p.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:199:20
    def CopyPipe(self) -> Optional['PipeNode']:
        #         {
        #         	if p == nil {
        #         		return p
        #         	}
        #         	vars := make([]*VariableNode, len(p.Decl))
        #         	for i, d := range p.Decl {
        #         		vars[i] = d.Copy().(*VariableNode)
        #         	}
        #         	n := p.tr.newPipeline(p.Pos, p.Line, vars)
        #         	n.IsAssign = p.IsAssign
        #         	for _, c := range p.Cmds {
        #         		n.append(c.Copy().(*CommandNode))
        #         	}
        #         	return n
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:215:20
    def Copy(self) -> 'Node':
        #         {
        #         	return p.CopyPipe()
        #         }
        pass


# c:\go\src\text\template\parse\node.go:878:6
class RangeNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:886:21
    def Copy(self) -> 'Node':
        #         {
        #         	return r.tr.newRange(r.Pos, r.Line, r.Pipe.CopyPipe(), r.List.CopyList(), r.ElseList.CopyList())
        #         }
        pass


# c:\go\src\text\template\parse\node.go:717:6
class StringNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Quoted: str  # The original text of the string, with quotes.
    Text: str  # The string, after quote processing.

    # c:\go\src\text\template\parse\node.go:729:22
    def String(self) -> str:
        #         {
        #         	return s.Quoted
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:733:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(s.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:737:22
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return s.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:741:22
    def Copy(self) -> 'Node':
        #         {
        #         	return s.tr.newString(s.Pos, s.Quoted, s.Text)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:904:6
class TemplateNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    Name: str  # The name of the template (unquoted).
    Pipe: Optional['PipeNode']  # The command to evaluate as dot for the template.

    # c:\go\src\text\template\parse\node.go:917:24
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	t.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:923:24
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString("{{template ")
        #         	sb.WriteString(strconv.Quote(t.Name))
        #         	if t.Pipe != nil {
        #         		sb.WriteByte(' ')
        #         		t.Pipe.writeTo(sb)
        #         	}
        #         	sb.WriteString("}}")
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:933:24
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return t.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:937:24
    def Copy(self) -> 'Node':
        #         {
        #         	return t.tr.newTemplate(t.Pos, t.Line, t.Name, t.Pipe.CopyPipe())
        #         }
        pass


# c:\go\src\text\template\parse\node.go:125:6
class TextNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Text: Optional[List[int]]  # The text; may span newlines.

    # c:\go\src\text\template\parse\node.go:136:20
    def String(self) -> str:
        #         {
        #         	return fmt.Sprintf(textFormat, t.Text)
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:140:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(t.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:144:20
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return t.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:148:20
    def Copy(self) -> 'Node':
        #         {
        #         	return &TextNode{tr: t.tr, NodeType: NodeText, Pos: t.Pos, Text: append([]byte{}, t.Text...)}
        #         }
        pass


# c:\go\src\text\template\parse\parse.go:20:6
class Tree:
    Name: str  # name of the template represented by the tree.
    ParseName: str  # name of the top-level template during parsing, for error messages.
    Root: Optional['ListNode']  # top-level root of the tree.
    text: str  # text parsed to create the template (or its parent)
    funcs: Optional[List[Dict[str, Any]]]
    lex: Optional['lexer']
    token: Optional[List['item']]  # three-token lookahead for parser.
    peekCount: int
    vars: Optional[List[str]]  # variables defined at the moment.
    treeSet: Optional[Dict[str, Optional['Tree']]]

    # c:\go\src\text\template\parse\node.go:85:16
    def newList(self, pos: 'Pos') -> Optional['ListNode']:
        #         {
        #         	return &ListNode{tr: t, NodeType: NodeList, Pos: pos}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:132:16
    def newText(self, pos: 'Pos', text: str) -> Optional['TextNode']:
        #         {
        #         	return &TextNode{tr: t, NodeType: NodeText, Pos: pos, Text: []byte(text)}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:163:16
    def newPipeline(self, pos: 'Pos', line: int, vars: List[Optional['VariableNode']]) -> Optional['PipeNode']:
        #         {
        #         	return &PipeNode{tr: t, NodeType: NodePipe, Pos: pos, Line: line, Decl: vars}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:230:16
    def newAction(self, pos: 'Pos', line: int, pipe: Optional['PipeNode']) -> Optional['ActionNode']:
        #         {
        #         	return &ActionNode{tr: t, NodeType: NodeAction, Pos: pos, Line: line, Pipe: pipe}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:263:16
    def newCommand(self, pos: 'Pos') -> Optional['CommandNode']:
        #         {
        #         	return &CommandNode{tr: t, NodeType: NodeCommand, Pos: pos}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:361:16
    def newVariable(self, pos: 'Pos', ident: str) -> Optional['VariableNode']:
        #         {
        #         	return &VariableNode{tr: t, NodeType: NodeVariable, Pos: pos, Ident: strings.Split(ident, ".")}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:395:16
    def newDot(self, pos: 'Pos') -> Optional['DotNode']:
        #         {
        #         	return &DotNode{tr: t, NodeType: NodeDot, Pos: pos}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:429:16
    def newNil(self, pos: 'Pos') -> Optional['NilNode']:
        #         {
        #         	return &NilNode{tr: t, NodeType: NodeNil, Pos: pos}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:466:16
    def newField(self, pos: 'Pos', ident: str) -> Optional['FieldNode']:
        #         {
        #         	return &FieldNode{tr: t, NodeType: NodeField, Pos: pos, Ident: strings.Split(ident[1:], ".")}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:502:16
    def newChain(self, pos: 'Pos', node: 'Node') -> Optional['ChainNode']:
        #         {
        #         	return &ChainNode{tr: t, NodeType: NodeChain, Pos: pos, Node: node}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:554:16
    def newBool(self, pos: 'Pos', true: bool) -> Optional['BoolNode']:
        #         {
        #         	return &BoolNode{tr: t, NodeType: NodeBool, Pos: pos, True: true}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:595:16
    def newNumber(self, pos: 'Pos', text: str, typ: 'itemType') -> Tuple[Optional['NumberNode'], 'goext.error']:
        #         {
        #         	n := &NumberNode{tr: t, NodeType: NodeNumber, Pos: pos, Text: text}
        #         	switch typ {
        #         	case itemCharConstant:
        #         		rune, _, tail, err := strconv.UnquoteChar(text[1:], text[0])
        #         		if err != nil {
        #         			return nil, err
        #         		}
        #         		if tail != "'" {
        #         			return nil, fmt.Errorf("malformed character constant: %!s(MISSING)", text)
        #         		}
        #         		n.Int64 = int64(rune)
        #         		n.IsInt = true
        #         		n.Uint64 = uint64(rune)
        #         		n.IsUint = true
        #         		n.Float64 = float64(rune)
        #         		n.IsFloat = true
        #         		return n, nil
        #         	case itemComplex:
        #         
        #         		if _, err := fmt.Sscan(text, &n.Complex128); err != nil {
        #         			return nil, err
        #         		}
        #         		n.IsComplex = true
        #         		n.simplifyComplex()
        #         		return n, nil
        #         	}
        #         
        #         	if len(text) > 0 && text[len(text)-1] == 'i' {
        #         		f, err := strconv.ParseFloat(text[:len(text)-1], 64)
        #         		if err == nil {
        #         			n.IsComplex = true
        #         			n.Complex128 = complex(0, f)
        #         			n.simplifyComplex()
        #         			return n, nil
        #         		}
        #         	}
        #         
        #         	u, err := strconv.ParseUint(text, 0, 64)
        #         	if err == nil {
        #         		n.IsUint = true
        #         		n.Uint64 = u
        #         	}
        #         	i, err := strconv.ParseInt(text, 0, 64)
        #         	if err == nil {
        #         		n.IsInt = true
        #         		n.Int64 = i
        #         		if i == 0 {
        #         			n.IsUint = true
        #         			n.Uint64 = u
        #         		}
        #         	}
        #         
        #         	if n.IsInt {
        #         		n.IsFloat = true
        #         		n.Float64 = float64(n.Int64)
        #         	} else if n.IsUint {
        #         		n.IsFloat = true
        #         		n.Float64 = float64(n.Uint64)
        #         	} else {
        #         		f, err := strconv.ParseFloat(text, 64)
        #         		if err == nil {
        #         
        #         			if !strings.ContainsAny(text, ".eEpP") {
        #         				return nil, fmt.Errorf("integer overflow: %!q(MISSING)", text)
        #         			}
        #         			n.IsFloat = true
        #         			n.Float64 = f
        #         
        #         			if !n.IsInt && float64(int64(f)) == f {
        #         				n.IsInt = true
        #         				n.Int64 = int64(f)
        #         			}
        #         			if !n.IsUint && float64(uint64(f)) == f {
        #         				n.IsUint = true
        #         				n.Uint64 = uint64(f)
        #         			}
        #         		}
        #         	}
        #         	if !n.IsInt && !n.IsUint && !n.IsFloat {
        #         		return nil, fmt.Errorf("illegal number syntax: %!q(MISSING)", text)
        #         	}
        #         	return n, nil
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:725:16
    def newString(self, pos: 'Pos', orig: str, text: str) -> Optional['StringNode']:
        #         {
        #         	return &StringNode{tr: t, NodeType: NodeString, Pos: pos, Quoted: orig, Text: text}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:753:16
    def newEnd(self, pos: 'Pos') -> Optional['endNode']:
        #         {
        #         	return &endNode{tr: t, NodeType: nodeEnd, Pos: pos}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:781:16
    def newElse(self, pos: 'Pos', line: int) -> Optional['elseNode']:
        #         {
        #         	return &elseNode{tr: t, NodeType: nodeElse, Pos: pos, Line: line}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:869:16
    def newIf(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['IfNode']:
        #         {
        #         	return &IfNode{BranchNode{tr: t, NodeType: NodeIf, Pos: pos, Line: line, Pipe: pipe, List: list, ElseList: elseList}}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:882:16
    def newRange(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['RangeNode']:
        #         {
        #         	return &RangeNode{BranchNode{tr: t, NodeType: NodeRange, Pos: pos, Line: line, Pipe: pipe, List: list, ElseList: elseList}}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:895:16
    def newWith(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['WithNode']:
        #         {
        #         	return &WithNode{BranchNode{tr: t, NodeType: NodeWith, Pos: pos, Line: line, Pipe: pipe, List: list, ElseList: elseList}}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:913:16
    def newTemplate(self, pos: 'Pos', line: int, name: str, pipe: Optional['PipeNode']) -> Optional['TemplateNode']:
        #         {
        #         	return &TemplateNode{tr: t, NodeType: NodeTemplate, Pos: pos, Line: line, Name: name, Pipe: pipe}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:35:16
    def Copy(self) -> Optional['Tree']:
        #         {
        #         	if t == nil {
        #         		return nil
        #         	}
        #         	return &Tree{
        #         		Name:		t.Name,
        #         		ParseName:	t.ParseName,
        #         		Root:		t.Root.CopyList(),
        #         		text:		t.text,
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:60:16
    def next(self) -> 'item':
        #         {
        #         	if t.peekCount > 0 {
        #         		t.peekCount--
        #         	} else {
        #         		t.token[0] = t.lex.nextItem()
        #         	}
        #         	return t.token[t.peekCount]
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:70:16
    def backup(self) -> None:
        #         {
        #         	t.peekCount++
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:76:16
    def backup2(self, t1: 'item') -> None:
        #         {
        #         	t.token[1] = t1
        #         	t.peekCount = 2
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:83:16
    def backup3(self, t2: 'item', t1: 'item') -> None:
        #         {
        #         	t.token[1] = t1
        #         	t.token[2] = t2
        #         	t.peekCount = 3
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:90:16
    def peek(self) -> 'item':
        #         {
        #         	if t.peekCount > 0 {
        #         		return t.token[t.peekCount-1]
        #         	}
        #         	t.peekCount = 1
        #         	t.token[0] = t.lex.nextItem()
        #         	return t.token[0]
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:100:16
    def nextNonSpace(self) -> 'item':
        #         {
        #         	for {
        #         		token = t.next()
        #         		if token.typ != itemSpace {
        #         			break
        #         		}
        #         	}
        #         	return token
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:111:16
    def peekNonSpace(self) -> 'item':
        #         {
        #         	token := t.nextNonSpace()
        #         	t.backup()
        #         	return token
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:130:16
    def ErrorContext(self, n: 'Node') -> Tuple[str, str]:
        #         {
        #         	pos := int(n.Position())
        #         	tree := n.tree()
        #         	if tree == nil {
        #         		tree = t
        #         	}
        #         	text := tree.text[:pos]
        #         	byteNum := strings.LastIndex(text, "\n")
        #         	if byteNum == -1 {
        #         		byteNum = pos
        #         	} else {
        #         		byteNum++
        #         		byteNum = pos - byteNum
        #         	}
        #         	lineNum := 1 + strings.Count(text, "\n")
        #         	context = n.String()
        #         	return fmt.Sprintf("%!s(MISSING):%!d(MISSING):%!d(MISSING)", tree.ParseName, lineNum, byteNum), context
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:150:16
    def errorf(self, format: str, *args: Any) -> None:
        #         {
        #         	t.Root = nil
        #         	format = fmt.Sprintf("template: %!s(MISSING):%!d(MISSING): %!s(MISSING)", t.ParseName, t.token[0].line, format)
        #         	panic(fmt.Errorf(format, args...))
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:157:16
    def error(self, err: 'goext.error') -> None:
        #         {
        #         	t.errorf("%!s(MISSING)", err)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:162:16
    def expect(self, expected: 'itemType', context: str) -> 'item':
        #         {
        #         	token := t.nextNonSpace()
        #         	if token.typ != expected {
        #         		t.unexpected(token, context)
        #         	}
        #         	return token
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:171:16
    def expectOneOf(self, expected1: 'itemType', expected2: 'itemType', context: str) -> 'item':
        #         {
        #         	token := t.nextNonSpace()
        #         	if token.typ != expected1 && token.typ != expected2 {
        #         		t.unexpected(token, context)
        #         	}
        #         	return token
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:180:16
    def unexpected(self, token: 'item', context: str) -> None:
        #         {
        #         	t.errorf("unexpected %!s(MISSING) in %!s(MISSING)", token, context)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:185:16
    def recover(self, errp: Optional['goext.error']) -> None:
        #         {
        #         	e := recover()
        #         	if e != nil {
        #         		if _, ok := e.(runtime.Error); ok {
        #         			panic(e)
        #         		}
        #         		if t != nil {
        #         			t.lex.drain()
        #         			t.stopParse()
        #         		}
        #         		*errp = e.(error)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:200:16
    def startParse(self, funcs: List[Dict[str, Any]], lex: Optional['lexer'], treeSet: Dict[str, Optional['Tree']]) -> None:
        #         {
        #         	t.Root = nil
        #         	t.lex = lex
        #         	t.vars = []string{"$"}
        #         	t.funcs = funcs
        #         	t.treeSet = treeSet
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:209:16
    def stopParse(self) -> None:
        #         {
        #         	t.lex = nil
        #         	t.vars = nil
        #         	t.funcs = nil
        #         	t.treeSet = nil
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:220:16
    def Parse(self, text: str, leftDelim: str, rightDelim: str, treeSet: Dict[str, Optional['Tree']], *funcs: Dict[str, Any]) -> Tuple[Optional['Tree'], 'goext.error']:
        #         {
        #         	defer t.recover(&err)
        #         	t.ParseName = t.Name
        #         	t.startParse(funcs, lex(t.Name, text, leftDelim, rightDelim), treeSet)
        #         	t.text = text
        #         	t.parse()
        #         	t.add()
        #         	t.stopParse()
        #         	return t, nil
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:232:16
    def add(self) -> None:
        #         {
        #         	tree := t.treeSet[t.Name]
        #         	if tree == nil || IsEmptyTree(tree.Root) {
        #         		t.treeSet[t.Name] = t
        #         		return
        #         	}
        #         	if !IsEmptyTree(t.Root) {
        #         		t.errorf("template: multiple definition of template %!q(MISSING)", t.Name)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:271:16
    def parse(self) -> None:
        #         {
        #         	t.Root = t.newList(t.peek().pos)
        #         	for t.peek().typ != itemEOF {
        #         		if t.peek().typ == itemLeftDelim {
        #         			delim := t.next()
        #         			if t.nextNonSpace().typ == itemDefine {
        #         				newT := New("definition")
        #         				newT.text = t.text
        #         				newT.ParseName = t.ParseName
        #         				newT.startParse(t.funcs, t.lex, t.treeSet)
        #         				newT.parseDefinition()
        #         				continue
        #         			}
        #         			t.backup2(delim)
        #         		}
        #         		switch n := t.textOrAction(); n.Type() {
        #         		case nodeEnd, nodeElse:
        #         			t.errorf("unexpected %!s(MISSING)", n)
        #         		default:
        #         			t.Root.append(n)
        #         		}
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:298:16
    def parseDefinition(self) -> None:
        #         {
        #         	const context = "define clause"
        #         	name := t.expectOneOf(itemString, itemRawString, context)
        #         	var err error
        #         	t.Name, err = strconv.Unquote(name.val)
        #         	if err != nil {
        #         		t.error(err)
        #         	}
        #         	t.expect(itemRightDelim, context)
        #         	var end Node
        #         	t.Root, end = t.itemList()
        #         	if end.Type() != nodeEnd {
        #         		t.errorf("unexpected %!s(MISSING) in %!s(MISSING)", end, context)
        #         	}
        #         	t.add()
        #         	t.stopParse()
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:319:16
    def itemList(self) -> Tuple[Optional['ListNode'], 'Node']:
        #         {
        #         	list = t.newList(t.peekNonSpace().pos)
        #         	for t.peekNonSpace().typ != itemEOF {
        #         		n := t.textOrAction()
        #         		switch n.Type() {
        #         		case nodeEnd, nodeElse:
        #         			return list, n
        #         		}
        #         		list.append(n)
        #         	}
        #         	t.errorf("unexpected EOF")
        #         	return
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:335:16
    def textOrAction(self) -> 'Node':
        #         {
        #         	switch token := t.nextNonSpace(); token.typ {
        #         	case itemText:
        #         		return t.newText(token.pos, token.val)
        #         	case itemLeftDelim:
        #         		return t.action()
        #         	default:
        #         		t.unexpected(token, "input")
        #         	}
        #         	return nil
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:352:16
    def action(self) -> 'Node':
        #         {
        #         	switch token := t.nextNonSpace(); token.typ {
        #         	case itemBlock:
        #         		return t.blockControl()
        #         	case itemElse:
        #         		return t.elseControl()
        #         	case itemEnd:
        #         		return t.endControl()
        #         	case itemIf:
        #         		return t.ifControl()
        #         	case itemRange:
        #         		return t.rangeControl()
        #         	case itemTemplate:
        #         		return t.templateControl()
        #         	case itemWith:
        #         		return t.withControl()
        #         	}
        #         	t.backup()
        #         	token := t.peek()
        #         
        #         	return t.newAction(token.pos, token.line, t.pipeline("command"))
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:377:16
    def pipeline(self, context: str) -> Optional['PipeNode']:
        #         {
        #         	token := t.peekNonSpace()
        #         	pipe = t.newPipeline(token.pos, token.line, nil)
        #         
        #         decls:
        #         	if v := t.peekNonSpace(); v.typ == itemVariable {
        #         		t.next()
        #         
        #         		tokenAfterVariable := t.peek()
        #         		next := t.peekNonSpace()
        #         		switch {
        #         		case next.typ == itemAssign, next.typ == itemDeclare:
        #         			pipe.IsAssign = next.typ == itemAssign
        #         			t.nextNonSpace()
        #         			pipe.Decl = append(pipe.Decl, t.newVariable(v.pos, v.val))
        #         			t.vars = append(t.vars, v.val)
        #         		case next.typ == itemChar && next.val == ",":
        #         			t.nextNonSpace()
        #         			pipe.Decl = append(pipe.Decl, t.newVariable(v.pos, v.val))
        #         			t.vars = append(t.vars, v.val)
        #         			if context == "range" && len(pipe.Decl) < 2 {
        #         				switch t.peekNonSpace().typ {
        #         				case itemVariable, itemRightDelim, itemRightParen:
        #         
        #         					goto decls
        #         				default:
        #         					t.errorf("range can only initialize variables")
        #         				}
        #         			}
        #         			t.errorf("too many declarations in %!s(MISSING)", context)
        #         		case tokenAfterVariable.typ == itemSpace:
        #         			t.backup3(v, tokenAfterVariable)
        #         		default:
        #         			t.backup2(v)
        #         		}
        #         	}
        #         	for {
        #         		switch token := t.nextNonSpace(); token.typ {
        #         		case itemRightDelim, itemRightParen:
        #         
        #         			t.checkPipeline(pipe, context)
        #         			if token.typ == itemRightParen {
        #         				t.backup()
        #         			}
        #         			return
        #         		case itemBool, itemCharConstant, itemComplex, itemDot, itemField, itemIdentifier,
        #         			itemNumber, itemNil, itemRawString, itemString, itemVariable, itemLeftParen:
        #         			t.backup()
        #         			pipe.append(t.command())
        #         		default:
        #         			t.unexpected(token, context)
        #         		}
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:435:16
    def checkPipeline(self, pipe: Optional['PipeNode'], context: str) -> None:
        #         {
        #         
        #         	if len(pipe.Cmds) == 0 {
        #         		t.errorf("missing value for %!s(MISSING)", context)
        #         	}
        #         
        #         	for i, c := range pipe.Cmds[1:] {
        #         		switch c.Args[0].Type() {
        #         		case NodeBool, NodeDot, NodeNil, NodeNumber, NodeString:
        #         
        #         			t.errorf("non executable command in pipeline stage %!d(MISSING)", i+2)
        #         		}
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:450:16
    def parseControl(self, allowElseIf: bool, context: str) -> Tuple['Pos', int, Optional['PipeNode'], Optional['ListNode'], Optional['ListNode']]:
        #         {
        #         	defer t.popVars(len(t.vars))
        #         	pipe = t.pipeline(context)
        #         	var next Node
        #         	list, next = t.itemList()
        #         	switch next.Type() {
        #         	case nodeEnd:
        #         	case nodeElse:
        #         		if allowElseIf {
        #         
        #         			if t.peek().typ == itemIf {
        #         				t.next()
        #         				elseList = t.newList(next.Position())
        #         				elseList.append(t.ifControl())
        #         
        #         				break
        #         			}
        #         		}
        #         		elseList, next = t.itemList()
        #         		if next.Type() != nodeEnd {
        #         			t.errorf("expected end; found %!s(MISSING)", next)
        #         		}
        #         	}
        #         	return pipe.Position(), pipe.Line, pipe, list, elseList
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:487:16
    def ifControl(self) -> 'Node':
        #         {
        #         	return t.newIf(t.parseControl(true, "if"))
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:495:16
    def rangeControl(self) -> 'Node':
        #         {
        #         	return t.newRange(t.parseControl(false, "range"))
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:503:16
    def withControl(self) -> 'Node':
        #         {
        #         	return t.newWith(t.parseControl(false, "with"))
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:510:16
    def endControl(self) -> 'Node':
        #         {
        #         	return t.newEnd(t.expect(itemRightDelim, "end").pos)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:517:16
    def elseControl(self) -> 'Node':
        #         {
        #         
        #         	peek := t.peekNonSpace()
        #         	if peek.typ == itemIf {
        #         
        #         		return t.newElse(peek.pos, peek.line)
        #         	}
        #         	token := t.expect(itemRightDelim, "else")
        #         	return t.newElse(token.pos, token.line)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:533:16
    def blockControl(self) -> 'Node':
        #         {
        #         	const context = "block clause"
        #         
        #         	token := t.nextNonSpace()
        #         	name := t.parseTemplateName(token, context)
        #         	pipe := t.pipeline(context)
        #         
        #         	block := New(name)
        #         	block.text = t.text
        #         	block.ParseName = t.ParseName
        #         	block.startParse(t.funcs, t.lex, t.treeSet)
        #         	var end Node
        #         	block.Root, end = block.itemList()
        #         	if end.Type() != nodeEnd {
        #         		t.errorf("unexpected %!s(MISSING) in %!s(MISSING)", end, context)
        #         	}
        #         	block.add()
        #         	block.stopParse()
        #         
        #         	return t.newTemplate(token.pos, token.line, name, pipe)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:559:16
    def templateControl(self) -> 'Node':
        #         {
        #         	const context = "template clause"
        #         	token := t.nextNonSpace()
        #         	name := t.parseTemplateName(token, context)
        #         	var pipe *PipeNode
        #         	if t.nextNonSpace().typ != itemRightDelim {
        #         		t.backup()
        #         
        #         		pipe = t.pipeline(context)
        #         	}
        #         	return t.newTemplate(token.pos, token.line, name, pipe)
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:572:16
    def parseTemplateName(self, token: 'item', context: str) -> str:
        #         {
        #         	switch token.typ {
        #         	case itemString, itemRawString:
        #         		s, err := strconv.Unquote(token.val)
        #         		if err != nil {
        #         			t.error(err)
        #         		}
        #         		name = s
        #         	default:
        #         		t.unexpected(token, context)
        #         	}
        #         	return
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:590:16
    def command(self) -> Optional['CommandNode']:
        #         {
        #         	cmd := t.newCommand(t.peekNonSpace().pos)
        #         	for {
        #         		t.peekNonSpace()
        #         		operand := t.operand()
        #         		if operand != nil {
        #         			cmd.append(operand)
        #         		}
        #         		switch token := t.next(); token.typ {
        #         		case itemSpace:
        #         			continue
        #         		case itemError:
        #         			t.errorf("%!s(MISSING)", token.val)
        #         		case itemRightDelim, itemRightParen:
        #         			t.backup()
        #         		case itemPipe:
        #         		default:
        #         			t.errorf("unexpected %!s(MISSING) in operand", token)
        #         		}
        #         		break
        #         	}
        #         	if len(cmd.Args) == 0 {
        #         		t.errorf("empty command")
        #         	}
        #         	return cmd
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:622:16
    def operand(self) -> 'Node':
        #         {
        #         	node := t.term()
        #         	if node == nil {
        #         		return nil
        #         	}
        #         	if t.peek().typ == itemField {
        #         		chain := t.newChain(t.peek().pos, node)
        #         		for t.peek().typ == itemField {
        #         			chain.Add(t.next().val)
        #         		}
        #         
        #         		switch node.Type() {
        #         		case NodeField:
        #         			node = t.newField(chain.Position(), chain.String())
        #         		case NodeVariable:
        #         			node = t.newVariable(chain.Position(), chain.String())
        #         		case NodeBool, NodeString, NodeNumber, NodeNil, NodeDot:
        #         			t.errorf("unexpected . after term %!q(MISSING)", node.String())
        #         		default:
        #         			node = chain
        #         		}
        #         	}
        #         	return node
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:660:16
    def term(self) -> 'Node':
        #         {
        #         	switch token := t.nextNonSpace(); token.typ {
        #         	case itemError:
        #         		t.errorf("%!s(MISSING)", token.val)
        #         	case itemIdentifier:
        #         		if !t.hasFunction(token.val) {
        #         			t.errorf("function %!q(MISSING) not defined", token.val)
        #         		}
        #         		return NewIdentifier(token.val).SetTree(t).SetPos(token.pos)
        #         	case itemDot:
        #         		return t.newDot(token.pos)
        #         	case itemNil:
        #         		return t.newNil(token.pos)
        #         	case itemVariable:
        #         		return t.useVar(token.pos, token.val)
        #         	case itemField:
        #         		return t.newField(token.pos, token.val)
        #         	case itemBool:
        #         		return t.newBool(token.pos, token.val == "true")
        #         	case itemCharConstant, itemComplex, itemNumber:
        #         		number, err := t.newNumber(token.pos, token.val, token.typ)
        #         		if err != nil {
        #         			t.error(err)
        #         		}
        #         		return number
        #         	case itemLeftParen:
        #         		pipe := t.pipeline("parenthesized pipeline")
        #         		if token := t.next(); token.typ != itemRightParen {
        #         			t.errorf("unclosed right paren: unexpected %!s(MISSING)", token)
        #         		}
        #         		return pipe
        #         	case itemString, itemRawString:
        #         		s, err := strconv.Unquote(token.val)
        #         		if err != nil {
        #         			t.error(err)
        #         		}
        #         		return t.newString(token.pos, token.val, s)
        #         	}
        #         	t.backup()
        #         	return nil
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:703:16
    def hasFunction(self, name: str) -> bool:
        #         {
        #         	for _, funcMap := range t.funcs {
        #         		if funcMap == nil {
        #         			continue
        #         		}
        #         		if funcMap[name] != nil {
        #         			return true
        #         		}
        #         	}
        #         	return false
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:716:16
    def popVars(self, n: int) -> None:
        #         {
        #         	t.vars = t.vars[:n]
        #         }
        pass

    # c:\go\src\text\template\parse\parse.go:722:16
    def useVar(self, pos: 'Pos', name: str) -> 'Node':
        #         {
        #         	v := t.newVariable(pos, name)
        #         	for _, varName := range t.vars {
        #         		if varName == v.Ident[0] {
        #         			return v
        #         		}
        #         	}
        #         	t.errorf("undefined variable %!q(MISSING)", v.Ident[0])
        #         	return nil
        #         }
        pass


# c:\go\src\text\template\parse\node.go:354:6
class VariableNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: Optional[List[str]]  # Variable name and fields in lexical order.

    # c:\go\src\text\template\parse\node.go:365:24
    def String(self) -> str:
        #         {
        #         	var sb strings.Builder
        #         	v.writeTo(&sb)
        #         	return sb.String()
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:371:24
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	for i, id := range v.Ident {
        #         		if i > 0 {
        #         			sb.WriteByte('.')
        #         		}
        #         		sb.WriteString(id)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:380:24
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return v.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:384:24
    def Copy(self) -> 'Node':
        #         {
        #         	return &VariableNode{tr: v.tr, NodeType: NodeVariable, Pos: v.Pos, Ident: append([]string{}, v.Ident...)}
        #         }
        pass


# c:\go\src\text\template\parse\node.go:891:6
class WithNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:899:20
    def Copy(self) -> 'Node':
        #         {
        #         	return w.tr.newWith(w.Pos, w.Line, w.Pipe.CopyPipe(), w.List.CopyList(), w.ElseList.CopyList())
        #         }
        pass


# c:\go\src\text\template\parse\node.go:774:6
class elseNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.

    # c:\go\src\text\template\parse\node.go:785:20
    def Type(self) -> 'NodeType':
        #         {
        #         	return nodeElse
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:789:20
    def String(self) -> str:
        #         {
        #         	return "{{else}}"
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:793:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(e.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:797:20
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return e.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:801:20
    def Copy(self) -> 'Node':
        #         {
        #         	return e.tr.newElse(e.Pos, e.Line)
        #         }
        pass


# c:\go\src\text\template\parse\node.go:747:6
class endNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:757:19
    def String(self) -> str:
        #         {
        #         	return "{{end}}"
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:761:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        #         {
        #         	sb.WriteString(e.String())
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:765:19
    def tree(self) -> Optional['Tree']:
        #         {
        #         	return e.tr
        #         }
        pass

    # c:\go\src\text\template\parse\node.go:769:19
    def Copy(self) -> 'Node':
        #         {
        #         	return e.tr.newEnd(e.Pos)
        #         }
        pass


# c:\go\src\text\template\parse\lex.go:15:6
class item:
    typ: 'itemType'  # The type of this item.
    pos: 'Pos'  # The starting position, in bytes, of this item in the input string.
    val: str  # The value of this item.
    line: int  # The line number at the start of this item.

    # c:\go\src\text\template\parse\lex.go:22:15
    def String(self) -> str:
        #         {
        #         	switch {
        #         	case i.typ == itemEOF:
        #         		return "EOF"
        #         	case i.typ == itemError:
        #         		return i.val
        #         	case i.typ > itemKeyword:
        #         		return fmt.Sprintf("<%!s(MISSING)>", i.val)
        #         	case len(i.val) > 10:
        #         		return fmt.Sprintf("%!q(MISSING)...", i.val)
        #         	}
        #         	return fmt.Sprintf("%!q(MISSING)", i.val)
        #         }
        pass


# c:\go\src\text\template\parse\lex.go:109:6
class lexer:
    name: str  # the name of the input; used only for error reports
    input: str  # the string being scanned
    leftDelim: str  # start of action
    rightDelim: str  # end of action
    trimRightDelim: str  # end of action with trim marker
    pos: 'Pos'  # current position in the input
    start: 'Pos'  # start position of this item
    width: 'Pos'  # width of last rune read from input
    items: queue.LifoQueue  # channel of scanned items
    parenDepth: int  # nesting depth of ( ) exprs
    line: int  # 1+number of newlines seen
    startLine: int  # start line of this item

    # c:\go\src\text\template\parse\lex.go:125:17
    def next(self) -> int:
        #         {
        #         	if int(l.pos) >= len(l.input) {
        #         		l.width = 0
        #         		return eof
        #         	}
        #         	r, w := utf8.DecodeRuneInString(l.input[l.pos:])
        #         	l.width = Pos(w)
        #         	l.pos += l.width
        #         	if r == '\n' {
        #         		l.line++
        #         	}
        #         	return r
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:140:17
    def peek(self) -> int:
        #         {
        #         	r := l.next()
        #         	l.backup()
        #         	return r
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:147:17
    def backup(self) -> None:
        #         {
        #         	l.pos -= l.width
        #         
        #         	if l.width == 1 && l.input[l.pos] == '\n' {
        #         		l.line--
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:156:17
    def emit(self, t: 'itemType') -> None:
        #         {
        #         	l.items <- item{t, l.start, l.input[l.start:l.pos], l.startLine}
        #         	l.start = l.pos
        #         	l.startLine = l.line
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:163:17
    def ignore(self) -> None:
        #         {
        #         	l.line += strings.Count(l.input[l.start:l.pos], "\n")
        #         	l.start = l.pos
        #         	l.startLine = l.line
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:170:17
    def accept(self, valid: str) -> bool:
        #         {
        #         	if strings.ContainsRune(valid, l.next()) {
        #         		return true
        #         	}
        #         	l.backup()
        #         	return false
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:179:17
    def acceptRun(self, valid: str) -> None:
        #         {
        #         	for strings.ContainsRune(valid, l.next()) {
        #         	}
        #         	l.backup()
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:187:17
    def errorf(self, format: str, *args: Any) -> 'stateFn':
        #         {
        #         	l.items <- item{itemError, l.start, fmt.Sprintf(format, args...), l.startLine}
        #         	return nil
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:194:17
    def nextItem(self) -> 'item':
        #         {
        #         	return <-l.items
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:200:17
    def drain(self) -> None:
        #         {
        #         	for range l.items {
        #         	}
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:228:17
    def run(self) -> None:
        #         {
        #         	for state := lexText; state != nil; {
        #         		state = state(l)
        #         	}
        #         	close(l.items)
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:279:17
    def atRightDelim(self) -> Tuple[bool, bool]:
        #         {
        #         	if strings.HasPrefix(l.input[l.pos:], l.trimRightDelim) {
        #         		return true, true
        #         	}
        #         	if strings.HasPrefix(l.input[l.pos:], l.rightDelim) {
        #         		return true, false
        #         	}
        #         	return false, false
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:521:17
    def atTerminator(self) -> bool:
        #         {
        #         	r := l.peek()
        #         	if isSpace(r) || isEndOfLine(r) {
        #         		return true
        #         	}
        #         	switch r {
        #         	case eof, '.', ',', '|', ':', ')', '(':
        #         		return true
        #         	}
        #         
        #         	if rd, _ := utf8.DecodeRuneInString(l.rightDelim); rd == r {
        #         		return true
        #         	}
        #         	return false
        #         }
        pass

    # c:\go\src\text\template\parse\lex.go:580:17
    def scanNumber(self) -> bool:
        #         {
        #         
        #         	l.accept("+-")
        #         
        #         	digits := "0123456789_"
        #         	if l.accept("0") {
        #         
        #         		if l.accept("xX") {
        #         			digits = "0123456789abcdefABCDEF_"
        #         		} else if l.accept("oO") {
        #         			digits = "01234567_"
        #         		} else if l.accept("bB") {
        #         			digits = "01_"
        #         		}
        #         	}
        #         	l.acceptRun(digits)
        #         	if l.accept(".") {
        #         		l.acceptRun(digits)
        #         	}
        #         	if len(digits) == 10+1 && l.accept("eE") {
        #         		l.accept("+-")
        #         		l.acceptRun("0123456789_")
        #         	}
        #         	if len(digits) == 16+6+1 && l.accept("pP") {
        #         		l.accept("+-")
        #         		l.acceptRun("0123456789_")
        #         	}
        #         
        #         	l.accept("i")
        #         
        #         	if isAlphaNumeric(l.peek()) {
        #         		l.next()
        #         		return false
        #         	}
        #         	return true
        #         }
        pass


#
# FUNCS
#


# c:\go\src\text\template\parse\parse.go:244:6
def IsEmptyTree(n: 'Node') -> bool:
    #     {
    #     	switch n := n.(type) {
    #     	case nil:
    #     		return true
    #     	case *ActionNode:
    #     	case *IfNode:
    #     	case *ListNode:
    #     		for _, node := range n.Nodes {
    #     			if !IsEmptyTree(node) {
    #     				return false
    #     			}
    #     		}
    #     		return true
    #     	case *RangeNode:
    #     	case *TemplateNode:
    #     	case *TextNode:
    #     		return len(bytes.TrimSpace(n.Text)) == 0
    #     	case *WithNode:
    #     	default:
    #     		panic("unknown node: " + n.String())
    #     	}
    #     	return false
    #     }
    pass


# c:\go\src\text\template\parse\parse.go:120:6
def New(name: str, *funcs: Dict[str, Any]) -> Optional['Tree']:
    #     {
    #     	return &Tree{
    #     		Name:	name,
    #     		funcs:	funcs,
    #     	}
    #     }
    pass


# c:\go\src\text\template\parse\node.go:316:6
def NewIdentifier(ident: str) -> Optional['IdentifierNode']:
    #     {
    #     	return &IdentifierNode{NodeType: NodeIdentifier, Ident: ident}
    #     }
    pass


# c:\go\src\text\template\parse\parse.go:51:6
def Parse(name: str, text: str, leftDelim: str, rightDelim: str, *funcs: Dict[str, Any]) -> Tuple[Dict[str, Optional['Tree']], 'goext.error']:
    #     {
    #     	treeSet := make(map[string]*Tree)
    #     	t := New(name)
    #     	t.text = text
    #     	_, err := t.Parse(text, leftDelim, rightDelim, treeSet, funcs...)
    #     	return treeSet, err
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:663:6
def isAlphaNumeric(r: int) -> bool:
    #     {
    #     	return r == '_' || unicode.IsLetter(r) || unicode.IsDigit(r)
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:658:6
def isEndOfLine(r: int) -> bool:
    #     {
    #     	return r == '\r' || r == '\n'
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:653:6
def isSpace(r: int) -> bool:
    #     {
    #     	return r == ' ' || r == '\t'
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:290:6
def leftTrimLength(s: str) -> 'Pos':
    #     {
    #     	return Pos(len(s) - len(strings.TrimLeft(s, spaceChars)))
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:206:6
def lex(name: str, input: str, left: str, right: str) -> Optional['lexer']:
    #     {
    #     	if left == "" {
    #     		left = leftDelim
    #     	}
    #     	if right == "" {
    #     		right = rightDelim
    #     	}
    #     	l := &lexer{
    #     		name:		name,
    #     		input:		input,
    #     		leftDelim:	left,
    #     		rightDelim:	right,
    #     		trimRightDelim:	rightTrimMarker + right,
    #     		items:		make(chan item),
    #     		line:		1,
    #     		startLine:	1,
    #     	}
    #     	go l.run()
    #     	return l
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:541:6
def lexChar(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     Loop:
    #     	for {
    #     		switch l.next() {
    #     		case '\\':
    #     			if r := l.next(); r != eof && r != '\n' {
    #     				break
    #     			}
    #     			fallthrough
    #     		case eof, '\n':
    #     			return l.errorf("unterminated character constant")
    #     		case '\'':
    #     			break Loop
    #     		}
    #     	}
    #     	l.emit(itemCharConstant)
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:315:6
def lexComment(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	l.pos += Pos(len(leftComment))
    #     	i := strings.Index(l.input[l.pos:], rightComment)
    #     	if i < 0 {
    #     		return l.errorf("unclosed comment")
    #     	}
    #     	l.pos += Pos(i + len(rightComment))
    #     	delim, trimSpace := l.atRightDelim()
    #     	if !delim {
    #     		return l.errorf("comment ends before closing delimiter")
    #     	}
    #     	if trimSpace {
    #     		l.pos += trimMarkerLen
    #     	}
    #     	l.pos += Pos(len(l.rightDelim))
    #     	if trimSpace {
    #     		l.pos += leftTrimLength(l.input[l.pos:])
    #     	}
    #     	l.ignore()
    #     	return lexText
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:477:6
def lexField(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	return lexFieldOrVariable(l, itemField)
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:493:6
def lexFieldOrVariable(l: Optional['lexer'], typ: 'itemType') -> 'stateFn':
    #     {
    #     	if l.atTerminator() {
    #     		if typ == itemVariable {
    #     			l.emit(itemVariable)
    #     		} else {
    #     			l.emit(itemDot)
    #     		}
    #     		return lexInsideAction
    #     	}
    #     	var r rune
    #     	for {
    #     		r = l.next()
    #     		if !isAlphaNumeric(r) {
    #     			l.backup()
    #     			break
    #     		}
    #     	}
    #     	if !l.atTerminator() {
    #     		return l.errorf("bad character %!U(MISSING)", r)
    #     	}
    #     	l.emit(typ)
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:447:6
def lexIdentifier(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     Loop:
    #     	for {
    #     		switch r := l.next(); {
    #     		case isAlphaNumeric(r):
    #     
    #     		default:
    #     			l.backup()
    #     			word := l.input[l.start:l.pos]
    #     			if !l.atTerminator() {
    #     				return l.errorf("bad character %!U(MISSING)", r)
    #     			}
    #     			switch {
    #     			case key[word] > itemKeyword:
    #     				l.emit(key[word])
    #     			case word[0] == '.':
    #     				l.emit(itemField)
    #     			case word == "true", word == "false":
    #     				l.emit(itemBool)
    #     			default:
    #     				l.emit(itemIdentifier)
    #     			}
    #     			break Loop
    #     		}
    #     	}
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:354:6
def lexInsideAction(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     
    #     	delim, _ := l.atRightDelim()
    #     	if delim {
    #     		if l.parenDepth == 0 {
    #     			return lexRightDelim
    #     		}
    #     		return l.errorf("unclosed left paren")
    #     	}
    #     	switch r := l.next(); {
    #     	case r == eof || isEndOfLine(r):
    #     		return l.errorf("unclosed action")
    #     	case isSpace(r):
    #     		l.backup()
    #     		return lexSpace
    #     	case r == '=':
    #     		l.emit(itemAssign)
    #     	case r == ':':
    #     		if l.next() != '=' {
    #     			return l.errorf("expected :=")
    #     		}
    #     		l.emit(itemDeclare)
    #     	case r == '|':
    #     		l.emit(itemPipe)
    #     	case r == '"':
    #     		return lexQuote
    #     	case r == '`':
    #     		return lexRawQuote
    #     	case r == '$':
    #     		return lexVariable
    #     	case r == '\'':
    #     		return lexChar
    #     	case r == '.':
    #     
    #     		if l.pos < Pos(len(l.input)) {
    #     			r := l.input[l.pos]
    #     			if r < '0' || '9' < r {
    #     				return lexField
    #     			}
    #     		}
    #     		fallthrough
    #     	case r == '+' || r == '-' || ('0' <= r && r <= '9'):
    #     		l.backup()
    #     		return lexNumber
    #     	case isAlphaNumeric(r):
    #     		l.backup()
    #     		return lexIdentifier
    #     	case r == '(':
    #     		l.emit(itemLeftParen)
    #     		l.parenDepth++
    #     	case r == ')':
    #     		l.emit(itemRightParen)
    #     		l.parenDepth--
    #     		if l.parenDepth < 0 {
    #     			return l.errorf("unexpected right paren %!U(MISSING)", r)
    #     		}
    #     	case r <= unicode.MaxASCII && unicode.IsPrint(r):
    #     		l.emit(itemChar)
    #     	default:
    #     		return l.errorf("unrecognized character in action: %!U(MISSING)", r)
    #     	}
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:295:6
def lexLeftDelim(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	l.pos += Pos(len(l.leftDelim))
    #     	trimSpace := strings.HasPrefix(l.input[l.pos:], leftTrimMarker)
    #     	afterMarker := Pos(0)
    #     	if trimSpace {
    #     		afterMarker = trimMarkerLen
    #     	}
    #     	if strings.HasPrefix(l.input[l.pos+afterMarker:], leftComment) {
    #     		l.pos += afterMarker
    #     		l.ignore()
    #     		return lexComment
    #     	}
    #     	l.emit(itemLeftDelim)
    #     	l.pos += afterMarker
    #     	l.ignore()
    #     	l.parenDepth = 0
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:564:6
def lexNumber(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	if !l.scanNumber() {
    #     		return l.errorf("bad number syntax: %!q(MISSING)", l.input[l.start:l.pos])
    #     	}
    #     	if sign := l.peek(); sign == '+' || sign == '-' {
    #     
    #     		if !l.scanNumber() || l.input[l.pos-1] != 'i' {
    #     			return l.errorf("bad number syntax: %!q(MISSING)", l.input[l.start:l.pos])
    #     		}
    #     		l.emit(itemComplex)
    #     	} else {
    #     		l.emit(itemNumber)
    #     	}
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:618:6
def lexQuote(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     Loop:
    #     	for {
    #     		switch l.next() {
    #     		case '\\':
    #     			if r := l.next(); r != eof && r != '\n' {
    #     				break
    #     			}
    #     			fallthrough
    #     		case eof, '\n':
    #     			return l.errorf("unterminated quoted string")
    #     		case '"':
    #     			break Loop
    #     		}
    #     	}
    #     	l.emit(itemString)
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:638:6
def lexRawQuote(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     Loop:
    #     	for {
    #     		switch l.next() {
    #     		case eof:
    #     			return l.errorf("unterminated raw quoted string")
    #     		case '`':
    #     			break Loop
    #     		}
    #     	}
    #     	l.emit(itemRawString)
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:338:6
def lexRightDelim(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	trimSpace := strings.HasPrefix(l.input[l.pos:], rightTrimMarker)
    #     	if trimSpace {
    #     		l.pos += trimMarkerLen
    #     		l.ignore()
    #     	}
    #     	l.pos += Pos(len(l.rightDelim))
    #     	l.emit(itemRightDelim)
    #     	if trimSpace {
    #     		l.pos += leftTrimLength(l.input[l.pos:])
    #     		l.ignore()
    #     	}
    #     	return lexText
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:423:6
def lexSpace(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	var r rune
    #     	var numSpaces int
    #     	for {
    #     		r = l.peek()
    #     		if !isSpace(r) {
    #     			break
    #     		}
    #     		l.next()
    #     		numSpaces++
    #     	}
    #     
    #     	if strings.HasPrefix(l.input[l.pos-1:], l.trimRightDelim) {
    #     		l.backup()
    #     		if numSpaces == 1 {
    #     			return lexRightDelim
    #     		}
    #     	}
    #     	l.emit(itemSpace)
    #     	return lexInsideAction
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:245:6
def lexText(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	l.width = 0
    #     	if x := strings.Index(l.input[l.pos:], l.leftDelim); x >= 0 {
    #     		ldn := Pos(len(l.leftDelim))
    #     		l.pos += Pos(x)
    #     		trimLength := Pos(0)
    #     		if strings.HasPrefix(l.input[l.pos+ldn:], leftTrimMarker) {
    #     			trimLength = rightTrimLength(l.input[l.start:l.pos])
    #     		}
    #     		l.pos -= trimLength
    #     		if l.pos > l.start {
    #     			l.line += strings.Count(l.input[l.start:l.pos], "\n")
    #     			l.emit(itemText)
    #     		}
    #     		l.pos += trimLength
    #     		l.ignore()
    #     		return lexLeftDelim
    #     	}
    #     	l.pos = Pos(len(l.input))
    #     
    #     	if l.pos > l.start {
    #     		l.line += strings.Count(l.input[l.start:l.pos], "\n")
    #     		l.emit(itemText)
    #     	}
    #     	l.emit(itemEOF)
    #     	return nil
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:483:6
def lexVariable(l: Optional['lexer']) -> 'stateFn':
    #     {
    #     	if l.atTerminator() {
    #     		l.emit(itemVariable)
    #     		return lexInsideAction
    #     	}
    #     	return lexFieldOrVariable(l, itemVariable)
    #     }
    pass


# c:\go\src\text\template\parse\lex.go:274:6
def rightTrimLength(s: str) -> 'Pos':
    #     {
    #     	return Pos(len(s) - len(strings.TrimRight(s, spaceChars)))
    #     }
    pass

