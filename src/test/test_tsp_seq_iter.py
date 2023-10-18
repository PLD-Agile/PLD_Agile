from src.tsp.seq_iter import SeqIter

class TestTspSeqIter:
    def test_should_create(self):
        assert SeqIter([], 0, None)