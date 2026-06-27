from common import App, Node, Var
from egraph import EGraph


class TestHashCons:
    def test_hash_cons_basic(self) -> None:
        egraph = EGraph()

        a = Node("a")
        a_id1 = egraph.add(a)
        a_id2 = egraph.add(a)

        assert a_id1 == a_id2

        b = Node("b")
        b_id = egraph.add(b)

        assert a_id1 != b_id

    def test_congruence_closure(self) -> None:
        egraph = EGraph()

        a = Node("a")
        b = Node("b")

        a_id = egraph.add(a)
        b_id = egraph.add(b)

        f_a = Node("f", (a_id,))
        f_b = Node("f", (b_id,))

        f_a_id = egraph.add(f_a)
        f_b_id = egraph.add(f_b)

        egraph.union(a_id, b_id)
        egraph.rebuild()

        assert egraph.are_equiv(f_a_id, f_b_id)

    def test_instantiate(self) -> None:
        egraph = EGraph()

        a = Node("a")
        a_id = egraph.add(a)

        pattern_var = Var("?x")

        assert egraph.instantiate(pattern_var, {pattern_var: a_id}) == a_id


class TestFullEgraph:
    def test_small(self) -> None:
        egraph = EGraph()
        assoc = (App("+", (Var("?a"), Var("?b"))), App("+", (Var("?b"), Var("?a"))))

        rewrites = (assoc,)

        a = egraph.add(Node("a"))
        b = egraph.add(Node("b"))
        egraph.add(Node("+", (a, b)))
        egraph.rewrites = rewrites
        egraph.saturate()

        assert len(set(egraph.hashcons.values())) == 3
        assert len(set(egraph.hashcons.keys())) == 4

    def test_full(self) -> None:
        assoc = (
            App("+", ((App("+", (Var("?a"), Var("?b")))), Var("?c"))),
            App("+", (Var("?a"), (App("+", (Var("?b"), Var("?c")))))),
        )

        commut = (App("+", (Var("?a"), Var("?b"))), App("+", (Var("?b"), Var("?a"))))

        rewrites = (assoc, commut)

        egraph = EGraph(rewrites=rewrites)

        a = egraph.add(Node("a"))
        b = egraph.add(Node("b"))
        c = egraph.add(Node("c"))
        d = egraph.add(Node("d"))
        e = egraph.add(Node("e"))
        f = egraph.add(Node("f"))
        g = egraph.add(Node("g"))

        egraph.add(
            Node(
                "+",
                (
                    egraph.add(
                        Node(
                            "+",
                            (
                                egraph.add(
                                    Node(
                                        "+",
                                        (
                                            egraph.add(
                                                Node(
                                                    "+",
                                                    (
                                                        egraph.add(
                                                            Node(
                                                                "+",
                                                                (
                                                                    egraph.add(Node("+", (a, b))),
                                                                    c,
                                                                ),
                                                            )
                                                        ),
                                                        d,
                                                    ),
                                                )
                                            ),
                                            e,
                                        ),
                                    )
                                ),
                                f,
                            ),
                        )
                    ),
                    g,
                ),
            )
        )
        egraph.rewrites = rewrites
        egraph.saturate()

        assert len(set(egraph.hashcons.values())) == 127
        assert len(set(egraph.hashcons.keys())) == 1939
