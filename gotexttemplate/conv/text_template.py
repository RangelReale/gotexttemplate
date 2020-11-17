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


# c:\go\src\text\template\option.go:12:6
class missingKeyAction:
    mapInvalid = 0  # Return an invalid reflect.Value.
    mapZeroValue = 1  # Return the zero value for the map element.
    mapError = 2  # Error out


# c:\go\src\text\template\funcs.go:424:6
class kind:
    invalidKind = 0
    boolKind = 1
    complexKind = 2
    intKind = 3
    floatKind = 4
    stringKind = 5
    uintKind = 6


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


# c:\go\src\text\template\template.go:14:6
class common:
    tmpl: Optional[Dict[str, Optional['Template']]]  # Map from name to defined templates.
    option: 'option'
    muFuncs: goext.sync_RWMutex  # protects parseFuncs and execFuncs
    parseFuncs: 'FuncMap'
    execFuncs: Optional[Dict[str, goext.reflect_Value]]


# c:\go\src\text\template\exec.go:114:6
class ExecError:
    Name: str  # Name of template.
    Err: 'goext.error'  # Pre-formatted error.

    # c:\go\src\text\template\exec.go:119:20
    def Error(self) -> str:
        #         {
        #         	return e.Err.Error()
        #         }
        pass

    # c:\go\src\text\template\exec.go:123:20
    def Unwrap(self) -> 'goext.error':
        #         {
        #         	return e.Err
        #         }
        pass


