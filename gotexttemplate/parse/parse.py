from enum import Enum
from queue import LifoQueue
from typing import NewType, List, Dict, Any, Tuple, Optional, TypeVar, Sequence, Callable, Generator

from gotexttemplate.parse.exception import ParseError
from gotexttemplate.parse.util import StringsBuilder


Pos = int
"""Pos represents a byte position in the original input text from which this template was parsed."""


#
# lex.go
#

class itemType(Enum):
    itemError = 1 # error occurred; value is text of error
    itemBool = 2  # boolean constant
    itemChar = 3  # printable ASCII character; grab bag for comma etc.
    itemCharConstant = 4  # character constant
    itemComment = 5  # comment text
    itemComplex = 6  # complex constant (1+2i); imaginary is just a number
    itemAssign = 7  # equals ('=') introducing an assignment
    itemDeclare = 8  # colon-equals (':=') introducing a declaration
    itemEOF = 9
    itemField = 10  # alphanumeric identifier starting with '.'
    itemIdentifier = 11  # alphanumeric identifier not starting with '.'
    itemLeftDelim = 12  # left action delimiter
    itemLeftParen = 13  # '(' inside action
    itemNumber = 14  # simple number, including imaginary
    itemPipe = 15  # pipe symbol
    itemRawString = 16  # raw quoted string (includes quotes)
    itemRightDelim = 17  # right action delimiter
    itemRightParen = 18  # ')' inside action
    itemSpace = 19  # run of spaces separating arguments
    itemString = 20  # quoted string (includes quotes)
    itemText = 21  # plain text
    itemVariable = 22  # variable starting with '$', such as '$' or  '$1' or '$hello'
    # Keywords appear after all the rest.
    itemKeyword = 23  # used only to delimit the keywords
    itemBlock = 24  # block keyword
    itemDot = 25  # the cursor, spelled '.'
    itemDefine = 26  # define keyword
    itemElse = 27  # else keyword
    itemEnd = 28  # end keyword
    itemIf = 29  # if keyword
    itemNil = 30  # the untyped nil constant, easiest to treat as a keyword
    itemRange = 31  # range keyword
    itemTemplate = 32  # template keyword
    itemWith = 33  # with keyword


class item:
    typ: itemType  # The type of this item.
    pos: Pos  # The starting position, in bytes, of this item in the input string.
    val: str  # The value of this item.
    line: int  # The line number at the start of this item.

    def __init__(self, typ: itemType, pos: Pos, val: str, line: int):
        self.typ = typ
        self.pos = pos
        self.val = val
        self.line = line

    def String(self) -> str:
        if self.typ == itemType.itemEOF:
            return 'EOF'
        elif self.typ == itemType.itemError:
            return self.val
        elif self.typ == itemType.itemKeyword:
            return '<{}>'.format(self.val)
        elif len(self.val) > 10:
            return '{}...'.format(self.val[:10])
        return '"{}"'.format(self.val.replace('"', r'\"'))


key: Dict[str, itemType] = {
    ".": itemType.itemDot,
    "block": itemType.itemBlock,
    "define": itemType.itemDefine,
    "else": itemType.itemElse,
    "end": itemType.itemEnd,
    "if": itemType.itemIf,
    "range": itemType.itemRange,
    "nil": itemType.itemNil,
    "template": itemType.itemTemplate,
    "with": itemType.itemWith,
}


# eof = -1
eof = None


"""
Trimming spaces.
If the action begins "{{- " rather than "{{", then all space/tab/newlines
preceding the action are trimmed; conversely if it ends " -}}" the
leading spaces are trimmed. This is done entirely in the lexer; the
parser never sees it happen. We require an ASCII space (' ', \t, \r, \n)
to be present to avoid ambiguity with things like "{{-3}}". It reads
better with the space present anyway. For simplicity, only ASCII
does the job.
"""
spaceChars = " \t\r\n"  # These are the space characters defined by Go itself.
trimMarker = '-'  # Attached to left/right delimiter, trims trailing spaces from preceding/following text.
trimMarkerLen = Pos(1 + 1)  # marker plus space before or after


