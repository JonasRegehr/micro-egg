from common import Id


class UnionFind:
    parent: list[Id]

    def __init__(self) -> None:
        self.parent = []

    def __str__(self) -> str:
        return str(self.parent)

    def makeset(self) -> Id:
        """Adds a new node to the union-find in its own tree"""
        new_id = len(self.parent)
        self.parent.append(new_id)
        return new_id

    def find(self, id: Id) -> Id:
        """Finds the \"canonical\" id of the tree for a given `id`,
        i.e., the root of the tree containing `id`
        """
        while self.parent[id] != id:
            id = self.parent[id]

        return id

    def union(self, a: Id, b: Id) -> bool:
        """Unions the two trees containing `a` and `b`"""
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        self.parent[b] = a
        return True

    def are_equal(self, a: Id, b: Id) -> bool:
        """Checks if `a` and `b` belong to the same tree"""
        return self.find(a) == self.find(b)
