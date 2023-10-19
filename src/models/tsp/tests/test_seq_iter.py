from src.graph.complete_graph import CompleteGraph
from src.tsp.seq_iter import SeqIter


class TestTspSeqIter:
    def test_should_create(self):
        assert SeqIter([], 0, None)

    def test_should_iterate(self):
        assert [2] == list(
            SeqIter(
                unvisited=[1, 2],
                current_vertex=1,
                graph=CompleteGraph(5),
            )
        )