stateFn = Callable[['lexer'], 'stateFn']
"""stateFn represents the state of the scanner as a function that returns the next state."""


class lexer:
    """lexer holds the state of the scanner."""
    name: str  # the name of the input; used only for error reports
    input: str  # the string being scanned
    leftDelim: str  # start of action
    rightDelim: str  # end of action
    emitComment: bool  # emit itemComment tokens.
    pos: Pos  # current position in the input
    start: Pos  # start position of this item
    width: Pos  # width of last rune read from input
    items: LifoQueue  # channel of scanned items
    parenDepth: int  # nesting depth of ( ) exprs
    line: int  # 1+number of newlines seen
    startLine: int  # start line of this item

    def __init__(self, name: str, input: str, leftDelim: str, rightDelim: str,
                 emitComment: bool, line: int, startLine: int):
        self.name = name
        self.input = input
        self.leftDelim = leftDelim
        self.rightDelim = rightDelim
        self.emitComment = emitComment
        self.pos = 0
        self.start = 0
        self.width = 0
        self.items = LifoQueue()
        self.parenDepth = 0
        self.line = line
        self.startLine = startLine

    def next(self) -> Optional[str]:
        if self.pos >= len(self.input):
            self.width = 0
            return eof
        # TODO
        # r, w := utf8.DecodeRuneInString(l.input[l.pos:])
        r = self.input[self.pos:1]
        w = len(r)
        self.width = w
        self.pos += self.width
        if r == '\n':
            self.line += 1
        return r

    def peek(self) -> Optional[str]:
        r = self.next()
        self.backup()
        return r

    def backup(self):
        self.pos -= self.width
        # Correct newline count.
        if self.width == 1 and self.input[self.pos:1] == '\n':
            self.line -= 1

    def emit(self, t: itemType):
        self.items.put(item(t, self.start, self.input[self.start:self.pos-self.start], self.startLine))
        self.start = self.pos
        self.startLine = self.line

    def ignore(self):
        """ignore skips over the pending input before this point."""
        self.line += self.input[self.start:self.pos-self.start].count('\n')
        self.start = self.pos
        self.startLine = self.line

    def accept(self, valid: str) -> bool:
        """accept consumes the next rune if it's from the valid set."""
        if self.next() in [c for c in valid]:
            return True
        self.backup()
        return False

    def acceptRun(self, valid: str):
        """acceptRun consumes a run of runes from the valid set."""
        while True:
            if self.next() not in [c for c in valid]:
                break
        self.backup()

    def errorf(self, format: str, *args: Any) -> Optional[stateFn]:
        """
        errorf returns an error token and terminates the scan by passing
        back a nil pointer that will be the next state, terminating l.nextItem.
        """
        self.items.put(item(itemType.itemError, self.start, format.format(*args), self.startLine))
        return None

    def nextItem(self) -> item:
        """
        nextItem returns the next item from the input.
        Called by the parser, not in the lexing goroutine.
        """
        return self.items.get()

    def drain(self) -> None:
        """
        drain drains the output so the lexing goroutine will exit.
        Called by the parser, not in the lexing goroutine.
        """
        while not self.items.empty():
            self.items.get()

    def run(self):
        state = lexText
        while state is not None:
            state = state(self)
        # close(self.items)

    def atRightDelim(self) -> Tuple[bool, bool]:
        """atRightDelim reports whether the lexer is at a right delimiter, possibly preceded by a trim marker."""
        if hasRightTrimMarker(self.input[self.pos:]) and self.input[self.pos+trimMarkerLen:].startswith(self.rightDelim):  #  With trim marker.
            return True, True
        if self.input[self.pos:].startswith(self.rightDelim):
            return True, False
        return False, False

    def atTerminator(self) -> bool:
        """
        atTerminator reports whether the input is at valid termination character to
        appear after an identifier. Breaks .X.Y into two pieces. Also catches cases
        like "$x+2" not being acceptable without a space, in case we decide one
        day to implement arithmetic.
        """
        r = self.peek()
        if isSpace(r):
            return True
        if r in [eof, '.', ',', '|', ':', ')', '(']:
            return True
        # Does r start the delimiter? This can be ambiguous (with delim=="#", $x/2 will
        # succeed but should fail) but only in extremely rare cases caused by willfully
        # bad choice of delimiter.
        if self.rightDelim == r:
            return True
        return False

    def scanNumber(self) -> bool:
        # Optional leading sign.
        self.accept('+-')
        # Is it hex?
        digits = "0123456789_"
        if self.accept('0'):
            # Note: Leading 0 does not mean octal in floats.
            if self.accept('xX'):
                digits = "0123456789abcdefABCDEF_"
            elif self.accept('bB'):
                digits = "01_"
        self.acceptRun(digits)
        if self.accept('.'):
            self.acceptRun(digits)
        if len(digits) == 10+1 and self.accept('eE'):
            self.accept('+-')
            self.acceptRun("0123456789_")
        if len(digits) == 16 + 6 + 1 and self.accept("pP"):
            self.accept('+-')
            self.acceptRun('0123456789_')
        # Is it imaginary?
        self.accept('i')
        # Next thing mustn't be alphanumeric.
        if isAlphaNumeric(self.peek()):
            self.next()
            return False
        return True