# c:\go\src\text\template\template.go:28:6
class Template(text_template_parse.Tree, common):
    name: str
    leftDelim: str
    rightDelim: str

    # c:\go\src\text\template\exec.go:181:20
    def ExecuteTemplate(self, wr: goext.io_Writer, name: str, data: Any) -> 'goext.error':
        #         {
        #         	var tmpl *Template
        #         	if t.common != nil {
        #         		tmpl = t.tmpl[name]
        #         	}
        #         	if tmpl == nil {
        #         		return fmt.Errorf("template: no template %!q(MISSING) associated with template %!q(MISSING)", name, t.name)
        #         	}
        #         	return tmpl.Execute(wr, data)
        #         }
        pass

    # c:\go\src\text\template\exec.go:202:20
    def Execute(self, wr: goext.io_Writer, data: Any) -> 'goext.error':
        #         {
        #         	return t.execute(wr, data)
        #         }
        pass

    # c:\go\src\text\template\exec.go:206:20
    def execute(self, wr: goext.io_Writer, data: Any) -> 'goext.error':
        #         {
        #         	defer errRecover(&err)
        #         	value, ok := data.(reflect.Value)
        #         	if !ok {
        #         		value = reflect.ValueOf(data)
        #         	}
        #         	state := &state{
        #         		tmpl:	t,
        #         		wr:	wr,
        #         		vars:	[]variable{{"$", value}},
        #         	}
        #         	if t.Tree == nil || t.Root == nil {
        #         		state.errorf("%!q(MISSING) is an incomplete or empty template", t.Name())
        #         	}
        #         	state.walk(value, t.Root)
        #         	return
        #         }
        pass

    # c:\go\src\text\template\exec.go:228:20
    def DefinedTemplates(self) -> str:
        #         {
        #         	if t.common == nil {
        #         		return ""
        #         	}
        #         	var b strings.Builder
        #         	for name, tmpl := range t.tmpl {
        #         		if tmpl.Tree == nil || tmpl.Root == nil {
        #         			continue
        #         		}
        #         		if b.Len() == 0 {
        #         			b.WriteString("; defined templates are: ")
        #         		} else {
        #         			b.WriteString(", ")
        #         		}
        #         		fmt.Fprintf(&b, "%!q(MISSING)", name)
        #         	}
        #         	return b.String()
        #         }
        pass

    # c:\go\src\text\template\helper.go:52:20
    def ParseFiles(self, *filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
        #         {
        #         	t.init()
        #         	return parseFiles(t, filenames...)
        #         }
        pass

    # c:\go\src\text\template\helper.go:115:20
    def ParseGlob(self, pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
        #         {
        #         	t.init()
        #         	return parseGlob(t, pattern)
        #         }
        pass

    # c:\go\src\text\template\option.go:42:20
    def Option(self, *opt: str) -> Optional['Template']:
        #         {
        #         	t.init()
        #         	for _, s := range opt {
        #         		t.setOption(s)
        #         	}
        #         	return t
        #         }
        pass

    # c:\go\src\text\template\option.go:50:20
    def setOption(self, opt: str) -> None:
        #         {
        #         	if opt == "" {
        #         		panic("empty option string")
        #         	}
        #         	elems := strings.Split(opt, "=")
        #         	switch len(elems) {
        #         	case 2:
        #         
        #         		switch elems[0] {
        #         		case "missingkey":
        #         			switch elems[1] {
        #         			case "invalid", "default":
        #         				t.option.missingKey = mapInvalid
        #         				return
        #         			case "zero":
        #         				t.option.missingKey = mapZeroValue
        #         				return
        #         			case "error":
        #         				t.option.missingKey = mapError
        #         				return
        #         			}
        #         		}
        #         	}
        #         	panic("unrecognized option: " + opt)
        #         }
        pass

    # c:\go\src\text\template\template.go:46:20
    def Name(self) -> str:
        #         {
        #         	return t.name
        #         }
        pass

    # c:\go\src\text\template\template.go:57:20
    def New(self, name: str) -> Optional['Template']:
        #         {
        #         	t.init()
        #         	nt := &Template{
        #         		name:		name,
        #         		common:		t.common,
        #         		leftDelim:	t.leftDelim,
        #         		rightDelim:	t.rightDelim,
        #         	}
        #         	return nt
        #         }
        pass

    # c:\go\src\text\template\template.go:69:20
    def init(self) -> None:
        #         {
        #         	if t.common == nil {
        #         		c := new(common)
        #         		c.tmpl = make(map[string]*Template)
        #         		c.parseFuncs = make(FuncMap)
        #         		c.execFuncs = make(map[string]reflect.Value)
        #         		t.common = c
        #         	}
        #         }
        pass

    # c:\go\src\text\template\template.go:85:20
    def Clone(self) -> Tuple[Optional['Template'], 'goext.error']:
        #         {
        #         	nt := t.copy(nil)
        #         	nt.init()
        #         	if t.common == nil {
        #         		return nt, nil
        #         	}
        #         	for k, v := range t.tmpl {
        #         		if k == t.name {
        #         			nt.tmpl[t.name] = nt
        #         			continue
        #         		}
        #         
        #         		tmpl := v.copy(nt.common)
        #         		nt.tmpl[k] = tmpl
        #         	}
        #         	t.muFuncs.RLock()
        #         	defer t.muFuncs.RUnlock()
        #         	for k, v := range t.parseFuncs {
        #         		nt.parseFuncs[k] = v
        #         	}
        #         	for k, v := range t.execFuncs {
        #         		nt.execFuncs[k] = v
        #         	}
        #         	return nt, nil
        #         }
        pass

    # c:\go\src\text\template\template.go:112:20
    def copy(self, c: Optional['common']) -> Optional['Template']:
        #         {
        #         	return &Template{
        #         		name:		t.name,
        #         		Tree:		t.Tree,
        #         		common:		c,
        #         		leftDelim:	t.leftDelim,
        #         		rightDelim:	t.rightDelim,
        #         	}
        #         }
        pass

    # c:\go\src\text\template\template.go:126:20
    def AddParseTree(self, name: str, tree: Optional[text_template_parse.Tree]) -> Tuple[Optional['Template'], 'goext.error']:
        #         {
        #         	t.init()
        #         	nt := t
        #         	if name != t.name {
        #         		nt = t.New(name)
        #         	}
        #         
        #         	if t.associate(nt, tree) || nt.Tree == nil {
        #         		nt.Tree = tree
        #         	}
        #         	return nt, nil
        #         }
        pass

    # c:\go\src\text\template\template.go:140:20
    def Templates(self) -> List[Optional['Template']]:
        #         {
        #         	if t.common == nil {
        #         		return nil
        #         	}
        #         
        #         	m := make([]*Template, 0, len(t.tmpl))
        #         	for _, v := range t.tmpl {
        #         		m = append(m, v)
        #         	}
        #         	return m
        #         }
        pass

    # c:\go\src\text\template\template.go:157:20
    def Delims(self, left: str, right: str) -> Optional['Template']:
        #         {
        #         	t.init()
        #         	t.leftDelim = left
        #         	t.rightDelim = right
        #         	return t
        #         }
        pass

    # c:\go\src\text\template\template.go:170:20
    def Funcs(self, funcMap: 'FuncMap') -> Optional['Template']:
        #         {
        #         	t.init()
        #         	t.muFuncs.Lock()
        #         	defer t.muFuncs.Unlock()
        #         	addValueFuncs(t.execFuncs, funcMap)
        #         	addFuncs(t.parseFuncs, funcMap)
        #         	return t
        #         }
        pass

    # c:\go\src\text\template\template.go:181:20
    def Lookup(self, name: str) -> Optional['Template']:
        #         {
        #         	if t.common == nil {
        #         		return nil
        #         	}
        #         	return t.tmpl[name]
        #         }
        pass

    # c:\go\src\text\template\template.go:198:20
    def Parse(self, text: str) -> Tuple[Optional['Template'], 'goext.error']:
        #         {
        #         	t.init()
        #         	t.muFuncs.RLock()
        #         	trees, err := parse.Parse(t.name, text, t.leftDelim, t.rightDelim, t.parseFuncs, builtins())
        #         	t.muFuncs.RUnlock()
        #         	if err != nil {
        #         		return nil, err
        #         	}
        #         
        #         	for name, tree := range trees {
        #         		if _, err := t.AddParseTree(name, tree); err != nil {
        #         			return nil, err
        #         		}
        #         	}
        #         	return t, nil
        #         }
        pass

    # c:\go\src\text\template\template.go:218:20
    def associate(self, new: Optional['Template'], tree: Optional[text_template_parse.Tree]) -> bool:
        #         {
        #         	if new.common != t.common {
        #         		panic("internal error: associate not common")
        #         	}
        #         	if old := t.tmpl[new.name]; old != nil && parse.IsEmptyTree(tree.Root) && old.Tree != nil {
        #         
        #         		return false
        #         	}
        #         	t.tmpl[new.name] = new
        #         	return true
        #         }
        pass


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
        #         {
        #         	s.vars = append(s.vars, variable{name, value})
        #         }
        pass

    # c:\go\src\text\template\exec.go:53:17
    def mark(self) -> int:
        #         {
        #         	return len(s.vars)
        #         }
        pass

    # c:\go\src\text\template\exec.go:58:17
    def pop(self, mark: int) -> None:
        #         {
        #         	s.vars = s.vars[0:mark]
        #         }
        pass

    # c:\go\src\text\template\exec.go:64:17
    def setVar(self, name: str, value: goext.reflect_Value) -> None:
        #         {
        #         	for i := s.mark() - 1; i >= 0; i-- {
        #         		if s.vars[i].name == name {
        #         			s.vars[i].value = value
        #         			return
        #         		}
        #         	}
        #         	s.errorf("undefined variable: %!s(MISSING)", name)
        #         }
        pass

    # c:\go\src\text\template\exec.go:75:17
    def setTopVar(self, n: int, value: goext.reflect_Value) -> None:
        #         {
        #         	s.vars[len(s.vars)-n].value = value
        #         }
        pass

    # c:\go\src\text\template\exec.go:80:17
    def varValue(self, name: str) -> goext.reflect_Value:
        #         {
        #         	for i := s.mark() - 1; i >= 0; i-- {
        #         		if s.vars[i].name == name {
        #         			return s.vars[i].value
        #         		}
        #         	}
        #         	s.errorf("undefined variable: %!s(MISSING)", name)
        #         	return zero
        #         }
        pass

    # c:\go\src\text\template\exec.go:97:17
    def at(self, node: text_template_parse.Node) -> None:
        #         {
        #         	s.node = node
        #         }
        pass

    # c:\go\src\text\template\exec.go:128:17
    def errorf(self, format: str, *args: Any) -> None:
        #         {
        #         	name := doublePercent(s.tmpl.Name())
        #         	if s.node == nil {
        #         		format = fmt.Sprintf("template: %!s(MISSING): %!s(MISSING)", name, format)
        #         	} else {
        #         		location, context := s.tmpl.ErrorContext(s.node)
        #         		format = fmt.Sprintf("template: %!s(MISSING): executing %!q(MISSING) at <%!s(MISSING)>: %!s(MISSING)", location, name, doublePercent(context), format)
        #         	}
        #         	panic(ExecError{
        #         		Name:	s.tmpl.Name(),
        #         		Err:	fmt.Errorf(format, args...),
        #         	})
        #         }
        pass

    # c:\go\src\text\template\exec.go:150:17
    def writeError(self, err: 'goext.error') -> None:
        #         {
        #         	panic(writeError{
        #         		Err: err,
        #         	})
        #         }
        pass

    # c:\go\src\text\template\exec.go:249:17
    def walk(self, dot: goext.reflect_Value, node: text_template_parse.Node) -> None:
        #         {
        #         	s.at(node)
        #         	switch node := node.(type) {
        #         	case *parse.ActionNode:
        #         
        #         		val := s.evalPipeline(dot, node.Pipe)
        #         		if len(node.Pipe.Decl) == 0 {
        #         			s.printValue(node, val)
        #         		}
        #         	case *parse.IfNode:
        #         		s.walkIfOrWith(parse.NodeIf, dot, node.Pipe, node.List, node.ElseList)
        #         	case *parse.ListNode:
        #         		for _, node := range node.Nodes {
        #         			s.walk(dot, node)
        #         		}
        #         	case *parse.RangeNode:
        #         		s.walkRange(dot, node)
        #         	case *parse.TemplateNode:
        #         		s.walkTemplate(dot, node)
        #         	case *parse.TextNode:
        #         		if _, err := s.wr.Write(node.Text); err != nil {
        #         			s.writeError(err)
        #         		}
        #         	case *parse.WithNode:
        #         		s.walkIfOrWith(parse.NodeWith, dot, node.Pipe, node.List, node.ElseList)
        #         	default:
        #         		s.errorf("unknown node: %!s(MISSING)", node)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\exec.go:282:17
    def walkIfOrWith(self, typ: text_template_parse.NodeType, dot: goext.reflect_Value, pipe: Optional[text_template_parse.PipeNode], list: Optional[text_template_parse.ListNode], elseList: Optional[text_template_parse.ListNode]) -> None:
        #         {
        #         	defer s.pop(s.mark())
        #         	val := s.evalPipeline(dot, pipe)
        #         	truth, ok := isTrue(indirectInterface(val))
        #         	if !ok {
        #         		s.errorf("if/with can't use %!v(MISSING)", val)
        #         	}
        #         	if truth {
        #         		if typ == parse.NodeWith {
        #         			s.walk(val, list)
        #         		} else {
        #         			s.walk(dot, list)
        #         		}
        #         	} else if elseList != nil {
        #         		s.walk(dot, elseList)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\exec.go:335:17
    def walkRange(self, dot: goext.reflect_Value, r: Optional[text_template_parse.RangeNode]) -> None:
        #         {
        #         	s.at(r)
        #         	defer s.pop(s.mark())
        #         	val, _ := indirect(s.evalPipeline(dot, r.Pipe))
        #         
        #         	mark := s.mark()
        #         	oneIteration := func(index, elem reflect.Value) {
        #         
        #         		if len(r.Pipe.Decl) > 0 {
        #         			s.setTopVar(1, elem)
        #         		}
        #         
        #         		if len(r.Pipe.Decl) > 1 {
        #         			s.setTopVar(2, index)
        #         		}
        #         		s.walk(elem, r.List)
        #         		s.pop(mark)
        #         	}
        #         	switch val.Kind() {
        #         	case reflect.Array, reflect.Slice:
        #         		if val.Len() == 0 {
        #         			break
        #         		}
        #         		for i := 0; i < val.Len(); i++ {
        #         			oneIteration(reflect.ValueOf(i), val.Index(i))
        #         		}
        #         		return
        #         	case reflect.Map:
        #         		if val.Len() == 0 {
        #         			break
        #         		}
        #         		om := fmtsort.Sort(val)
        #         		for i, key := range om.Key {
        #         			oneIteration(key, om.Value[i])
        #         		}
        #         		return
        #         	case reflect.Chan:
        #         		if val.IsNil() {
        #         			break
        #         		}
        #         		i := 0
        #         		for ; ; i++ {
        #         			elem, ok := val.Recv()
        #         			if !ok {
        #         				break
        #         			}
        #         			oneIteration(reflect.ValueOf(i), elem)
        #         		}
        #         		if i == 0 {
        #         			break
        #         		}
        #         		return
        #         	case reflect.Invalid:
        #         		break
        #         	default:
        #         		s.errorf("range can't iterate over %!v(MISSING)", val)
        #         	}
        #         	if r.ElseList != nil {
        #         		s.walk(dot, r.ElseList)
        #         	}
        #         }
        pass

    # c:\go\src\text\template\exec.go:397:17
    def walkTemplate(self, dot: goext.reflect_Value, t: Optional[text_template_parse.TemplateNode]) -> None:
        #         {
        #         	s.at(t)
        #         	tmpl := s.tmpl.tmpl[t.Name]
        #         	if tmpl == nil {
        #         		s.errorf("template %!q(MISSING) not defined", t.Name)
        #         	}
        #         	if s.depth == maxExecDepth {
        #         		s.errorf("exceeded maximum template depth (%!v(MISSING))", maxExecDepth)
        #         	}
        #         
        #         	dot = s.evalPipeline(dot, t.Pipe)
        #         	newState := *s
        #         	newState.depth++
        #         	newState.tmpl = tmpl
        #         
        #         	newState.vars = []variable{{"$", dot}}
        #         	newState.walk(dot, tmpl.Root)
        #         }
        pass

    # c:\go\src\text\template\exec.go:424:17
    def evalPipeline(self, dot: goext.reflect_Value, pipe: Optional[text_template_parse.PipeNode]) -> goext.reflect_Value:
        #         {
        #         	if pipe == nil {
        #         		return
        #         	}
        #         	s.at(pipe)
        #         	value = missingVal
        #         	for _, cmd := range pipe.Cmds {
        #         		value = s.evalCommand(dot, cmd, value)
        #         
        #         		if value.Kind() == reflect.Interface && value.Type().NumMethod() == 0 {
        #         			value = reflect.ValueOf(value.Interface())
        #         		}
        #         	}
        #         	for _, variable := range pipe.Decl {
        #         		if pipe.IsAssign {
        #         			s.setVar(variable.Ident[0], value)
        #         		} else {
        #         			s.push(variable.Ident[0], value)
        #         		}
        #         	}
        #         	return value
        #         }
        pass

    # c:\go\src\text\template\exec.go:447:17
    def notAFunction(self, args: List[text_template_parse.Node], final: goext.reflect_Value) -> None:
        #         {
        #         	if len(args) > 1 || final != missingVal {
        #         		s.errorf("can't give argument to non-function %!s(MISSING)", args[0])
        #         	}
        #         }
        pass

    # c:\go\src\text\template\exec.go:453:17
    def evalCommand(self, dot: goext.reflect_Value, cmd: Optional[text_template_parse.CommandNode], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	firstWord := cmd.Args[0]
        #         	switch n := firstWord.(type) {
        #         	case *parse.FieldNode:
        #         		return s.evalFieldNode(dot, n, cmd.Args, final)
        #         	case *parse.ChainNode:
        #         		return s.evalChainNode(dot, n, cmd.Args, final)
        #         	case *parse.IdentifierNode:
        #         
        #         		return s.evalFunction(dot, n, cmd, cmd.Args, final)
        #         	case *parse.PipeNode:
        #         
        #         		s.notAFunction(cmd.Args, final)
        #         		return s.evalPipeline(dot, n)
        #         	case *parse.VariableNode:
        #         		return s.evalVariableNode(dot, n, cmd.Args, final)
        #         	}
        #         	s.at(firstWord)
        #         	s.notAFunction(cmd.Args, final)
        #         	switch word := firstWord.(type) {
        #         	case *parse.BoolNode:
        #         		return reflect.ValueOf(word.True)
        #         	case *parse.DotNode:
        #         		return dot
        #         	case *parse.NilNode:
        #         		s.errorf("nil is not a command")
        #         	case *parse.NumberNode:
        #         		return s.idealConstant(word)
        #         	case *parse.StringNode:
        #         		return reflect.ValueOf(word.Text)
        #         	}
        #         	s.errorf("can't evaluate command %!q(MISSING)", firstWord)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:492:17
    def idealConstant(self, constant: Optional[text_template_parse.NumberNode]) -> goext.reflect_Value:
        #         {
        #         
        #         	s.at(constant)
        #         	switch {
        #         	case constant.IsComplex:
        #         		return reflect.ValueOf(constant.Complex128)
        #         
        #         	case constant.IsFloat &&
        #         		!isHexInt(constant.Text) && !isRuneInt(constant.Text) &&
        #         		strings.ContainsAny(constant.Text, ".eEpP"):
        #         		return reflect.ValueOf(constant.Float64)
        #         
        #         	case constant.IsInt:
        #         		n := int(constant.Int64)
        #         		if int64(n) != constant.Int64 {
        #         			s.errorf("%!s(MISSING) overflows int", constant.Text)
        #         		}
        #         		return reflect.ValueOf(n)
        #         
        #         	case constant.IsUint:
        #         		s.errorf("%!s(MISSING) overflows int", constant.Text)
        #         	}
        #         	return zero
        #         }
        pass

    # c:\go\src\text\template\exec.go:527:17
    def evalFieldNode(self, dot: goext.reflect_Value, field: Optional[text_template_parse.FieldNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	s.at(field)
        #         	return s.evalFieldChain(dot, dot, field, field.Ident, args, final)
        #         }
        pass

    # c:\go\src\text\template\exec.go:532:17
    def evalChainNode(self, dot: goext.reflect_Value, chain: Optional[text_template_parse.ChainNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	s.at(chain)
        #         	if len(chain.Field) == 0 {
        #         		s.errorf("internal error: no fields in evalChainNode")
        #         	}
        #         	if chain.Node.Type() == parse.NodeNil {
        #         		s.errorf("indirection through explicit nil in %!s(MISSING)", chain)
        #         	}
        #         
        #         	pipe := s.evalArg(dot, nil, chain.Node)
        #         	return s.evalFieldChain(dot, pipe, chain, chain.Field, args, final)
        #         }
        pass

    # c:\go\src\text\template\exec.go:545:17
    def evalVariableNode(self, dot: goext.reflect_Value, variable: Optional[text_template_parse.VariableNode], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         
        #         	s.at(variable)
        #         	value := s.varValue(variable.Ident[0])
        #         	if len(variable.Ident) == 1 {
        #         		s.notAFunction(args, final)
        #         		return value
        #         	}
        #         	return s.evalFieldChain(dot, value, variable, variable.Ident[1:], args, final)
        #         }
        pass

    # c:\go\src\text\template\exec.go:559:17
    def evalFieldChain(self, dot: goext.reflect_Value, receiver: goext.reflect_Value, node: text_template_parse.Node, ident: List[str], args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	n := len(ident)
        #         	for i := 0; i < n-1; i++ {
        #         		receiver = s.evalField(dot, ident[i], node, nil, missingVal, receiver)
        #         	}
        #         
        #         	return s.evalField(dot, ident[n-1], node, args, final, receiver)
        #         }
        pass

    # c:\go\src\text\template\exec.go:568:17
    def evalFunction(self, dot: goext.reflect_Value, node: Optional[text_template_parse.IdentifierNode], cmd: text_template_parse.Node, args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	s.at(node)
        #         	name := node.Ident
        #         	function, ok := findFunction(name, s.tmpl)
        #         	if !ok {
        #         		s.errorf("%!q(MISSING) is not a defined function", name)
        #         	}
        #         	return s.evalCall(dot, function, cmd, name, args, final)
        #         }
        pass

    # c:\go\src\text\template\exec.go:581:17
    def evalField(self, dot: goext.reflect_Value, fieldName: str, node: text_template_parse.Node, args: List[text_template_parse.Node], final: goext.reflect_Value, receiver: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	if !receiver.IsValid() {
        #         		if s.tmpl.option.missingKey == mapError {
        #         			s.errorf("nil data; no entry for key %!q(MISSING)", fieldName)
        #         		}
        #         		return zero
        #         	}
        #         	typ := receiver.Type()
        #         	receiver, isNil := indirect(receiver)
        #         	if receiver.Kind() == reflect.Interface && isNil {
        #         
        #         		s.errorf("nil pointer evaluating %!s(MISSING).%!s(MISSING)", typ, fieldName)
        #         		return zero
        #         	}
        #         
        #         	ptr := receiver
        #         	if ptr.Kind() != reflect.Interface && ptr.Kind() != reflect.Ptr && ptr.CanAddr() {
        #         		ptr = ptr.Addr()
        #         	}
        #         	if method := ptr.MethodByName(fieldName); method.IsValid() {
        #         		return s.evalCall(dot, method, node, fieldName, args, final)
        #         	}
        #         	hasArgs := len(args) > 1 || final != missingVal
        #         
        #         	switch receiver.Kind() {
        #         	case reflect.Struct:
        #         		tField, ok := receiver.Type().FieldByName(fieldName)
        #         		if ok {
        #         			field := receiver.FieldByIndex(tField.Index)
        #         			if tField.PkgPath != "" {
        #         				s.errorf("%!s(MISSING) is an unexported field of struct type %!s(MISSING)", fieldName, typ)
        #         			}
        #         
        #         			if hasArgs {
        #         				s.errorf("%!s(MISSING) has arguments but cannot be invoked as function", fieldName)
        #         			}
        #         			return field
        #         		}
        #         	case reflect.Map:
        #         
        #         		nameVal := reflect.ValueOf(fieldName)
        #         		if nameVal.Type().AssignableTo(receiver.Type().Key()) {
        #         			if hasArgs {
        #         				s.errorf("%!s(MISSING) is not a method but has arguments", fieldName)
        #         			}
        #         			result := receiver.MapIndex(nameVal)
        #         			if !result.IsValid() {
        #         				switch s.tmpl.option.missingKey {
        #         				case mapInvalid:
        #         
        #         				case mapZeroValue:
        #         					result = reflect.Zero(receiver.Type().Elem())
        #         				case mapError:
        #         					s.errorf("map has no entry for key %!q(MISSING)", fieldName)
        #         				}
        #         			}
        #         			return result
        #         		}
        #         	case reflect.Ptr:
        #         		etyp := receiver.Type().Elem()
        #         		if etyp.Kind() == reflect.Struct {
        #         			if _, ok := etyp.FieldByName(fieldName); !ok {
        #         
        #         				break
        #         			}
        #         		}
        #         		if isNil {
        #         			s.errorf("nil pointer evaluating %!s(MISSING).%!s(MISSING)", typ, fieldName)
        #         		}
        #         	}
        #         	s.errorf("can't evaluate field %!s(MISSING) in type %!s(MISSING)", fieldName, typ)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:668:17
    def evalCall(self, dot: goext.reflect_Value, fun: goext.reflect_Value, node: text_template_parse.Node, name: str, args: List[text_template_parse.Node], final: goext.reflect_Value) -> goext.reflect_Value:
        #         {
        #         	if args != nil {
        #         		args = args[1:]
        #         	}
        #         	typ := fun.Type()
        #         	numIn := len(args)
        #         	if final != missingVal {
        #         		numIn++
        #         	}
        #         	numFixed := len(args)
        #         	if typ.IsVariadic() {
        #         		numFixed = typ.NumIn() - 1
        #         		if numIn < numFixed {
        #         			s.errorf("wrong number of args for %!s(MISSING): want at least %!d(MISSING) got %!d(MISSING)", name, typ.NumIn()-1, len(args))
        #         		}
        #         	} else if numIn != typ.NumIn() {
        #         		s.errorf("wrong number of args for %!s(MISSING): want %!d(MISSING) got %!d(MISSING)", name, typ.NumIn(), numIn)
        #         	}
        #         	if !goodFunc(typ) {
        #         
        #         		s.errorf("can't call method/function %!q(MISSING) with %!d(MISSING) results", name, typ.NumOut())
        #         	}
        #         
        #         	argv := make([]reflect.Value, numIn)
        #         
        #         	i := 0
        #         	for ; i < numFixed && i < len(args); i++ {
        #         		argv[i] = s.evalArg(dot, typ.In(i), args[i])
        #         	}
        #         
        #         	if typ.IsVariadic() {
        #         		argType := typ.In(typ.NumIn() - 1).Elem()
        #         		for ; i < len(args); i++ {
        #         			argv[i] = s.evalArg(dot, argType, args[i])
        #         		}
        #         	}
        #         
        #         	if final != missingVal {
        #         		t := typ.In(typ.NumIn() - 1)
        #         		if typ.IsVariadic() {
        #         			if numIn-1 < numFixed {
        #         
        #         				t = typ.In(numIn - 1)
        #         			} else {
        #         
        #         				t = t.Elem()
        #         			}
        #         		}
        #         		argv[i] = s.validateType(final, t)
        #         	}
        #         	v, err := safeCall(fun, argv)
        #         
        #         	if err != nil {
        #         		s.at(node)
        #         		s.errorf("error calling %!s(MISSING): %!v(MISSING)", name, err)
        #         	}
        #         	if v.Type() == reflectValueType {
        #         		v = v.Interface().(reflect.Value)
        #         	}
        #         	return v
        #         }
        pass

    # c:\go\src\text\template\exec.go:745:17
    def validateType(self, value: goext.reflect_Value, typ: goext.reflect_Type) -> goext.reflect_Value:
        #         {
        #         	if !value.IsValid() {
        #         		if typ == nil {
        #         
        #         			return reflect.ValueOf(nil)
        #         		}
        #         		if canBeNil(typ) {
        #         
        #         			return reflect.Zero(typ)
        #         		}
        #         		s.errorf("invalid value; expected %!s(MISSING)", typ)
        #         	}
        #         	if typ == reflectValueType && value.Type() != typ {
        #         		return reflect.ValueOf(value)
        #         	}
        #         	if typ != nil && !value.Type().AssignableTo(typ) {
        #         		if value.Kind() == reflect.Interface && !value.IsNil() {
        #         			value = value.Elem()
        #         			if value.Type().AssignableTo(typ) {
        #         				return value
        #         			}
        #         
        #         		}
        #         
        #         		switch {
        #         		case value.Kind() == reflect.Ptr && value.Type().Elem().AssignableTo(typ):
        #         			value = value.Elem()
        #         			if !value.IsValid() {
        #         				s.errorf("dereference of nil pointer of type %!s(MISSING)", typ)
        #         			}
        #         		case reflect.PtrTo(value.Type()).AssignableTo(typ) && value.CanAddr():
        #         			value = value.Addr()
        #         		default:
        #         			s.errorf("wrong type for value; expected %!s(MISSING); got %!s(MISSING)", typ, value.Type())
        #         		}
        #         	}
        #         	return value
        #         }
        pass

    # c:\go\src\text\template\exec.go:787:17
    def evalArg(self, dot: goext.reflect_Value, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	switch arg := n.(type) {
        #         	case *parse.DotNode:
        #         		return s.validateType(dot, typ)
        #         	case *parse.NilNode:
        #         		if canBeNil(typ) {
        #         			return reflect.Zero(typ)
        #         		}
        #         		s.errorf("cannot assign nil to %!s(MISSING)", typ)
        #         	case *parse.FieldNode:
        #         		return s.validateType(s.evalFieldNode(dot, arg, []parse.Node{n}, missingVal), typ)
        #         	case *parse.VariableNode:
        #         		return s.validateType(s.evalVariableNode(dot, arg, nil, missingVal), typ)
        #         	case *parse.PipeNode:
        #         		return s.validateType(s.evalPipeline(dot, arg), typ)
        #         	case *parse.IdentifierNode:
        #         		return s.validateType(s.evalFunction(dot, arg, arg, nil, missingVal), typ)
        #         	case *parse.ChainNode:
        #         		return s.validateType(s.evalChainNode(dot, arg, nil, missingVal), typ)
        #         	}
        #         	switch typ.Kind() {
        #         	case reflect.Bool:
        #         		return s.evalBool(typ, n)
        #         	case reflect.Complex64, reflect.Complex128:
        #         		return s.evalComplex(typ, n)
        #         	case reflect.Float32, reflect.Float64:
        #         		return s.evalFloat(typ, n)
        #         	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
        #         		return s.evalInteger(typ, n)
        #         	case reflect.Interface:
        #         		if typ.NumMethod() == 0 {
        #         			return s.evalEmptyInterface(dot, n)
        #         		}
        #         	case reflect.Struct:
        #         		if typ == reflectValueType {
        #         			return reflect.ValueOf(s.evalEmptyInterface(dot, n))
        #         		}
        #         	case reflect.String:
        #         		return s.evalString(typ, n)
        #         	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
        #         		return s.evalUnsignedInteger(typ, n)
        #         	}
        #         	s.errorf("can't handle %!s(MISSING) for arg of type %!s(MISSING)", n, typ)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:834:17
    def evalBool(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	if n, ok := n.(*parse.BoolNode); ok {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetBool(n.True)
        #         		return value
        #         	}
        #         	s.errorf("expected bool; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:845:17
    def evalString(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	if n, ok := n.(*parse.StringNode); ok {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetString(n.Text)
        #         		return value
        #         	}
        #         	s.errorf("expected string; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:856:17
    def evalInteger(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	if n, ok := n.(*parse.NumberNode); ok && n.IsInt {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetInt(n.Int64)
        #         		return value
        #         	}
        #         	s.errorf("expected integer; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:867:17
    def evalUnsignedInteger(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	if n, ok := n.(*parse.NumberNode); ok && n.IsUint {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetUint(n.Uint64)
        #         		return value
        #         	}
        #         	s.errorf("expected unsigned integer; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:878:17
    def evalFloat(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	if n, ok := n.(*parse.NumberNode); ok && n.IsFloat {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetFloat(n.Float64)
        #         		return value
        #         	}
        #         	s.errorf("expected float; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:889:17
    def evalComplex(self, typ: goext.reflect_Type, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	if n, ok := n.(*parse.NumberNode); ok && n.IsComplex {
        #         		value := reflect.New(typ).Elem()
        #         		value.SetComplex(n.Complex128)
        #         		return value
        #         	}
        #         	s.errorf("expected complex; found %!s(MISSING)", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:899:17
    def evalEmptyInterface(self, dot: goext.reflect_Value, n: text_template_parse.Node) -> goext.reflect_Value:
        #         {
        #         	s.at(n)
        #         	switch n := n.(type) {
        #         	case *parse.BoolNode:
        #         		return reflect.ValueOf(n.True)
        #         	case *parse.DotNode:
        #         		return dot
        #         	case *parse.FieldNode:
        #         		return s.evalFieldNode(dot, n, nil, missingVal)
        #         	case *parse.IdentifierNode:
        #         		return s.evalFunction(dot, n, n, nil, missingVal)
        #         	case *parse.NilNode:
        #         
        #         		s.errorf("evalEmptyInterface: nil (can't happen)")
        #         	case *parse.NumberNode:
        #         		return s.idealConstant(n)
        #         	case *parse.StringNode:
        #         		return reflect.ValueOf(n.Text)
        #         	case *parse.VariableNode:
        #         		return s.evalVariableNode(dot, n, nil, missingVal)
        #         	case *parse.PipeNode:
        #         		return s.evalPipeline(dot, n)
        #         	}
        #         	s.errorf("can't handle assignment of %!s(MISSING) to empty interface argument", n)
        #         	panic("not reached")
        #         }
        pass

    # c:\go\src\text\template\exec.go:954:17
    def printValue(self, n: text_template_parse.Node, v: goext.reflect_Value) -> None:
        #         {
        #         	s.at(n)
        #         	iface, ok := printableValue(v)
        #         	if !ok {
        #         		s.errorf("can't print %!s(MISSING) of type %!s(MISSING)", n, v.Type())
        #         	}
        #         	_, err := fmt.Fprint(s.wr, iface)
        #         	if err != nil {
        #         		s.writeError(err)
        #         	}
        #         }
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
    #     {
    #     	last := 0
    #     	for i, c := range b {
    #     		var html []byte
    #     		switch c {
    #     		case '\000':
    #     			html = htmlNull
    #     		case '"':
    #     			html = htmlQuot
    #     		case '\'':
    #     			html = htmlApos
    #     		case '&':
    #     			html = htmlAmp
    #     		case '<':
    #     			html = htmlLt
    #     		case '>':
    #     			html = htmlGt
    #     		default:
    #     			continue
    #     		}
    #     		w.Write(b[last:i])
    #     		w.Write(html)
    #     		last = i + 1
    #     	}
    #     	w.Write(b[last:])
    #     }
    pass


# c:\go\src\text\template\funcs.go:631:6
def HTMLEscapeString(s: str) -> str:
    #     {
    #     
    #     	if !strings.ContainsAny(s, "'\"&<>\000") {
    #     		return s
    #     	}
    #     	var b bytes.Buffer
    #     	HTMLEscape(&b, []byte(s))
    #     	return b.String()
    #     }
    pass


# c:\go\src\text\template\funcs.go:643:6
def HTMLEscaper(*args: Any) -> str:
    #     {
    #     	return HTMLEscapeString(evalArgs(args))
    #     }
    pass


# c:\go\src\text\template\exec.go:303:6
def IsTrue(val: Any) -> Tuple[bool, bool]:
    #     {
    #     	return isTrue(reflect.ValueOf(val))
    #     }
    pass


# c:\go\src\text\template\funcs.go:663:6
def JSEscape(w: goext.io_Writer, b: List[int]) -> None:
    #     {
    #     	last := 0
    #     	for i := 0; i < len(b); i++ {
    #     		c := b[i]
    #     
    #     		if !jsIsSpecial(rune(c)) {
    #     
    #     			continue
    #     		}
    #     		w.Write(b[last:i])
    #     
    #     		if c < utf8.RuneSelf {
    #     
    #     			switch c {
    #     			case '\\':
    #     				w.Write(jsBackslash)
    #     			case '\'':
    #     				w.Write(jsApos)
    #     			case '"':
    #     				w.Write(jsQuot)
    #     			case '<':
    #     				w.Write(jsLt)
    #     			case '>':
    #     				w.Write(jsGt)
    #     			case '&':
    #     				w.Write(jsAmp)
    #     			case '=':
    #     				w.Write(jsEq)
    #     			default:
    #     				w.Write(jsLowUni)
    #     				t, b := c>>4, c&0x0f
    #     				w.Write(hex[t : t+1])
    #     				w.Write(hex[b : b+1])
    #     			}
    #     		} else {
    #     
    #     			r, size := utf8.DecodeRune(b[i:])
    #     			if unicode.IsPrint(r) {
    #     				w.Write(b[i : i+size])
    #     			} else {
    #     				fmt.Fprintf(w, "\\u%!X(MISSING)", r)
    #     			}
    #     			i += size - 1
    #     		}
    #     		last = i + 1
    #     	}
    #     	w.Write(b[last:])
    #     }
    pass


# c:\go\src\text\template\funcs.go:714:6
def JSEscapeString(s: str) -> str:
    #     {
    #     
    #     	if strings.IndexFunc(s, jsIsSpecial) < 0 {
    #     		return s
    #     	}
    #     	var b bytes.Buffer
    #     	JSEscape(&b, []byte(s))
    #     	return b.String()
    #     }
    pass


# c:\go\src\text\template\funcs.go:734:6
def JSEscaper(*args: Any) -> str:
    #     {
    #     	return JSEscapeString(evalArgs(args))
    #     }
    pass


# c:\go\src\text\template\helper.go:21:6
def Must(t: Optional['Template'], err: 'goext.error') -> Optional['Template']:
    #     {
    #     	if err != nil {
    #     		panic(err)
    #     	}
    #     	return t
    #     }
    pass


# c:\go\src\text\template\template.go:37:6
def New(name: str) -> Optional['Template']:
    #     {
    #     	t := &Template{
    #     		name: name,
    #     	}
    #     	t.init()
    #     	return t
    #     }
    pass


# c:\go\src\text\template\helper.go:37:6
def ParseFiles(*filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
    #     {
    #     	return parseFiles(nil, filenames...)
    #     }
    pass


# c:\go\src\text\template\helper.go:103:6
def ParseGlob(pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
    #     {
    #     	return parseGlob(nil, pattern)
    #     }
    pass


# c:\go\src\text\template\funcs.go:740:6
def URLQueryEscaper(*args: Any) -> str:
    #     {
    #     	return url.QueryEscape(evalArgs(args))
    #     }
    pass


# c:\go\src\text\template\funcs.go:103:6
def addFuncs(out: 'FuncMap', in_: 'FuncMap') -> None:
    #     {
    #     	for name, fn := range in {
    #     		out[name] = fn
    #     	}
    #     }
    pass


# c:\go\src\text\template\funcs.go:85:6
def addValueFuncs(out: Dict[str, goext.reflect_Value], in_: 'FuncMap') -> None:
    #     {
    #     	for name, fn := range in {
    #     		if !goodName(name) {
    #     			panic(fmt.Errorf("function name %!q(MISSING) is not a valid identifier", name))
    #     		}
    #     		v := reflect.ValueOf(fn)
    #     		if v.Kind() != reflect.Func {
    #     			panic("value for " + name + " not a function")
    #     		}
    #     		if !goodFunc(v.Type()) {
    #     			panic(fmt.Errorf("can't install method/function %!q(MISSING) with %!d(MISSING) results", name, v.Type().NumOut()))
    #     		}
    #     		out[name] = v
    #     	}
    #     }
    pass


# c:\go\src\text\template\funcs.go:381:6
def and_(arg0: goext.reflect_Value, *args: goext.reflect_Value) -> goext.reflect_Value:
    #     {
    #     	if !truth(arg0) {
    #     		return arg0
    #     	}
    #     	for i := range args {
    #     		arg0 = args[i]
    #     		if !truth(arg0) {
    #     			break
    #     		}
    #     	}
    #     	return arg0
    #     }
    pass


# c:\go\src\text\template\funcs.go:436:6
def basicKind(v: goext.reflect_Value) -> Tuple['kind', 'goext.error']:
    #     {
    #     	switch v.Kind() {
    #     	case reflect.Bool:
    #     		return boolKind, nil
    #     	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    #     		return intKind, nil
    #     	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    #     		return uintKind, nil
    #     	case reflect.Float32, reflect.Float64:
    #     		return floatKind, nil
    #     	case reflect.Complex64, reflect.Complex128:
    #     		return complexKind, nil
    #     	case reflect.String:
    #     		return stringKind, nil
    #     	}
    #     	return invalidKind, errBadComparisonType
    #     }
    pass


# c:\go\src\text\template\funcs.go:70:6
def builtinFuncs() -> Dict[str, goext.reflect_Value]:
    #     {
    #     	builtinFuncsOnce.Do(func() {
    #     		builtinFuncsOnce.v = createValueFuncs(builtins())
    #     	})
    #     	return builtinFuncsOnce.v
    #     }
    pass


# c:\go\src\text\template\funcs.go:37:6
def builtins() -> 'FuncMap':
    #     {
    #     	return FuncMap{
    #     		"and":		and,
    #     		"call":		call,
    #     		"html":		HTMLEscaper,
    #     		"index":	index,
    #     		"slice":	slice,
    #     		"js":		JSEscaper,
    #     		"len":		length,
    #     		"not":		not,
    #     		"or":		or,
    #     		"print":	fmt.Sprint,
    #     		"printf":	fmt.Sprintf,
    #     		"println":	fmt.Sprintln,
    #     		"urlquery":	URLQueryEscaper,
    #     
    #     		"eq":	eq,
    #     		"ge":	ge,
    #     		"gt":	gt,
    #     		"le":	le,
    #     		"lt":	lt,
    #     		"ne":	ne,
    #     	}
    #     }
    pass


# c:\go\src\text\template\funcs.go:312:6
def call(fn: goext.reflect_Value, *args: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    #     {
    #     	fn = indirectInterface(fn)
    #     	if !fn.IsValid() {
    #     		return reflect.Value{}, fmt.Errorf("call of nil")
    #     	}
    #     	typ := fn.Type()
    #     	if typ.Kind() != reflect.Func {
    #     		return reflect.Value{}, fmt.Errorf("non-function of type %!s(MISSING)", typ)
    #     	}
    #     	if !goodFunc(typ) {
    #     		return reflect.Value{}, fmt.Errorf("function called with %!d(MISSING) args; should be 1 or 2", typ.NumOut())
    #     	}
    #     	numIn := typ.NumIn()
    #     	var dddType reflect.Type
    #     	if typ.IsVariadic() {
    #     		if len(args) < numIn-1 {
    #     			return reflect.Value{}, fmt.Errorf("wrong number of args: got %!d(MISSING) want at least %!d(MISSING)", len(args), numIn-1)
    #     		}
    #     		dddType = typ.In(numIn - 1).Elem()
    #     	} else {
    #     		if len(args) != numIn {
    #     			return reflect.Value{}, fmt.Errorf("wrong number of args: got %!d(MISSING) want %!d(MISSING)", len(args), numIn)
    #     		}
    #     	}
    #     	argv := make([]reflect.Value, len(args))
    #     	for i, arg := range args {
    #     		arg = indirectInterface(arg)
    #     
    #     		argType := dddType
    #     		if !typ.IsVariadic() || i < numIn-1 {
    #     			argType = typ.In(i)
    #     		}
    #     
    #     		var err error
    #     		if argv[i], err = prepareArg(arg, argType); err != nil {
    #     			return reflect.Value{}, fmt.Errorf("arg %!d(MISSING): %!s(MISSING)", i, err)
    #     		}
    #     	}
    #     	return safeCall(fn, argv)
    #     }
    pass


# c:\go\src\text\template\exec.go:734:6
def canBeNil(typ: goext.reflect_Type) -> bool:
    #     {
    #     	switch typ.Kind() {
    #     	case reflect.Chan, reflect.Func, reflect.Interface, reflect.Map, reflect.Ptr, reflect.Slice:
    #     		return true
    #     	case reflect.Struct:
    #     		return typ == reflectValueType
    #     	}
    #     	return false
    #     }
    pass


# c:\go\src\text\template\funcs.go:78:6
def createValueFuncs(funcMap: 'FuncMap') -> Dict[str, goext.reflect_Value]:
    #     {
    #     	m := make(map[string]reflect.Value)
    #     	addValueFuncs(m, funcMap)
    #     	return m
    #     }
    pass


# c:\go\src\text\template\exec.go:103:6
def doublePercent(str: str) -> str:
    #     {
    #     	return strings.ReplaceAll(str, "%!"(MISSING), "%")
    #     }
    pass


# c:\go\src\text\template\funcs.go:455:6
def eq(arg1: goext.reflect_Value, *arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     	arg1 = indirectInterface(arg1)
    #     	if arg1 != zero {
    #     		if t1 := arg1.Type(); !t1.Comparable() {
    #     			return false, fmt.Errorf("uncomparable type %!s(MISSING): %!v(MISSING)", t1, arg1)
    #     		}
    #     	}
    #     	if len(arg2) == 0 {
    #     		return false, errNoComparison
    #     	}
    #     	k1, _ := basicKind(arg1)
    #     	for _, arg := range arg2 {
    #     		arg = indirectInterface(arg)
    #     		k2, _ := basicKind(arg)
    #     		truth := false
    #     		if k1 != k2 {
    #     
    #     			switch {
    #     			case k1 == intKind && k2 == uintKind:
    #     				truth = arg1.Int() >= 0 && uint64(arg1.Int()) == arg.Uint()
    #     			case k1 == uintKind && k2 == intKind:
    #     				truth = arg.Int() >= 0 && arg1.Uint() == uint64(arg.Int())
    #     			default:
    #     				return false, errBadComparison
    #     			}
    #     		} else {
    #     			switch k1 {
    #     			case boolKind:
    #     				truth = arg1.Bool() == arg.Bool()
    #     			case complexKind:
    #     				truth = arg1.Complex() == arg.Complex()
    #     			case floatKind:
    #     				truth = arg1.Float() == arg.Float()
    #     			case intKind:
    #     				truth = arg1.Int() == arg.Int()
    #     			case stringKind:
    #     				truth = arg1.String() == arg.String()
    #     			case uintKind:
    #     				truth = arg1.Uint() == arg.Uint()
    #     			default:
    #     				if arg == zero {
    #     					truth = arg1 == arg
    #     				} else {
    #     					if t2 := arg.Type(); !t2.Comparable() {
    #     						return false, fmt.Errorf("uncomparable type %!s(MISSING): %!v(MISSING)", t2, arg)
    #     					}
    #     					truth = arg1.Interface() == arg.Interface()
    #     				}
    #     			}
    #     		}
    #     		if truth {
    #     			return true, nil
    #     		}
    #     	}
    #     	return false, nil
    #     }
    pass


# c:\go\src\text\template\exec.go:158:6
def errRecover(errp: Optional['goext.error']) -> None:
    #     {
    #     	e := recover()
    #     	if e != nil {
    #     		switch err := e.(type) {
    #     		case runtime.Error:
    #     			panic(e)
    #     		case writeError:
    #     			*errp = err.Err
    #     		case ExecError:
    #     			*errp = err
    #     		default:
    #     			panic(e)
    #     		}
    #     	}
    #     }
    pass


# c:\go\src\text\template\funcs.go:749:6
def evalArgs(args: List[Any]) -> str:
    #     {
    #     	ok := false
    #     	var s string
    #     
    #     	if len(args) == 1 {
    #     		s, ok = args[0].(string)
    #     	}
    #     	if !ok {
    #     		for i, arg := range args {
    #     			a, ok := printableValue(reflect.ValueOf(arg))
    #     			if ok {
    #     				args[i] = a
    #     			}
    #     		}
    #     		s = fmt.Sprint(args...)
    #     	}
    #     	return s
    #     }
    pass


# c:\go\src\text\template\funcs.go:139:6
def findFunction(name: str, tmpl: Optional['Template']) -> Tuple[goext.reflect_Value, bool]:
    #     {
    #     	if tmpl != nil && tmpl.common != nil {
    #     		tmpl.muFuncs.RLock()
    #     		defer tmpl.muFuncs.RUnlock()
    #     		if fn := tmpl.execFuncs[name]; fn.IsValid() {
    #     			return fn, true
    #     		}
    #     	}
    #     	if fn := builtinFuncs()[name]; fn.IsValid() {
    #     		return fn, true
    #     	}
    #     	return reflect.Value{}, false
    #     }
    pass


# c:\go\src\text\template\funcs.go:582:6
def ge(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     
    #     	lessThan, err := lt(arg1, arg2)
    #     	if err != nil {
    #     		return false, err
    #     	}
    #     	return !lessThan, nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:110:6
def goodFunc(typ: goext.reflect_Type) -> bool:
    #     {
    #     
    #     	switch {
    #     	case typ.NumOut() == 1:
    #     		return true
    #     	case typ.NumOut() == 2 && typ.Out(1) == errorType:
    #     		return true
    #     	}
    #     	return false
    #     }
    pass


# c:\go\src\text\template\funcs.go:122:6
def goodName(name: str) -> bool:
    #     {
    #     	if name == "" {
    #     		return false
    #     	}
    #     	for i, r := range name {
    #     		switch {
    #     		case r == '_':
    #     		case i == 0 && !unicode.IsLetter(r):
    #     			return false
    #     		case !unicode.IsLetter(r) && !unicode.IsDigit(r):
    #     			return false
    #     		}
    #     	}
    #     	return true
    #     }
    pass


# c:\go\src\text\template\funcs.go:572:6
def gt(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     
    #     	lessOrEqual, err := le(arg1, arg2)
    #     	if err != nil {
    #     		return false, err
    #     	}
    #     	return !lessOrEqual, nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:206:6
def index(item: goext.reflect_Value, *indexes: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    #     {
    #     	item = indirectInterface(item)
    #     	if !item.IsValid() {
    #     		return reflect.Value{}, fmt.Errorf("index of untyped nil")
    #     	}
    #     	for _, index := range indexes {
    #     		index = indirectInterface(index)
    #     		var isNil bool
    #     		if item, isNil = indirect(item); isNil {
    #     			return reflect.Value{}, fmt.Errorf("index of nil pointer")
    #     		}
    #     		switch item.Kind() {
    #     		case reflect.Array, reflect.Slice, reflect.String:
    #     			x, err := indexArg(index, item.Len())
    #     			if err != nil {
    #     				return reflect.Value{}, err
    #     			}
    #     			item = item.Index(x)
    #     		case reflect.Map:
    #     			index, err := prepareArg(index, item.Type().Key())
    #     			if err != nil {
    #     				return reflect.Value{}, err
    #     			}
    #     			if x := item.MapIndex(index); x.IsValid() {
    #     				item = x
    #     			} else {
    #     				item = reflect.Zero(item.Type().Elem())
    #     			}
    #     		case reflect.Invalid:
    #     
    #     			panic("unreachable")
    #     		default:
    #     			return reflect.Value{}, fmt.Errorf("can't index item of type %!s(MISSING)", item.Type())
    #     		}
    #     	}
    #     	return item, nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:183:6
def indexArg(index: goext.reflect_Value, cap: int) -> Tuple[int, 'goext.error']:
    #     {
    #     	var x int64
    #     	switch index.Kind() {
    #     	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    #     		x = index.Int()
    #     	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    #     		x = int64(index.Uint())
    #     	case reflect.Invalid:
    #     		return 0, fmt.Errorf("cannot index slice/array with nil")
    #     	default:
    #     		return 0, fmt.Errorf("cannot index slice/array with type %!s(MISSING)", index.Type())
    #     	}
    #     	if x < 0 || int(x) < 0 || int(x) > cap {
    #     		return 0, fmt.Errorf("index out of range: %!d(MISSING)", x)
    #     	}
    #     	return int(x), nil
    #     }
    pass


# c:\go\src\text\template\exec.go:929:6
def indirect(v: goext.reflect_Value) -> Tuple[goext.reflect_Value, bool]:
    #     {
    #     	for ; v.Kind() == reflect.Ptr || v.Kind() == reflect.Interface; v = v.Elem() {
    #     		if v.IsNil() {
    #     			return v, true
    #     		}
    #     	}
    #     	return v, false
    #     }
    pass


# c:\go\src\text\template\exec.go:942:6
def indirectInterface(v: goext.reflect_Value) -> goext.reflect_Value:
    #     {
    #     	if v.Kind() != reflect.Interface {
    #     		return v
    #     	}
    #     	if v.IsNil() {
    #     		return reflect.Value{}
    #     	}
    #     	return v.Elem()
    #     }
    pass


# c:\go\src\text\template\exec.go:23:6
def initMaxExecDepth() -> int:
    #     {
    #     	if runtime.GOARCH == "wasm" {
    #     		return 1000
    #     	}
    #     	return 100000
    #     }
    pass


# c:\go\src\text\template\funcs.go:172:6
def intLike(typ: goext.reflect_Kind) -> bool:
    #     {
    #     	switch typ {
    #     	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    #     		return true
    #     	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    #     		return true
    #     	}
    #     	return false
    #     }
    pass


# c:\go\src\text\template\exec.go:523:6
def isHexInt(s: str) -> bool:
    #     {
    #     	return len(s) > 2 && s[0] == '0' && (s[1] == 'x' || s[1] == 'X') && !strings.ContainsAny(s, "pP")
    #     }
    pass


# c:\go\src\text\template\exec.go:519:6
def isRuneInt(s: str) -> bool:
    #     {
    #     	return len(s) > 0 && s[0] == '\''
    #     }
    pass


# c:\go\src\text\template\exec.go:307:6
def isTrue(val: goext.reflect_Value) -> Tuple[bool, bool]:
    #     {
    #     	if !val.IsValid() {
    #     
    #     		return false, true
    #     	}
    #     	switch val.Kind() {
    #     	case reflect.Array, reflect.Map, reflect.Slice, reflect.String:
    #     		truth = val.Len() > 0
    #     	case reflect.Bool:
    #     		truth = val.Bool()
    #     	case reflect.Complex64, reflect.Complex128:
    #     		truth = val.Complex() != 0
    #     	case reflect.Chan, reflect.Func, reflect.Ptr, reflect.Interface:
    #     		truth = !val.IsNil()
    #     	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
    #     		truth = val.Int() != 0
    #     	case reflect.Float32, reflect.Float64:
    #     		truth = val.Float() != 0
    #     	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
    #     		truth = val.Uint() != 0
    #     	case reflect.Struct:
    #     		truth = true
    #     	default:
    #     		return
    #     	}
    #     	return truth, true
    #     }
    pass


# c:\go\src\text\template\funcs.go:724:6
def jsIsSpecial(r: int) -> bool:
    #     {
    #     	switch r {
    #     	case '\\', '\'', '"', '<', '>', '&', '=':
    #     		return true
    #     	}
    #     	return r < ' ' || utf8.RuneSelf <= r
    #     }
    pass


# c:\go\src\text\template\funcs.go:562:6
def le(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     
    #     	lessThan, err := lt(arg1, arg2)
    #     	if lessThan || err != nil {
    #     		return lessThan, err
    #     	}
    #     	return eq(arg1, arg2)
    #     }
    pass


# c:\go\src\text\template\funcs.go:296:6
def length(item: goext.reflect_Value) -> Tuple[int, 'goext.error']:
    #     {
    #     	item, isNil := indirect(item)
    #     	if isNil {
    #     		return 0, fmt.Errorf("len of nil pointer")
    #     	}
    #     	switch item.Kind() {
    #     	case reflect.Array, reflect.Chan, reflect.Map, reflect.Slice, reflect.String:
    #     		return item.Len(), nil
    #     	}
    #     	return 0, fmt.Errorf("len of type %!s(MISSING)", item.Type())
    #     }
    pass


# c:\go\src\text\template\funcs.go:520:6
def lt(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     	arg1 = indirectInterface(arg1)
    #     	k1, err := basicKind(arg1)
    #     	if err != nil {
    #     		return false, err
    #     	}
    #     	arg2 = indirectInterface(arg2)
    #     	k2, err := basicKind(arg2)
    #     	if err != nil {
    #     		return false, err
    #     	}
    #     	truth := false
    #     	if k1 != k2 {
    #     
    #     		switch {
    #     		case k1 == intKind && k2 == uintKind:
    #     			truth = arg1.Int() < 0 || uint64(arg1.Int()) < arg2.Uint()
    #     		case k1 == uintKind && k2 == intKind:
    #     			truth = arg2.Int() >= 0 && arg1.Uint() < uint64(arg2.Int())
    #     		default:
    #     			return false, errBadComparison
    #     		}
    #     	} else {
    #     		switch k1 {
    #     		case boolKind, complexKind:
    #     			return false, errBadComparisonType
    #     		case floatKind:
    #     			truth = arg1.Float() < arg2.Float()
    #     		case intKind:
    #     			truth = arg1.Int() < arg2.Int()
    #     		case stringKind:
    #     			truth = arg1.String() < arg2.String()
    #     		case uintKind:
    #     			truth = arg1.Uint() < arg2.Uint()
    #     		default:
    #     			panic("invalid kind")
    #     		}
    #     	}
    #     	return truth, nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:513:6
def ne(arg1: goext.reflect_Value, arg2: goext.reflect_Value) -> Tuple[bool, 'goext.error']:
    #     {
    #     
    #     	equal, err := eq(arg1, arg2)
    #     	return !equal, err
    #     }
    pass


# c:\go\src\text\template\funcs.go:410:6
def not_(arg: goext.reflect_Value) -> bool:
    #     {
    #     	return !truth(arg)
    #     }
    pass


# c:\go\src\text\template\funcs.go:396:6
def or_(arg0: goext.reflect_Value, *args: goext.reflect_Value) -> goext.reflect_Value:
    #     {
    #     	if truth(arg0) {
    #     		return arg0
    #     	}
    #     	for i := range args {
    #     		arg0 = args[i]
    #     		if truth(arg0) {
    #     			break
    #     		}
    #     	}
    #     	return arg0
    #     }
    pass


# c:\go\src\text\template\helper.go:59:6
def parseFiles(t: Optional['Template'], *filenames: str) -> Tuple[Optional['Template'], 'goext.error']:
    #     {
    #     	if len(filenames) == 0 {
    #     
    #     		return nil, fmt.Errorf("template: no files named in call to ParseFiles")
    #     	}
    #     	for _, filename := range filenames {
    #     		b, err := ioutil.ReadFile(filename)
    #     		if err != nil {
    #     			return nil, err
    #     		}
    #     		s := string(b)
    #     		name := filepath.Base(filename)
    #     		// First template becomes return value if not already defined,
    #     		// and we use that one for subsequent New calls to associate
    #     		// all the templates together. Also, if this file has the same name
    #     		// as t, this file becomes the contents of t, so
    #     		//  t, err := New(name).Funcs(xxx).ParseFiles(name)
    #     		// works. Otherwise we create a new template associated with t.
    #     		var tmpl *Template
    #     		if t == nil {
    #     			t = New(name)
    #     		}
    #     		if name == t.Name() {
    #     			tmpl = t
    #     		} else {
    #     			tmpl = t.New(name)
    #     		}
    #     		_, err = tmpl.Parse(s)
    #     		if err != nil {
    #     			return nil, err
    #     		}
    #     	}
    #     	return t, nil
    #     }
    pass


# c:\go\src\text\template\helper.go:121:6
def parseGlob(t: Optional['Template'], pattern: str) -> Tuple[Optional['Template'], 'goext.error']:
    #     {
    #     	filenames, err := filepath.Glob(pattern)
    #     	if err != nil {
    #     		return nil, err
    #     	}
    #     	if len(filenames) == 0 {
    #     		return nil, fmt.Errorf("template: pattern matches no files: %!q(MISSING)", pattern)
    #     	}
    #     	return parseFiles(t, filenames...)
    #     }
    pass


# c:\go\src\text\template\funcs.go:155:6
def prepareArg(value: goext.reflect_Value, argType: goext.reflect_Type) -> Tuple[goext.reflect_Value, 'goext.error']:
    #     {
    #     	if !value.IsValid() {
    #     		if !canBeNil(argType) {
    #     			return reflect.Value{}, fmt.Errorf("value is nil; should be of type %!s(MISSING)", argType)
    #     		}
    #     		value = reflect.Zero(argType)
    #     	}
    #     	if value.Type().AssignableTo(argType) {
    #     		return value, nil
    #     	}
    #     	if intLike(value.Kind()) && intLike(argType.Kind()) && value.Type().ConvertibleTo(argType) {
    #     		value = value.Convert(argType)
    #     		return value, nil
    #     	}
    #     	return reflect.Value{}, fmt.Errorf("value has type %!s(MISSING); should be %!s(MISSING)", value.Type(), argType)
    #     }
    pass


# c:\go\src\text\template\exec.go:968:6
def printableValue(v: goext.reflect_Value) -> Tuple[Any, bool]:
    #     {
    #     	if v.Kind() == reflect.Ptr {
    #     		v, _ = indirect(v)
    #     	}
    #     	if !v.IsValid() {
    #     		return "<no value>", true
    #     	}
    #     
    #     	if !v.Type().Implements(errorType) && !v.Type().Implements(fmtStringerType) {
    #     		if v.CanAddr() && (reflect.PtrTo(v.Type()).Implements(errorType) || reflect.PtrTo(v.Type()).Implements(fmtStringerType)) {
    #     			v = v.Addr()
    #     		} else {
    #     			switch v.Kind() {
    #     			case reflect.Chan, reflect.Func:
    #     				return nil, false
    #     			}
    #     		}
    #     	}
    #     	return v.Interface(), true
    #     }
    pass


# c:\go\src\text\template\funcs.go:355:6
def safeCall(fun: goext.reflect_Value, args: List[goext.reflect_Value]) -> Tuple[goext.reflect_Value, 'goext.error']:
    #     {
    #     	defer func() {
    #     		if r := recover(); r != nil {
    #     			if e, ok := r.(error); ok {
    #     				err = e
    #     			} else {
    #     				err = fmt.Errorf("%!v(MISSING)", r)
    #     			}
    #     		}
    #     	}()
    #     	ret := fun.Call(args)
    #     	if len(ret) == 2 && !ret[1].IsNil() {
    #     		return ret[0], ret[1].Interface().(error)
    #     	}
    #     	return ret[0], nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:250:6
def slice(item: goext.reflect_Value, *indexes: goext.reflect_Value) -> Tuple[goext.reflect_Value, 'goext.error']:
    #     {
    #     	item = indirectInterface(item)
    #     	if !item.IsValid() {
    #     		return reflect.Value{}, fmt.Errorf("slice of untyped nil")
    #     	}
    #     	if len(indexes) > 3 {
    #     		return reflect.Value{}, fmt.Errorf("too many slice indexes: %!d(MISSING)", len(indexes))
    #     	}
    #     	var cap int
    #     	switch item.Kind() {
    #     	case reflect.String:
    #     		if len(indexes) == 3 {
    #     			return reflect.Value{}, fmt.Errorf("cannot 3-index slice a string")
    #     		}
    #     		cap = item.Len()
    #     	case reflect.Array, reflect.Slice:
    #     		cap = item.Cap()
    #     	default:
    #     		return reflect.Value{}, fmt.Errorf("can't slice item of type %!s(MISSING)", item.Type())
    #     	}
    #     
    #     	idx := [3]int{0, item.Len()}
    #     	for i, index := range indexes {
    #     		x, err := indexArg(index, cap)
    #     		if err != nil {
    #     			return reflect.Value{}, err
    #     		}
    #     		idx[i] = x
    #     	}
    #     
    #     	if idx[0] > idx[1] {
    #     		return reflect.Value{}, fmt.Errorf("invalid slice index: %!d(MISSING) > %!d(MISSING)", idx[0], idx[1])
    #     	}
    #     	if len(indexes) < 3 {
    #     		return item.Slice(idx[0], idx[1]), nil
    #     	}
    #     
    #     	if idx[1] > idx[2] {
    #     		return reflect.Value{}, fmt.Errorf("invalid slice index: %!d(MISSING) > %!d(MISSING)", idx[1], idx[2])
    #     	}
    #     	return item.Slice3(idx[0], idx[1], idx[2]), nil
    #     }
    pass


# c:\go\src\text\template\funcs.go:374:6
def truth(arg: goext.reflect_Value) -> bool:
    #     {
    #     	t, _ := isTrue(indirectInterface(arg))
    #     	return t
    #     }
    pass

