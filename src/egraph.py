from common import App, Id, Node, Pattern, Rewrite, Var
from union_find import UnionFind


class EGraph:
    uf: UnionFind
    hashcons: dict[Node, Id]
    rewrites: tuple[Rewrite, ...]

    def __init__(self, rewrites: tuple[Rewrite, ...] = ()) -> None:
        self.uf = UnionFind()
        self.hashcons = {}
        self.rewrites = rewrites

    def canonicalize(self, node: Node) -> Node:
        """Returns `node` with each child id replaced by its canonical e-class id."""
        return Node(node.op_name, tuple(self.uf.find(child) for child in node.children))

    def are_equiv(self, a: Id, b: Id) -> bool:
        """Returns whether `a` and `b` identify the same e-class."""
        return self.uf.are_equal(a, b)

    def nodes_in_class(self, target_id: Id) -> list[Node]:
        """Returns e-nodes currently identified by `target_id`."""
        return [node for node, id in self.hashcons.items() if id == target_id]

    def add(self, node: Node) -> Id:
        """Adds `node` to the e-graph and returns the id of its e-class."""
        node = self.canonicalize(node)

        if node in self.hashcons:
            return self.hashcons[node]

        id = self.uf.makeset()
        self.hashcons[node] = id
        return id

    def union(self, a: Id, b: Id) -> bool:
        """Merges the e-classes identified by `a` and `b` and returns whether the e-graph changed."""
        return self.uf.union(a, b)

    def rebuild(self) -> None:
        """Canonicalizes stored e-nodes and merges e-classes whose e-nodes have become identical."""
        keep_going = True
        while keep_going:
            keep_going = False
            new_map: dict[Node, Id] = {}

            for old_node, old_id in self.hashcons.items():
                node = self.canonicalize(old_node)

                id = self.uf.find(old_id)

                # id2 = new_map[node] = id if node not in new_map else new_map[node]
                id2 = new_map.setdefault(node, id)

                if self.union(id, id2):
                    keep_going = True

            self.hashcons = new_map

    def instantiate(self, pattern: Pattern, subst: dict[Var, Id]) -> Id:
        """Replaces `pattern`'s variables with the e-classes from `subst` and adds resulting e-nodes 
        to the e-graph. Returns the id of the root e-class for `pattern`. 
        """
        match pattern:
            case Var():
                return subst[pattern]
            case App(op_symbol, children):
                inst = Node(op_symbol, tuple(self.instantiate(child, subst) for child in children))
                return self.add(inst)
            case _:
                raise TypeError(f"Invalid pattern: {pattern}")

    def ematch_rec(
        self,
        pattern: Pattern,
        id: Id,
        subst: dict[Var, Id],
    ) -> list[dict[Var, Id]]:
        """Returns all variable to e-class substitutions that match `pattern` at `eclass_id` plus
        all substitutions in `subst`."""
        match pattern:
            case Var():
                if pattern in subst:
                    return [subst] if subst[pattern] == id else []
                return [subst | {pattern: id}]
            case App():
                outputs = []
                for node in self.nodes_in_class(id):
                    if node.op_name != pattern.op_symbol or len(node.children) != len(pattern.children):
                        continue
                    todo = [subst]
                    for node_child, pattern_child in zip(node.children, pattern.children, strict=True):

                        # flattens [self.ematch_rec(pattern_child, node_child, sub) for sub in todo]
                        new_todo = [item for sub in todo for item in self.ematch_rec(pattern_child, node_child, sub)]
                        todo = new_todo
                    outputs += todo
                return outputs
            case _:
                raise TypeError(f"Invalid pattern: {pattern}")

    def ematch(self, pattern: Pattern, id: Id) -> list[dict[Var, Id]]:
        """Returns all variable to e-class substitutions that match `pattern` at `eclass_id`"""
        return self.ematch_rec(pattern, id, {})

    def rewrite(self, rewrites: tuple[Rewrite, ...]) -> None:
        """Applies each rewrite rule in `rewrites` once by matching its left-hand side in the 
        e-graph and unioning the match with the instantiated right-hand side.
        """
        matches = []
        for lhs, rhs in rewrites:
            for id in set(self.hashcons.values()):
                match = (rhs, id, self.ematch(lhs, id))
                matches.append(match)
        for rhs, id, substs in matches:
            for subst in substs:
                id2 = self.instantiate(rhs, subst)
                self.union(id, id2)

    def saturate(self) -> None:
        """Applies the rewrites in `self.rewrites` until fix point."""
        old_fp = (len(self.uf.parent), len(self.hashcons))
        while True:
            self.rewrite(self.rewrites)
            self.rebuild()
            fp = (len(self.uf.parent), len(self.hashcons))
            if old_fp == fp:
                break
            old_fp = fp