leftDelim = "{{"
rightDelim = "}}"
leftComment = "/*"
rightComment = "*/"


def lex(name: str, input: str, left: str, right: str, emitComment: bool) -> lexer:
    if left == '':
        left = leftDelim
    if right == '':
        right = rightDelim
    l = lexer(name=name, input=input, leftDelim=left, rightDelim=right,
              emitComment=emitComment, line=1, startLine=1)
    # TODO
    l.run()  # go
    return l


def isSpace(r: str) -> bool:
    return r == ' ' or r == '\t' or r == '\r' or r == '\n'


def hasLeftTrimMarker(s: str) -> bool:
    return len(s) > 2 and s[0] == trimMarker and isSpace(s[1])


def hasRightTrimMarker(s: str) -> bool:
    return len(s) >= 2 and isSpace(s[0]) and s[1] == trimMarker


def rightTrimLength(s: str) -> Pos:
    return len(s) - len(s.rstrip(spaceChars))


def leftTrimLength(s: str) -> Pos:
    return len(s) - len(s.lstrip(spaceChars))


def isAlphaNumeric(r: str) -> bool:
    return r.isalnum()


def lexText(l: lexer) -> Optional[stateFn]:
    """lexText scans until an opening action delimiter, "{{"."""
    l.width = 0
    x = l.input[l.pos:].find(l.leftDelim)
    if x >= 0:
        ldn: Pos = len(l.leftDelim)
        l.pos += x
        trimLength = 0
        if hasLeftTrimMarker(l.input[l.start:l.pos]):
            trimLength = rightTrimLength(l.input[l.start:l.pos])
        l.pos -= trimLength
        if l.pos > l.start:
            l.line += l.input[l.start:l.pos].count('\n')
            l.emit(itemType.itemText)
        l.pos += trimLength
        l.ignore()
        return lexLeftDelim
    l.pos = len(l.input)
    # Correctly reached EOF.
    if l.pos > l.start:
        l.line += l.input[l.start:l.pos].count('\n')
        l.emit(itemType.itemText)
    l.emit(itemType.itemEOF)
    return None


def lexLeftDelim(l: lexer) -> Optional[stateFn]:
    """lexLeftDelim scans the left delimiter, which is known to be present, possibly with a trim marker."""
    l.pos += len(l.leftDelim)
    trimSpace = hasLeftTrimMarker(l.input[l.pos:])
    afterMarker = 0
    if trimSpace:
        afterMarker = trimMarkerLen
    if l.input[l.pos+afterMarker:].startswith(leftComment):
        l.pos += afterMarker
        l.ignore()
        return lexComment

    l.emit(itemType.itemLeftDelim)
    l.pos += afterMarker
    l.ignore()
    l.parenDepth = 0
    return lexInsideAction


