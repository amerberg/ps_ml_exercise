from app import similarity
import pandas as pd
import pytest


class TestSim(object):
    @property
    def scores(self):
        d = 10
        return pd.DataFrame([[(i + j) / (2 * d) for i in range(d)] for j in range(d)])

    def test_most_similar(self):
        assert similarity.most_similar(self.scores, 5, 6).score.iloc[-1] == 0.40

    def test_most_similar_index(self):
        with pytest.raises(KeyError):
            result = similarity.most_similar(self.scores, 10, 100)
