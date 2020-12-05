import string
import os
import utils


class Indexer:

    def __init__(self, config, group_size=1):
        self.inverted_idx = {}
        self.config = config
        self.write_counter = 0
        self.group_size = group_size
        self.filename_counter = 0
        keys = set(string.ascii_lowercase) | {'special'}
        vals = [dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict()]
        self.letters_dict = dict(zip(keys, vals))

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
                    self.inverted_idx[term] = (1, fij)
                else:
                    df, sum_fij = self.inverted_idx[term]
                    self.inverted_idx[term] = (df+1, sum_fij + fij)

                if term[0].lower() in self.letters_dict.keys():
                    if term.lower() not in self.letters_dict[term[0].lower()]:
                        letter = self.letters_dict[term[0].lower()]
                        letter[term.lower()] = [(document.tweet_id, document.max_tf, document.unique_terms, fij, tf)]
                    else:
                        new_tup = (document.tweet_id, document.max_tf, document.unique_terms, fij, tf)
                        letter = self.letters_dict[term[0].lower()]
                        letter[term.lower()].append(new_tup)
                else:
                    if term not in self.letters_dict['special']:
                        letter = self.letters_dict['special']
                        letter[term] = [(document.tweet_id, document.max_tf, document.unique_terms, fij, tf)]
                    else:
                        new_tup = (document.tweet_id, document.max_tf, document.unique_terms, fij, tf)
                        letter = self.letters_dict['special']
                        letter[term].append(new_tup)
            except:
                continue

        self.write_counter += 1

        if self.write_counter == self.group_size:
            # write posting file
            self.write_files()
            self.write_counter = 0
            self.filename_counter += 1

    def write_files(self):
        if self.config.toStem:
            relpath = self.config.saveFilesWithStem
        else:
            relpath = self.config.saveFilesWithoutStem

        for letter in self.letters_dict.keys():
            filename = os.path.join(relpath, *['Posting', f'{letter + str(self.filename_counter)}'])
            utils.save_obj(self.letters_dict[letter], filename)
        # reset letters_dict
        keys = set(string.ascii_lowercase) | {'special'}
        vals = [dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict(), dict(), dict(), dict(),
                dict(), dict()]
        self.letters_dict = dict(zip(keys, vals))

        filename = os.path.join(relpath, *['Inverted_idx', f'inverted{str(self.filename_counter)}'])
        utils.save_obj(self.inverted_idx, filename)
        # reset inverted_idx
        self.inverted_idx = {}
