# type: ignore
# package: text/template

from enum import Enum
from typing import Callable, Optional, List, Dict, Any, Tuple
import queue
from . import goext
from . import text_template_parse

#
# ENUMS
#

# c:\go\src\text\template\funcs.go:424:6
class kind(Enum):
    invalidKind = 0
    boolKind = 1
    complexKind = 2
    intKind = 3
    floatKind = 4
    stringKind = 5
    uintKind = 6

# c:\go\src\text\template\option.go:12:6
class missingKeyAction(Enum):
    mapInvalid = 0  # Return an invalid reflect.Value.
    mapZeroValue = 1  # Return the zero value for the map element.
    mapError = 2  # Error out

#
# CONSTS
#

#
# TYPES
#

# c:\go\src\text\template\funcs.go:31:6
FuncMap = Dict[str, Any]

#
# INTERFACES
#

#
# STRUCTS
#

# c:\go\src\text\template\exec.go:114:6
class ExecError:
    Name: str  # Name of template.
    Err: 'goext.error'  # Pre-formatted error.

    # c:\go\src\text\template\exec.go:119:20
    def Error(self) -> str:
        pass
    # c:\go\src\text\template\exec.go:123:20
    def Unwrap(self) -> 'goext.error':
        pass

# c:\go\src\text\template\template.go:28:6
class Template(text_template_parse.Tree, common):
    name: str
    leftDelim: str
    rightDelim: str

    # c:\go\src\text\template\exec.go:181:20
    def ExecuteTemplate(self, wr: goext.io_Writer, name: str, data: Any) -> 'goext.error':
        pass
    # c:\go\src\text\template\exec.go:202:20
    def Execute(self, wr: goext.io_Writer, data: Any) -> 'goext.error':
        pass
    # c:\go\src\text\template\exec.go:206:20
    def execute(self, wr: goext.io_Writer, data: Any) -> 'goext.error':
        pass
    # c:\go\src\text\template\exec.go:228:20
    def DefinedTemplates(self) -> str:
        pass
    # c:\go\src\text\template\helper.go:52:20
    def ParseFiles(self, *filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
        pass
    # c:\go\src\text\template\helper.go:115:20
    def ParseGlob(self, pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
        pass
    # c:\go\src\text\template\option.go:42:20
    def Option(self, *opt: str) -> Optional['Template']:
        pass
    # c:\go\src\text\template\option.go:50:20
    def setOption(self, opt: str) -> None:
        pass
    # c:\go\src\text\template\template.go:46:20
    def Name(self) -> str:
        pass
    # c:\go\src\text\template\template.go:57:20
    def New(self, name: str) -> Optional['Template']:
        pass
    # c:\go\src\text\template\template.go:69:20
    def init(self) -> None:
        pass
    # c:\go\src\text\template\template.go:85:20
    def Clone(self) -> Tuple[Optional['Template'], 'goext.error']:
        pass
    # c:\go\src\text\template\template.go:112:20
    def copy(self, c: Optional['common']) -> Optional['Template']:
        pass
    # c:\go\src\text\template\template.go:126:20
    def AddParseTree(self, name: str, tree: Optional[text_template_parse.Tree]) -> Tuple[Optional['Template'], 'goext.error']:
        pass
    # c:\go\src\text\template\template.go:140:20
    def Templates(self) -> List[Optional['Template']]:
        pass
    # c:\go\src\text\template\template.go:157:20
    def Delims(self, left: str, right: str) -> Optional['Template']:
        pass
    # c:\go\src\text\template\template.go:170:20
    def Funcs(self, funcMap: 'FuncMap') -> Optional['Template']:
        pass
    # c:\go\src\text\template\template.go:181:20
    def Lookup(self, name: str) -> Optional['Template']:
        pass
    # c:\go\src\text\template\template.go:198:20
    def Parse(self, text: str) -> Tuple[Optional['Template'], 'goext.error']:
        pass
    # c:\go\src\text\template\template.go:218:20
    def associate(self, new: Optional['Template'], tree: Optional[text_template_parse.Tree]) -> bool:
        pass

# c:\go\src\text\template\template.go:14:6
class common:
    tmpl: Optional[Dict[str, Optional['Template']]]  # Map from name to defined templates.
    option: 'option'
    muFuncs: goext.sync_RWMutex  # protects parseFuncs and execFuncs
    parseFuncs: 'FuncMap'
    execFuncs: Optional[Dict[str, goext.reflect_Value]]

# c:\go\src\text\template\exec.go:92:6
class missingValType:
    pass

# c:\go\src\text\template\option.go:20:6
class option:
    missingKey: 'missingKeyAction'

# c:\go\src\text\template\exec.go:33:6
class state:
    tmpl: Optional['Template']
    wr: goext.io_Writer
    node: text_template_parse.Node  # current node, for errors
    vars: Optional[List['variable']]  # push-down stack of variable values.
    depth: int  # the height of the stack of executing templates.

    # c:\go\src\text\template\exec.go:48:17
    def push(self, name: str, value: goext.reflect_Value) -> None:
        pass
    # c:\go\src\text\template\exec.go:53:17
    def mark(self) -> int:
        pass
    # c:\go\src\text\template\exec.go:58:17
    def pop(self, mark: int) -> None:
        pass
    # c:\go\src\text\template\exec.go:64:17
    def setVar(self, name: str, value: goext.reflect_Value) -> None:
        pass
    # c:\go\src\text\template\exec.go:75:17
    def setTopVar(self, n: int, value: goext.reflect_Value) -> None:
        pass
    # c:\go\src\text\template\exec.go:80:17
    def varValue(self, name: str) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:97:17
    def at(self, node: text_template_parse.Node) -> None:
        pass
    # c:\go\src\text\template\exec.go:128:17
    def errorf(self, format: str, *args: Any) -> None:
        pass
    # c:\go\src\text\template\exec.go:150:17
    def writeError(self, err: 'goext.error') -> None:
        pass
    # c:\go\src\text\template\exec.go:249:17
    def walk(self, dot: goext.reflect_Value, node: text_template_parse.Node) -> None:
        pass
    # c:\go\src\text\template\exec.go:282:17
    def walkIfOrWith(self, typ: text_template_parse.NodeType, dot: goext.reflect_Value, pipe: Optional[text_template_parse.PipeNode], list: Optional[text_template_parse.ListNode], elseList: Optional[text_template_parse.ListNode]) -> None:
        pass
    # c:\go\src\text\template\exec.go:335:17
    def walkRange(self, dot: goext.reflect_Value, r: Optional[text_template_parse.RangeNode]) -> None:
        pass
    # c:\go\src\text\template\exec.go:397:17
    def walkTemplate(self, dot: goext.reflect_Value, t: Optional[text_template_parse.TemplateNode]) -> None:
        pass
    # c:\go\src\text\template\exec.go:424:17
    def evalPipeline(self, dot: goext.reflect_Value, pipe: Optional[text_template_parse.PipeNode]) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:447:17
    def notAFunction(self, args: List[text_template_parse.Node], final: goext.reflect_Value) -> None:
        pass
    # c:\go\src\text\template\exec.go:453:17
    def evalCommand(self, dot: goext.reflect_Value, cmd: Optional[text_template_parse.CommandNode], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:492:17
    def idealConstant(self, constant: Optional[text_template_parse.NumberNode]) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:527:17
    def evalFieldNode(self, dot: goext.reflect_Value, field: Optional[text_template_parse.FieldNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:532:17
    def evalChainNode(self, dot: goext.reflect_Value, chain: Optional[text_template_parse.ChainNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:545:17
    def evalVariableNode(self, dot: goext.reflect_Value, variable: Optional[text_template_parse.VariableNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:559:17
    def evalFieldChain(self, dot: goext.reflect_Value, receiver: goext.reflect_Value, node: text_template_parse.Node, ident: List[str], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:568:17
    def evalFunction(self, dot: goext.reflect_Value, node: Optional[text_template_parse.IdentifierNode], cmd: text_template_parse.Node, args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:581:17
    def evalField(self, dot: goext.reflect_Value, fieldName: str, node: text_template_parse.Node, args: List[text_template_parse.Node], final: goext.reflect_Value, receiver: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:668:17
    def evalCall(self, dot: goext.reflect_Value, fun: goext.reflect_Value, node: text_template_parse.Node, name: str, args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:745:17
    def validateType(self, value: goext.reflect_Value, typ: goext.reflect_Type) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:787:17
    def evalArg(self, dot: goext.reflect_Value, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:834:17
    def evalBool(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:845:17
    def evalString(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:856:17
    def evalInteger(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:867:17
    def evalUnsignedInteger(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:878:17
    def evalFloat(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:889:17
    def evalComplex(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:899:17
    def evalEmptyInterface(self, dot: goext.reflect_Value, n: text_template_parse.Node) -> goext.reflect_Value:
        pass
    # c:\go\src\text\template\exec.go:954:17
    def printValue(self, n: text_template_parse.Node, v: goext.reflect_Value) -> None:
        pass

# c:\go\src\text\template\exec.go:42:6
class variable:
    name: str
    value: goext.reflect_Value

# c:\go\src\text\template\exec.go:146:6
class writeError:
    Err: 'goext.error'  # Original error.

#
# FUNCS
#

# c:\go\src\text\template\funcs.go:603:6
def HTMLEscape(w: goext.io_Writer, b: List[int]) -> None:
    pass

# c:\go\src\text\template\funcs.go:631:6
def HTMLEscapeString(s: str) -> str:
    pass

# c:\go\src\text\template\funcs.go:643:6
def HTMLEscaper(*args: Any) -> str:
    pass

# c:\go\src\text\template\exec.go:303:6
def IsTrue(val: Any) -> Tuple[bool, bool]:
    pass

# c:\go\src\text\template\funcs.go:663:6
def JSEscape(w: goext.io_Writer, b: List[int]) -> None:
    pass

# c:\go\src\text\template\funcs.go:714:6
def JSEscapeString(s: str) -> str:
    pass

# c:\go\src\text\template\funcs.go:734:6
def JSEscaper(*args: Any) -> str:
    pass

# c:\go\src\text\template\helper.go:21:6
def Must(t: Optional['Template'], err: 'goext.error') -> Optional['Template']:
    pass

# c:\go\src\text\template\template.go:37:6
def New(name: str) -> Optional['Template']:
    pass

# c:\go\src\text\template\helper.go:37:6
def ParseFiles(*filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
    pass

# c:\go\src\text\template\helper.go:103:6
def ParseGlob(pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:740:6
def URLQueryEscaper(*args: Any) -> str:
    pass

# c:\go\src\text\template\funcs.go:103:6
def addFuncs(out: 'FuncMap', in_: 'FuncMap') -> None:
    pass

# c:\go\src\text\template\funcs.go:85:6
def addValueFuncs(out: Dict[str, goext.reflect_Value], in_: 'FuncMap') -> None:
    pass

# c:\go\src\text\template\funcs.go:381:6
def and_(arg0: goext.reflect_Value, *args: goext.reflect_Value) -> goext.reflect_Value:
    pass

# c:\go\src\text\template\funcs.go:436:6
def basicKind(v: goext.reflect_Value) -> Tuple['kind', 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:70:6
def builtinFuncs() -> Dict[str, goext.reflect_Value]:
    pass

# c:\go\src\text\template\funcs.go:37:6
def builtins() -> 'FuncMap':
    pass

# c:\go\src\text\template\funcs.go:312:6
def call(fn: goext.reflect_Value, *args: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    pass

# c:\go\src\text\template\exec.go:734:6
def canBeNil(typ: goext.reflect_Type) -> bool:
    pass

# c:\go\src\text\template\funcs.go:78:6
def createValueFuncs(funcMap: 'FuncMap') -> Dict[str, goext.reflect_Value]:
    pass

# c:\go\src\text\template\exec.go:103:6
def doublePercent(str: str) -> str:
    pass

# c:\go\src\text\template\funcs.go:455:6
def eq(arg1: goext.reflect_Value, *arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\exec.go:158:6
def errRecover(errp: Optional['goext.error']) -> None:
    pass

# c:\go\src\text\template\funcs.go:749:6
def evalArgs(args: List[Any]) -> str:
    pass

# c:\go\src\text\template\funcs.go:139:6
def findFunction(name: str, tmpl: Optional['Template']) -> Tuple[goext.reflect_Value, bool]:
    pass

# c:\go\src\text\template\funcs.go:582:6
def ge(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:110:6
def goodFunc(typ: goext.reflect_Type) -> bool:
    pass

# c:\go\src\text\template\funcs.go:122:6
def goodName(name: str) -> bool:
    pass

# c:\go\src\text\template\funcs.go:572:6
def gt(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:206:6
def index(item: goext.reflect_Value, *indexes: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:183:6
def indexArg(index: goext.reflect_Value, cap: int) -> Tuple[int, 'goext.error']:
    pass

# c:\go\src\text\template\exec.go:929:6
def indirect(v: goext.reflect_Value) -> Tuple[goext.reflect_Value, bool]:
    pass

# c:\go\src\text\template\exec.go:942:6
def indirectInterface(v: goext.reflect_Value) -> goext.reflect_Value:
    pass

# c:\go\src\text\template\exec.go:23:6
def initMaxExecDepth() -> int:
    pass

# c:\go\src\text\template\funcs.go:172:6
def intLike(typ: goext.reflect_Kind) -> bool:
    pass

# c:\go\src\text\template\exec.go:523:6
def isHexInt(s: str) -> bool:
    pass

# c:\go\src\text\template\exec.go:519:6
def isRuneInt(s: str) -> bool:
    pass

# c:\go\src\text\template\exec.go:307:6
def isTrue(val: goext.reflect_Value) -> Tuple[bool, bool]:
    pass

# c:\go\src\text\template\funcs.go:724:6
def jsIsSpecial(r: int) -> bool:
    pass

# c:\go\src\text\template\funcs.go:562:6
def le(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:296:6
def length(item: goext.reflect_Value) -> Tuple[int, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:520:6
def lt(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:513:6
def ne(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:410:6
def not_(arg: goext.reflect_Value) -> bool:
    pass

# c:\go\src\text\template\funcs.go:396:6
def or_(arg0: goext.reflect_Value, *args: goext.reflect_Value) -> goext.reflect_Value:
    pass

# c:\go\src\text\template\helper.go:59:6
def parseFiles(t: Optional['Template'], *filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
    pass

# c:\go\src\text\template\helper.go:121:6
def parseGlob(t: Optional['Template'], pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:155:6
def prepareArg(value: goext.reflect_Value, argType: goext.reflect_Type) -> Tuple[goext.reflect_Value, 'goext.error']:
    pass

# c:\go\src\text\template\exec.go:968:6
def printableValue(v: goext.reflect_Value) -> Tuple[Any, bool]:
    pass

# c:\go\src\text\template\funcs.go:355:6
def safeCall(fun: goext.reflect_Value, args: List[goext.reflect_Value]) -> Tuple[goext.reflect_Value, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:250:6
def slice(item: goext.reflect_Value, *indexes: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    pass

# c:\go\src\text\template\funcs.go:374:6
def truth(arg: goext.reflect_Value) -> bool:
    pass

