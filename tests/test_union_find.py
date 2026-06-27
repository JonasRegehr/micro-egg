from union_find import UnionFind


class TestUnionFind:
    def test_transitive(self) -> None:
        uf = UnionFind()
        a = uf.makeset()
        b = uf.makeset()
        c = uf.makeset()

        assert not uf.are_equal(a, b) and not uf.are_equal(b, c) and not uf.are_equal(a, c)

        assert uf.union(a, b)
        assert uf.union(b, c)
        assert uf.are_equal(a, c)

    def test_uf_basic(self) -> None:
        uf = UnionFind()
        a = uf.makeset()
        b = uf.makeset()
        c = uf.makeset()
        d = uf.makeset()

        assert uf.union(a, b)
        assert uf.are_equal(a, b)

        assert uf.union(c, d)
        assert uf.are_equal(c, d)

        assert uf.union(a, c)
        assert (
            uf.are_equal(a, b) and uf.are_equal(b, c) and uf.are_equal(c, d) and uf.are_equal(d, a)
        )

    def test_double_union_fails(self) -> None:
        uf = UnionFind()
        a = uf.makeset()
        b = uf.makeset()

        assert uf.union(a, b)
        assert not uf.union(a, b)
