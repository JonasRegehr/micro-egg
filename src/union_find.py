type Id = int

class UnionFind:
    parent: list[Id]

    def __init__(self) -> None:
        self.parent = []
    
    def __str__(self) -> str:
        return str(self.parent)

    """Adds a new node to the union-find in its own tree"""
    def makeset(self) -> Id:
        new_id = len(self.parent)
        self.parent.append(new_id)
        return new_id

    """Finds the root of the tree for a given id"""
    def find(self, id: Id) -> Id:
        if self.parent[id] == id:
            return id
        
        return self.find(self.parent[id])

    """Unions the two trees containing `a` and `b`"""
    def union(self, a: Id, b: Id) -> bool:
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False 
        
        self.parent[b] = a 
        return True 
    
    """Checks if `a` and `b` belong to the same tree"""
    def are_equal(self, a: Id, b: Id):
        return self.find(a) == self.find(b)