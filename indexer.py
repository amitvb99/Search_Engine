import string
import os
import utils


class Indexer:

    def __init__(self, config=None):
        self.inverted_idx = {}
        self.config = config

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        # TODO: deal with full path, the filename argument will not be the full path!
        if self.config is not None:
            if self.config.toStem:
                filename = os.path.join(self.config.saveFilesWithStem, fn)
            else:
                filename = os.path.join(self.config.saveFilesWithoutStem, fn)
        utils.save_obj(self.inverted_idx, filename)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implmentation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        # TODO: deal with full path, the filename argument will not be the full path!
        self.inverted_idx = utils.load_obj(fn)

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.inverted_idx

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def get_term_inverted_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.inverted_idx[term] if self.is_term_exist(term) else []

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                fij = document_dictionary[term]
                tf = fij / document.max_tf
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [(1, fij), {
                        document.tweet_id: (document.max_tf, document.unique_terms, fij, tf)
                    }]
                else:
                    (df, sum_fij), tweet_dict = self.inverted_idx[term]
                    tweet_dict[document.tweet_id] = (document.max_tf, document.unique_terms, fij, tf)
                    self.inverted_idx[term] = [(df+1, sum_fij + fij), tweet_dict]

            except:
                continue

    def change_inverted_by_caps(self, caps):
        to_add = {}
        for term in self.inverted_idx.keys():
            if term in caps.keys():
                if not caps[term]:
                    to_add[term.upper()] = self.inverted_idx[term]

        for term in to_add.keys():
            self.inverted_idx[term] = to_add[term]
            self.inverted_idx.pop(term.lower())
