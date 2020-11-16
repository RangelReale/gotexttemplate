package main

import (
	"go/types"
	"strings"
)

func labels(lbl []*types.Const) string {
	var sb strings.Builder
	sb.WriteString(lbl[0].Name())
	sb.WriteString(" = ")

	if len(lbl) > 1 {
		sb.WriteString(lbl[1].Name())
	} else {
		sb.WriteString(lbl[0].Val().String())
	}

	return sb.String()
}
