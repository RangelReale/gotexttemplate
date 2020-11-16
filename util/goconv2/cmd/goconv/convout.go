package main

import (
	"github.com/jimmyfrasche/closed"
)

func (c *Conv) outputEnum(gf *GenFile, enum *closed.Enum) error {
	gf.Line("# %s", c.FileSet.Position(enum.Types()[0].Pos()))
	gf.Line("class %s(Enum):", enum.Types()[0].Name())
	gf.I()

	valueAmount := 0
	if !enum.NonZero && !ContainsLabeledZero(enum) {
		//ind()
		//fmt.Println("\t0")
	}
	for _, lbl := range enum.Labels {
		valueAmount++
		gf.StartLine()
		gf.Append(labels(lbl))
		gf.Append(c.ReturnLineComment(lbl[0]))
		gf.NL()
	}

	if valueAmount == 0 {
		gf.Line("pass")
	}
	gf.D()

	return nil
}
