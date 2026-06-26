from dataclasses import dataclass

type Id = int

@dataclass(frozen=True)
class Pattern:
    pass

type Rewrite = tuple[Pattern, Pattern]

@dataclass(frozen=True)
class Var(Pattern):
    name: str

@dataclass(frozen=True)
class App(Pattern):
    op_symbol: str
    children: tuple[Pattern, ...]

@dataclass(frozen=True)
class Node:
    op_name: str
    children: tuple[Id, ...] = ()