def lexComment(l: lexer) -> Optional[stateFn]:
    l.pos += len(leftComment)
    i = l.input[l.pos:].find(rightComment)
    if i < 0:
        raise ParseError('Unclosed comment')
    l.pos += i + len(rightComment)
    delim, trimSpace = l.atRightDelim()
    if not delim:
        raise ParseError('comment ends before closing delimiter')
    if l.emitComment:
        l.emit(itemType.itemComment)
    if trimSpace:
        l.pos += trimMarkerLen
    l.pos += len(l.rightDelim)
    if trimSpace:
        l.pos += leftTrimLength(l.input[l.pos:])
    l.ignore()
    return lexText


def lexRightDelim(l: lexer) -> Optional[stateFn]:
    """lexRightDelim scans the right delimiter, which is known to be present, possibly with a trim marker."""
    trimSpace = hasRightTrimMarker(l.input[l.pos:])
    if trimSpace:
        l.pos += trimMarkerLen
        l.ignore()
    l.pos += len(l.rightDelim)
    if trimSpace:
        l.pos += leftTrimLength(l.input[l.pos:])
        l.ignore()
    return lexText


MaxASCII = '\u007F'


def lexInsideAction(l: lexer) -> Optional[stateFn]:
    """lexInsideAction scans the elements inside action delimiters."""
    # Either number, quoted string, or identifier.
    # Spaces separate arguments; runs of spaces turn into itemSpace.
    # Pipe symbols separate and are emitted.
    delim, _ = l.atRightDelim()
    if delim:
        if l.parenDepth == 0:
            return lexRightDelim
        raise ParseError('unclosed left paren')

    r = l.next()
    if r == eof:
        raise ParseError('unclosed action')
    elif isSpace(r):
        l.backup()  # Put space back in case we have " -}}".
        return lexSpace
    elif r == '=':
        l.emit(itemType.itemAssign)
    elif r == ':':
        if l.next() != '=':
            raise ParseError('expected :=')
        l.emit(itemType.itemDeclare)
    elif r == '|':
        l.emit(itemType.itemPipe)
    elif r == '"':
        return lexQuote
    elif r == '`':
        return lexRawQuote
    elif r == '$':
        return lexVariable
    elif r == "'":
        return lexChar
    elif r == '.':
        # special look-ahead for ".field" so we don't break l.backup().
        if l.pos < len(l.input):
            r = l.input[l.pos]
            if r < '0' or '9' < r:
                return lexField
        # '.' can start a number.
        if r == '+' or r == '-' or ('0' <= r and r <= '9'):
            l.backup()
            return lexNumber
    elif r == '+' or r == '-' or ('0' <= r and r <= '9'):
        l.backup()
        return lexNumber
    elif isAlphaNumeric(r):
        l.backup()
        return lexIdentifier
    elif r == '(':
        l.emit(itemType.itemLeftParen)
        l.parenDepth += 1
    elif r == ')':
        l.emit(itemType.itemRightParen)
        l.parenDepth -= 1
        if l.parenDepth < 0:
            raise ParseError('unexpected right paren {}'.format(r))
    elif r <= MaxASCII and r.isprintable():
        l.emit(itemType.itemChar)
    else:
        raise ParseError('unrecognized character in action: {}'.format(r))
    return lexInsideAction


def lexSpace(l: lexer) -> Optional[stateFn]:
    """
    lexSpace scans a run of space characters.
    We have not consumed the first space, which is known to be present.
    Take care if there is a trim-marked right delimiter, which starts with a space.
    """
    numSpaces = 0
    while True:
        r = l.peek()
        if not isSpace(r):
            break
        l.next()
        numSpaces += 1
    # Be careful about a trim-marked closing delimiter, which has a minus
    # after a space. We know there is a space, so check for the '-' that might follow.
    if hasRightTrimMarker(l.input[l.pos-1:]) and l.input[l.pos-1+trimMarkerLen:].startswith(l.rightDelim):
        l.backup()
        if numSpaces == 1:
            return lexRightDelim
    l.emit(itemType.itemSpace)
    return lexInsideAction


def lexIdentifier(l: lexer) -> Optional[stateFn]:
    """lexIdentifier scans an alphanumeric."""
    while True:
        r = l.next()
        if isAlphaNumeric(r):
            pass  # absorb.
        else:
            l.backup()
            word = l.input[l.start:l.pos]
            if not l.atTerminator():
                raise ParseError('bad character {}'.format(r))
            if key[word] > itemType.itemKeyword:
                l.emit(key[word])
            elif word[0] == '.':
                l.emit(itemType.itemField)
            elif word == 'true' or word == 'false':
                l.emit(itemType.itemBool)
            else:
                l.emit(itemType.itemIdentifier)
            break
    return lexInsideAction


