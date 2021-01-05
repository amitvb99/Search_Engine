from math import log10, sqrt


class CosineSimCalculator:
    def __init__(self, index, query, corpus_size):
        self.inverted_idx = index
        self.query = query
        self.doc_scores = {}
        self.wiq_dict = {}
        self.N = corpus_size

    def create_wiq_dict(self):
        for term in self.query:
            if term.lower() not in self.inverted_idx.keys() and term.upper() not in self.inverted_idx.keys():
                continue
            if term.lower() in self.inverted_idx.keys():
                self.query[self.query.index(term)] = term.lower()
                if term in self.wiq_dict:
                    self.wiq_dict[term.lower()] += 1
                else:
                    self.wiq_dict[term.lower()] = 1
            elif term.upper() in self.inverted_idx.keys():
                self.query[self.query.index(term)] = term.upper()
                if term in self.wiq_dict:
                    self.wiq_dict[term.upper()] += 1
                else:
                    self.wiq_dict[term.upper()] = 1

    def calc_similarity(self):
        for term in self.query:
            try:  # an example of checks that you have to do
                (df, sum_fij), tweet_dict = self.inverted_idx[term]
                idf = log10(self.N / df)
                tf_q = self.query.count(term)
                for id, (max_tf, unique, fij, tf) in tweet_dict.items():
                    doc = id
                    wij = idf * tf
                    if doc not in self.doc_scores:
                        self.doc_scores[doc] = (wij * tf_q, self.wiq_dict[term])
                    else:
                        sum_wij, sum_wij_squared = self.doc_scores[doc]
                        self.doc_scores[doc] = (sum_wij + wij * tf_q, sum_wij_squared + self.wiq_dict[term])
            except:
                continue

        for doc in self.doc_scores:
            sum_wij_wiq, sum_wij_squared = self.doc_scores[doc]
            self.doc_scores[doc] = sum_wij_wiq / sqrt(sum_wij_squared * sum([wiq**2 for wiq in self.wiq_dict.values()]))

        return self.doc_scores
