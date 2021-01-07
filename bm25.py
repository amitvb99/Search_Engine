import numpy as np
from math import log10, sqrt

class BM25:

    def __init__(self, index, query, total_doc_num, total_doc_len, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.inverted_idx = index
        self.query = query
        self.wiq_dict = {}
        self.doc_scores = {}
        self.avdl = total_doc_len / total_doc_num
        self.N = total_doc_num

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

    def calc_bm25(self):
        for term in self.query:
            try:  # an example of checks that you have to do
                (df, sum_fij), tweet_dict = self.inverted_idx[term]
                idf = log10(self.N / df)
                for doc_id, (max_tf, doc_len, unique, fij, tf) in tweet_dict.items():
                    wij = idf * tf
                    nom = self.wiq_dict[term] * (self.k1 + 1) * wij
                    den = wij + self.k1 * (1 - self.b + self.b * (doc_len / self.avdl))
                    if doc_id not in self.doc_scores:
                        self.doc_scores[doc_id] = nom / den
                    else:
                        self.doc_scores[doc_id] += nom / den
            except:
                continue

        return self.doc_scores

            

