from typing import List


class StringsBuilder:
    sb: List[str]

    def __init__(self):
        self.sb = []

    def WriteString(self, s: str) -> None:
        self.sb.append(s)

    def String(self) -> str:
        return ''.join(self.sb)