def lexField(l: lexer) -> Optional[stateFn]:
    """
    lexField scans a field: .Alphanumeric.
    The . has been scanned.
    """
    return lexFieldOrVariable(l, itemType.itemField)


def lexVariable(l: lexer) -> Optional[stateFn]:
    """
    lexVariable scans a Variable: $Alphanumeric.
    The $ has been scanned.
    """
    if l.atTerminator():  # Nothing interesting follows -> "$".
        l.emit(itemType.itemVariable)
        return lexInsideAction
    return lexFieldOrVariable(l, itemType.itemVariable)


def lexFieldOrVariable(l: lexer, typ: itemType) -> Optional[stateFn]:
    """
    lexVariable scans a field or variable: [.$]Alphanumeric.
    The . or $ has been scanned.
    """
    if l.atTerminator():  # Nothing interesting follows -> "." or "$".
        if typ == itemType.itemVariable:
            l.emit(itemType.itemVariable)
        else:
            l.emit(itemType.itemDot)
        return lexInsideAction
    while True:
        r = l.next()
        if not isAlphaNumeric(r):
            l.backup()
            break
    if not l.atTerminator():
        raise ParseError('bad character {}'.format(r))
    l.emit(typ)
    return lexInsideAction


def lexChar(l: lexer) -> Optional[stateFn]:
    """
    lexChar scans a character constant. The initial quote is already
    scanned. Syntax checking is done by the parser.
    """
    while True:
        x = l.next()
        if x == '\\':
            r = l.next()
            if r != eof and r != '\n':
                break
            if x == eof or x == '\n':
                raise ParseError('unterminated character constant')
        elif x == eof or x == '\n':
            raise ParseError('unterminated character constant')
        elif x == "'":
            break
    l.emit(itemType.itemCharConstant)
    return lexInsideAction


def lexNumber(l: lexer) -> Optional[stateFn]:
    """
    lexNumber scans a number: decimal, octal, hex, float, or imaginary. This
    isn't a perfect number scanner - for instance it accepts "." and "0x0.2"
    and "089" - but when it's wrong the input is invalid and the parser (via
    strconv) will notice.
    """
    if not l.scanNumber():
        raise ParseError('bad number syntax: {}'.format(l.input[l.start:l.pos]))
    sign = l.peek()
    if sign == '+' or sign == '-':
        # Complex: 1+2i. No spaces, must end in 'i'.
        if not l.scanNumber() or l.input[l.pos-1] != 'i':
            raise ParseError('bad number syntax: {}'.format(l.input[l.start:l.pos]))
        l.emit(itemType.itemComplex)
    else:
        l.emit(itemType.itemNumber)
    return lexInsideAction


def lexQuote(l: lexer) -> Optional[stateFn]:
    """lexQuote scans a quoted string."""
    while True:
        x = l.next()
        if x == '\\':
            r = l.next()
            if r != eof and r != '\n':
                break
            if x == 'eof' or x == '\n':
                raise ParseError('unterminated quoted string')
        elif x == 'eof' or x == '\n':
            raise ParseError('unterminated quoted string')
        elif x == '"':
            break
    l.emit(itemType.itemString)
    return lexInsideAction


def lexRawQuote(l: lexer) -> Optional[stateFn]:
    """lexRawQuote scans a raw quoted string."""
    while True:
        x = l.next()
        if x == eof:
            raise ParseError('unterminated raw quoted string')
        elif x == '`':
            break
    l.emit(itemType.itemRawString)
    return lexInsideAction


#
# node.go
#
NodeT = TypeVar('NodeT', bound='Node')


