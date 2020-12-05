from parser_module import Parse
from ranker import Ranker
import utils
from nltk.corpus import wordnet as wn
import os
from math import sqrt, log10
import string


class Searcher:

    def __init__(self, inverted_index, config):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(config)
        self.ranker = Ranker()
        self.inverted_index = inverted_index

    def relevant_docs_from_posting(self, query, relpath):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param relpath: path to folder - stemming\no stemming:
        :param query: query
        :return: dictionary of relevant documents.
        """

        # -------------------- wordnet ------------------------------------
        wordnet_expantion = set()
        for term in query:
            synsets = wn.synsets(term)
            if len(synsets) != 0:
                for l in synsets[0].lemma_names():
                    wordnet_expantion |= set(l.split('_'))
                wordnet_expantion -= {term}
                hypernyms = synsets[0].hypernyms()
                if len(hypernyms) != 0:
                    for l in hypernyms[0].lemma_names():
                        wordnet_expantion |= set(l.split('_'))

        query += [term for term in wordnet_expantion if term not in self.parser.stop_words]
        # -----------------------------------------------------------------
        files_to_load = set()
        N = 10000000  # TODO: change this back
        caps_filename = os.path.join(relpath, *['CapitalLetters', 'cl'])
        caps = utils.load_obj(caps_filename)
        wiq_dict = dict()
        for term in query:
            if term.lower() in caps:
                if caps[term.lower()]:
                    query[query.index(term)] = term.lower()
                    term = term.lower()
                else:
                    query[query.index(term)] = term.upper()
                    term = term.upper()
            if term[0].lower() in string.ascii_lowercase:
                files_to_load = files_to_load | {term[0].lower()}
            else:
                files_to_load = files_to_load | {'special'}
            if term in wiq_dict:
                wiq_dict[term] += 1
            else:
                wiq_dict[term] = 1
        relevant_docs = dict()
        for letter in files_to_load:
            posting_filename = os.path.join(relpath, letter)
            posting = utils.load_obj(posting_filename)
            terms = [term for term in query if term[0].lower() == letter]
            for term in terms:
                try:  # an example of checks that you have to do
                    posting_doc = posting[term]
                    df, sum_fij = self.inverted_index[term]
                    idf = log10(N / df)
                    tf_q = query.count(term)
                    for (id, max_tf, unique, fij, tf) in posting_doc:
                        doc = id
                        wij = idf * tf
                        if doc not in relevant_docs.keys():
                            relevant_docs[doc] = (wij * tf_q, wiq_dict[term])
                        else:
                            sum_wij, sum_wij_squared = relevant_docs[doc]
                            relevant_docs[doc] = (sum_wij + wij * tf_q, sum_wij_squared + wiq_dict[term])
                except:
                    continue
            posting = dict()
        for doc in relevant_docs:
            sum_wij_wiq, sum_wij_squared = relevant_docs[doc]
            relevant_docs[doc] = sum_wij_wiq / sqrt(sum_wij_squared * sum([wiq**2 for wiq in wiq_dict.values()]))

        return relevant_docs

