class BM25:

    def __init__(self, index, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.inverted_idx = index

    # def fit(self):