class Node:
    """
    A Node is an element in the parse tree. The interface is trivial.
    The interface contains an unexported method so that only
    types local to this package can satisfy it.
    """
    def Type(self) -> 'NodeType': ...
    def String(self) -> str: ...
    def Copy(self) -> 'NodeT': ...
    """
    Copy does a deep copy of the Node and all its components.
    To avoid type assertions, some XxxNodes also have specialized
    CopyXxx methods that return *XxxNode.
    """
    def Position(self) -> Pos: ...
    def tree(self) -> 'Tree': ...
    def writeTo(sb: StringsBuilder) -> None: ...


class NodeType(Enum):
    """
    NodeType identifies the type of a parse tree node.
    """
    NodeText = 1  # Plain text.
    NodeAction = 2  # A non-control action such as a field evaluation.
    NodeBool = 3  # A boolean constant.
    NodeChain = 4  # A sequence of field accesses.
    NodeCommand = 5  # An element of a pipeline.
    NodeDot = 6  # The cursor, dot.
    nodeElse = 7  # An else action. Not added to tree.
    nodeEnd = 8  # An end action. Not added to tree.
    NodeField = 9  # A field or method name.
    NodeIdentifier = 10  # An identifier; always a function name.
    NodeIf = 11  # An if action.
    NodeList = 12  # A list of Nodes.
    NodeNil = 13  # An untyped nil constant.
    NodeNumber = 14  # A numerical constant.
    NodePipe = 15  # A pipeline of commands.
    NodeRange = 16  # A range action.
    NodeString = 17  # A string constant.
    NodeTemplate = 18  # A template invocation action.
    NodeVariable = 19  # A $ variable.
    NodeWith = 20  # A with action.
    NodeComment = 21  # A comment.


# Nodes

class ListNode(Node):
    NodeType: NodeType
    Pos: Pos
    tr: 'Tree'
    Nodes: List[Node]


class Mode(Enum):
    """
    A mode value is a set of flags (or 0). Modes control parser behavior.
    """
    ModeNone = 0
    ParseComments = 1  # parse comments and add them to AST


class Tree:
    """
    Tree is the representation of a single parsed template.
    """
    Name: str
    ParseName: str
    Root: Optional[ListNode]
    Mode: Mode
    text: str
    funcs: List[Dict[str, Any]]
    lex: Optional[lexer]
    token: List[item]
    peekCount: int
    vars: List[str]
    treeSet: Dict[str, 'Tree']
    actionLine: int
    mode: Mode

    def __init__(self, Name: str, ParseName: Optional[str] = None, Root: Optional[ListNode] = None,
                 text: Optional[str] = None, funcs: Optional[List[Dict[str, Any]]] = None):
        self.Name = Name  # name of the template represented by the tree.
        self.ParseName = ParseName if ParseName is not None else ''  # name of the top-level template during parsing, for error messages.
        self.Root = Root  # top-level root of the tree.
        self.Mode = Mode.ModeNone  # parsing mode.
        self.text = text if text is not None else ''  # text parsed to create the template (or its parent)
        # Parsing only; cleared after parse.
        self.funcs = funcs if funcs is not None else []
        self.lex = None
        self.token = []  # three-token lookahead for parser.
        self.peekCount = 0
        self.vars = []  # variables defined at the moment.
        self.treeSet = {}
        self.actionLine = 0   # line of left delim starting action
        self.mode = Mode.ModeNone

    def Copy(self) -> 'Tree':
        """
        Copy returns a copy of the Tree. Any parsing state is discarded.
        """
        return Tree(self.Name, self.ParseName, self.Root.Copy(), self.text)

    def next(self) -> item:
        if self.peekCount > 0:
            self.peekCount -= 1
        else:
            self.token[0] = self.lex.nextItem()
        return self.token[self.peekCount]


def Parse(name: str, text: str, leftDelim: str, rightDelim: str, funcs: List[Dict[str, Any]]) -> Dict[str, Tree]:
    """
    Parse returns a map from template name to parse.Tree, created by parsing the
    templates described in the argument string. The top-level template will be
    given the specified name. If an error is encountered, parsing stops and an
    empty map is returned with the error.
    """
    treeSet: Dict[str, Tree] = {}
    t = Tree(Name=name, funcs=funcs)
    t.text = text
    t.Parse(text, leftDelim, rightDelim, treeSet, funcs)
    return treeSet
