# type: ignore
# package: text/template/parse

from enum import Enum
from typing import Callable, Optional, List, Dict, Any, Tuple
import queue
from . import goext


#
# ENUMS
#


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
        pass


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
        pass

    # c:\go\src\text\template\parse\node.go:27:2
    def Position(self) -> 'Pos':  # byte position of start of node in full original input string
        pass

    # c:\go\src\text\template\parse\node.go:22:2
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:21:2
    def Type(self) -> 'NodeType':
        pass

    # c:\go\src\text\template\parse\node.go:30:2
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:32:2
    def writeTo(self, p0: Optional[goext.strings_Builder]) -> None:
        pass


#
# STRUCTS
#


# c:\go\src\text\template\parse\node.go:40:6
class Pos:

    # c:\go\src\text\template\parse\node.go:42:14
    def Position(self) -> 'Pos':
        pass


# c:\go\src\text\template\parse\node.go:222:6
class ActionNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    Pipe: Optional['PipeNode']  # The pipeline in the action.

    # c:\go\src\text\template\parse\node.go:234:22
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:240:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:246:22
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:250:22
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:547:6
class BoolNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    True_: bool  # The value of the boolean constant.

    # c:\go\src\text\template\parse\node.go:558:20
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:565:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:569:20
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:573:20
    def Copy(self) -> 'Node':
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
        pass

    # c:\go\src\text\template\parse\node.go:822:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:847:22
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:851:22
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:494:6
class ChainNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Node: 'Node'
    Field: Optional[List[str]]  # The identifiers in lexical order.

    # c:\go\src\text\template\parse\node.go:507:21
    def Add(self, field: str) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:518:21
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:524:21
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:538:21
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:542:21
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:256:6
class CommandNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Args: Optional[List['Node']]  # Arguments in lexical order: Identifier, field, or constant.

    # c:\go\src\text\template\parse\node.go:267:23
    def append(self, arg: 'Node') -> None:
        pass

    # c:\go\src\text\template\parse\node.go:271:23
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:277:23
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:292:23
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:296:23
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:389:6
class DotNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:399:19
    def Type(self) -> 'NodeType':
        pass

    # c:\go\src\text\template\parse\node.go:406:19
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:410:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:414:19
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:418:19
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:459:6
class FieldNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: Optional[List[str]]  # The identifiers in lexical order.

    # c:\go\src\text\template\parse\node.go:470:21
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:476:21
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:483:21
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:487:21
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:308:6
class IdentifierNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: str  # The identifier's name.

    # c:\go\src\text\template\parse\node.go:323:26
    def SetPos(self, pos: 'Pos') -> Optional['IdentifierNode']:
        pass

    # c:\go\src\text\template\parse\node.go:331:26
    def SetTree(self, t: Optional['Tree']) -> Optional['IdentifierNode']:
        pass

    # c:\go\src\text\template\parse\node.go:336:26
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:340:26
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:344:26
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:348:26
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:865:6
class IfNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:873:18
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:78:6
class ListNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Nodes: Optional[List['Node']]  # The element nodes in lexical order.

    # c:\go\src\text\template\parse\node.go:89:20
    def append(self, n: 'Node') -> None:
        pass

    # c:\go\src\text\template\parse\node.go:93:20
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:97:20
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:103:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:109:20
    def CopyList(self) -> Optional['ListNode']:
        pass

    # c:\go\src\text\template\parse\node.go:120:20
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:423:6
class NilNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:433:19
    def Type(self) -> 'NodeType':
        pass

    # c:\go\src\text\template\parse\node.go:440:19
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:444:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:448:19
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:452:19
    def Copy(self) -> 'Node':
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
        pass

    # c:\go\src\text\template\parse\node.go:698:22
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:702:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:706:22
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:710:22
    def Copy(self) -> 'Node':
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
        pass

    # c:\go\src\text\template\parse\node.go:171:20
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:177:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:195:20
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:199:20
    def CopyPipe(self) -> Optional['PipeNode']:
        pass

    # c:\go\src\text\template\parse\node.go:215:20
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:878:6
class RangeNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:886:21
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:717:6
class StringNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Quoted: str  # The original text of the string, with quotes.
    Text: str  # The string, after quote processing.

    # c:\go\src\text\template\parse\node.go:729:22
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:733:22
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:737:22
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:741:22
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:904:6
class TemplateNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.
    Name: str  # The name of the template (unquoted).
    Pipe: Optional['PipeNode']  # The command to evaluate as dot for the template.

    # c:\go\src\text\template\parse\node.go:917:24
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:923:24
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:933:24
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:937:24
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:125:6
class TextNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Text: Optional[List[int]]  # The text; may span newlines.

    # c:\go\src\text\template\parse\node.go:136:20
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:140:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:144:20
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:148:20
    def Copy(self) -> 'Node':
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
        pass

    # c:\go\src\text\template\parse\node.go:132:16
    def newText(self, pos: 'Pos', text: str) -> Optional['TextNode']:
        pass

    # c:\go\src\text\template\parse\node.go:163:16
    def newPipeline(self, pos: 'Pos', line: int, vars: List[Optional['VariableNode']]) -> Optional['PipeNode']:
        pass

    # c:\go\src\text\template\parse\node.go:230:16
    def newAction(self, pos: 'Pos', line: int, pipe: Optional['PipeNode']) -> Optional['ActionNode']:
        pass

    # c:\go\src\text\template\parse\node.go:263:16
    def newCommand(self, pos: 'Pos') -> Optional['CommandNode']:
        pass

    # c:\go\src\text\template\parse\node.go:361:16
    def newVariable(self, pos: 'Pos', ident: str) -> Optional['VariableNode']:
        pass

    # c:\go\src\text\template\parse\node.go:395:16
    def newDot(self, pos: 'Pos') -> Optional['DotNode']:
        pass

    # c:\go\src\text\template\parse\node.go:429:16
    def newNil(self, pos: 'Pos') -> Optional['NilNode']:
        pass

    # c:\go\src\text\template\parse\node.go:466:16
    def newField(self, pos: 'Pos', ident: str) -> Optional['FieldNode']:
        pass

    # c:\go\src\text\template\parse\node.go:502:16
    def newChain(self, pos: 'Pos', node: 'Node') -> Optional['ChainNode']:
        pass

    # c:\go\src\text\template\parse\node.go:554:16
    def newBool(self, pos: 'Pos', true: bool) -> Optional['BoolNode']:
        pass

    # c:\go\src\text\template\parse\node.go:595:16
    def newNumber(self, pos: 'Pos', text: str, typ: 'itemType') -> Tuple[Optional['NumberNode'], 'goext.error']:
        pass

    # c:\go\src\text\template\parse\node.go:725:16
    def newString(self, pos: 'Pos', orig: str, text: str) -> Optional['StringNode']:
        pass

    # c:\go\src\text\template\parse\node.go:753:16
    def newEnd(self, pos: 'Pos') -> Optional['endNode']:
        pass

    # c:\go\src\text\template\parse\node.go:781:16
    def newElse(self, pos: 'Pos', line: int) -> Optional['elseNode']:
        pass

    # c:\go\src\text\template\parse\node.go:869:16
    def newIf(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['IfNode']:
        pass

    # c:\go\src\text\template\parse\node.go:882:16
    def newRange(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['RangeNode']:
        pass

    # c:\go\src\text\template\parse\node.go:895:16
    def newWith(self, pos: 'Pos', line: int, pipe: Optional['PipeNode'], list: Optional['ListNode'], elseList: Optional['ListNode']) -> Optional['WithNode']:
        pass

    # c:\go\src\text\template\parse\node.go:913:16
    def newTemplate(self, pos: 'Pos', line: int, name: str, pipe: Optional['PipeNode']) -> Optional['TemplateNode']:
        pass

    # c:\go\src\text\template\parse\parse.go:35:16
    def Copy(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\parse.go:60:16
    def next(self) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:70:16
    def backup(self) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:76:16
    def backup2(self, t1: 'item') -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:83:16
    def backup3(self, t2: 'item', t1: 'item') -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:90:16
    def peek(self) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:100:16
    def nextNonSpace(self) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:111:16
    def peekNonSpace(self) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:130:16
    def ErrorContext(self, n: 'Node') -> Tuple[str, str]:
        pass

    # c:\go\src\text\template\parse\parse.go:150:16
    def errorf(self, format: str, *args: Any) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:157:16
    def error(self, err: 'goext.error') -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:162:16
    def expect(self, expected: 'itemType', context: str) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:171:16
    def expectOneOf(self, expected1: 'itemType', expected2: 'itemType', context: str) -> 'item':
        pass

    # c:\go\src\text\template\parse\parse.go:180:16
    def unexpected(self, token: 'item', context: str) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:185:16
    def recover(self, errp: Optional['goext.error']) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:200:16
    def startParse(self, funcs: List[Dict[str, Any]], lex: Optional['lexer'], treeSet: Dict[str, Optional['Tree']]) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:209:16
    def stopParse(self) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:220:16
    def Parse(self, text: str, leftDelim: str, rightDelim: str, treeSet: Dict[str, Optional['Tree']], *funcs: Dict[str, Any]) -> Tuple[Optional['Tree'], 'goext.error']:
        pass

    # c:\go\src\text\template\parse\parse.go:232:16
    def add(self) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:271:16
    def parse(self) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:298:16
    def parseDefinition(self) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:319:16
    def itemList(self) -> Tuple[Optional['ListNode'], 'Node']:
        pass

    # c:\go\src\text\template\parse\parse.go:335:16
    def textOrAction(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:352:16
    def action(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:377:16
    def pipeline(self, context: str) -> Optional['PipeNode']:
        pass

    # c:\go\src\text\template\parse\parse.go:435:16
    def checkPipeline(self, pipe: Optional['PipeNode'], context: str) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:450:16
    def parseControl(self, allowElseIf: bool, context: str) -> Tuple['Pos', int, Optional['PipeNode'], Optional['ListNode'], Optional['ListNode']]:
        pass

    # c:\go\src\text\template\parse\parse.go:487:16
    def ifControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:495:16
    def rangeControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:503:16
    def withControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:510:16
    def endControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:517:16
    def elseControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:533:16
    def blockControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:559:16
    def templateControl(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:572:16
    def parseTemplateName(self, token: 'item', context: str) -> str:
        pass

    # c:\go\src\text\template\parse\parse.go:590:16
    def command(self) -> Optional['CommandNode']:
        pass

    # c:\go\src\text\template\parse\parse.go:622:16
    def operand(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:660:16
    def term(self) -> 'Node':
        pass

    # c:\go\src\text\template\parse\parse.go:703:16
    def hasFunction(self, name: str) -> bool:
        pass

    # c:\go\src\text\template\parse\parse.go:716:16
    def popVars(self, n: int) -> None:
        pass

    # c:\go\src\text\template\parse\parse.go:722:16
    def useVar(self, pos: 'Pos', name: str) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:354:6
class VariableNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Ident: Optional[List[str]]  # Variable name and fields in lexical order.

    # c:\go\src\text\template\parse\node.go:365:24
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:371:24
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:380:24
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:384:24
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:891:6
class WithNode(BranchNode):

    # c:\go\src\text\template\parse\node.go:899:20
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:774:6
class elseNode(Node, NodeType, Pos):
    tr: Optional['Tree']
    Line: int  # The line number in the input. Deprecated: Kept for compatibility.

    # c:\go\src\text\template\parse\node.go:785:20
    def Type(self) -> 'NodeType':
        pass

    # c:\go\src\text\template\parse\node.go:789:20
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:793:20
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:797:20
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:801:20
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\node.go:747:6
class endNode(Node, NodeType, Pos):
    tr: Optional['Tree']

    # c:\go\src\text\template\parse\node.go:757:19
    def String(self) -> str:
        pass

    # c:\go\src\text\template\parse\node.go:761:19
    def writeTo(self, sb: Optional[goext.strings_Builder]) -> None:
        pass

    # c:\go\src\text\template\parse\node.go:765:19
    def tree(self) -> Optional['Tree']:
        pass

    # c:\go\src\text\template\parse\node.go:769:19
    def Copy(self) -> 'Node':
        pass


# c:\go\src\text\template\parse\lex.go:15:6
class item:
    typ: 'itemType'  # The type of this item.
    pos: 'Pos'  # The starting position, in bytes, of this item in the input string.
    val: str  # The value of this item.
    line: int  # The line number at the start of this item.

    # c:\go\src\text\template\parse\lex.go:22:15
    def String(self) -> str:
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
        pass

    # c:\go\src\text\template\parse\lex.go:140:17
    def peek(self) -> int:
        pass

    # c:\go\src\text\template\parse\lex.go:147:17
    def backup(self) -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:156:17
    def emit(self, t: 'itemType') -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:163:17
    def ignore(self) -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:170:17
    def accept(self, valid: str) -> bool:
        pass

    # c:\go\src\text\template\parse\lex.go:179:17
    def acceptRun(self, valid: str) -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:187:17
    def errorf(self, format: str, *args: Any) -> 'stateFn':
        pass

    # c:\go\src\text\template\parse\lex.go:194:17
    def nextItem(self) -> 'item':
        pass

    # c:\go\src\text\template\parse\lex.go:200:17
    def drain(self) -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:228:17
    def run(self) -> None:
        pass

    # c:\go\src\text\template\parse\lex.go:279:17
    def atRightDelim(self) -> Tuple[bool, bool]:
        pass

    # c:\go\src\text\template\parse\lex.go:521:17
    def atTerminator(self) -> bool:
        pass

    # c:\go\src\text\template\parse\lex.go:580:17
    def scanNumber(self) -> bool:
        pass


#
# FUNCS
#


# c:\go\src\text\template\parse\parse.go:244:6
def IsEmptyTree(n: 'Node') -> bool:
    pass


# c:\go\src\text\template\parse\parse.go:120:6
def New(name: str, *funcs: Dict[str, Any]) -> Optional['Tree']:
    pass


# c:\go\src\text\template\parse\node.go:316:6
def NewIdentifier(ident: str) -> Optional['IdentifierNode']:
    pass


# c:\go\src\text\template\parse\parse.go:51:6
def Parse(name: str, text: str, leftDelim: str, rightDelim: str, *funcs: Dict[str, Any]) -> Tuple[Dict[str, Optional['Tree']], 'goext.error']:
    pass


# c:\go\src\text\template\parse\lex.go:663:6
def isAlphaNumeric(r: int) -> bool:
    pass


# c:\go\src\text\template\parse\lex.go:658:6
def isEndOfLine(r: int) -> bool:
    pass


# c:\go\src\text\template\parse\lex.go:653:6
def isSpace(r: int) -> bool:
    pass


# c:\go\src\text\template\parse\lex.go:290:6
def leftTrimLength(s: str) -> 'Pos':
    pass


# c:\go\src\text\template\parse\lex.go:206:6
def lex(name: str, input: str, left: str, right: str) -> Optional['lexer']:
    pass


# c:\go\src\text\template\parse\lex.go:541:6
def lexChar(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:315:6
def lexComment(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:477:6
def lexField(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:493:6
def lexFieldOrVariable(l: Optional['lexer'], typ: 'itemType') -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:447:6
def lexIdentifier(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:354:6
def lexInsideAction(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:295:6
def lexLeftDelim(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:564:6
def lexNumber(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:618:6
def lexQuote(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:638:6
def lexRawQuote(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:338:6
def lexRightDelim(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:423:6
def lexSpace(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:245:6
def lexText(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:483:6
def lexVariable(l: Optional['lexer']) -> 'stateFn':
    pass


# c:\go\src\text\template\parse\lex.go:274:6
def rightTrimLength(s: str) -> 'Pos':
    pass

