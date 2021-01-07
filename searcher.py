from ranker import Ranker
import utils
import os
from math import sqrt, log10
import string
import wordnet as wn
import spelling_correction as sp
from cosine_similatiry import CosineSimCalculator
from bm25 import BM25
import operator
import numpy as np


class Searcher:

    def __init__(self, parser, indexer, model=None, wordnet=False, correction=False):
        self._parser = parser
        self.indexer = indexer
        self._ranker = Ranker()
        self._model = model
        # method toggles
        self.wordnet_toggle = wordnet
        self.spelling_corr_toggle = correction

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implmentation as you see fit.
    def search(self, query, k=None):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relevant
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)

        relevant_docs = self.relevant_docs_from_posting(query_as_list)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs, k)
        # print(np.percentile(list(dict(ranked_doc_ids).values()), 10))
        # print(max(dict(ranked_doc_ids).items(), key=operator.itemgetter(1)))
        return n_relevant, ranked_doc_ids

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """

        # -------------------- methods ------------------------------------
        if self.wordnet_toggle:
            query = wn.expand_query(query, self._parser.stop_words)
        if self.spelling_corr_toggle:
            query = sp.correct_spelling(query)
        # -----------------------------------------------------------------
        N = self._parser.num_of_docs
        total_len = self._parser.total_doc_length
        inverted_idx = self.indexer.inverted_idx
        # cosine_sim = CosineSimCalculator(inverted_idx, query, N)
        # cosine_sim.create_wiq_dict()
        # relevant_docs = cosine_sim.calc_similarity()

        bm25 = BM25(inverted_idx, query, N, total_len)
        bm25.create_wiq_dict()
        relevant_docs = bm25.calc_bm25()

        for doc, socre in relevant_docs.items():
            if doc in self._parser.retweet_dict:
                relevant_docs[doc] += self._parser.retweet_dict[doc]

        return relevant_docs

