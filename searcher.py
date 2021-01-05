from ranker import Ranker
import utils
import os
from math import sqrt, log10
import string
import wordnet as wn
import spelling_correction as sp
from cosine_similatiry import CosineSimCalculator


class Searcher:

    def __init__(self, parser, indexer, model=None, n_docs=100000):
        self._parser = parser
        self.indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self.n_docs = n_docs
        # method toggles
        self.wordnet_toggle = True
        self.spelling_corr_toggle = True

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
        N = self.n_docs
        inverted_idx = self.indexer.inverted_idx
        cosine_sim = CosineSimCalculator(inverted_idx, query, N)
        cosine_sim.create_wiq_dict()
        relevant_docs = cosine_sim.calc_similarity()

        return relevant_docs

