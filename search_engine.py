from datetime import datetime

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import time
import os
import string


def run_engine(config=ConfigClass()):
    """

    :return:
    """
    number_of_documents = 0

    r = ReadFile(corpus_path=config.get__corpusPath())

    # documents_list = list(r.read_file('covid19_07-10.snappy.parquet'))
    # saving_number is the number of documents we read together and then save all of them to the disk
    saving_number = 500000
    indexer = Indexer(config, saving_number)
    '''measure parsing time'''
    start_time = time.time()
    p = Parse(config, saving_number)

    doc = []
    for root, dirs, files in os.walk(r.corpus_path):
        for file in files:
            if file.endswith('.parquet'):
                doc = r.read_file(file)
                for document in doc:
                    # parse the document and index it
                    parsed_document = p.parse_doc(document)
                    indexer.add_new_doc(parsed_document)
                    number_of_documents += 1
                    # if number_of_documents == 3000000:
                    #     print('got here')
                doc = []

    print('Finished parsing and indexing. Starting to export files')
    end_time = time.time()
    print(f'Total time : {end_time - start_time} seconds, parsed {number_of_documents} documents')


def merge_files(relpath):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'started merging caps at: {current_time}')
    merged_caps = merge_caps(relpath)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'started merging inverted at: {current_time}')
    merge_inverted_idx(relpath, merged_caps)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'started merging posting at: {current_time}')
    merge_posting(relpath, merged_caps)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'finished merging at: {current_time}')


def load_index(relpath=''):
    print('Load inverted index')
    filename = os.path.join(relpath, *['Inverted_idx', 'inverted'])
    inverted_index = utils.load_obj(filename)
    return inverted_index


def merge_caps(relpath):
    merge_dict = dict()
    path = os.path.join(relpath, 'CapitalLetters')
    for file in os.listdir(path):
        filename = os.path.join(relpath, *['CapitalLetters', file])
        temp_dict = utils.load_obj(filename.split('.')[0])  # get the file name, but not the '.pkl' postfix
        for term in temp_dict:
            if term not in merge_dict.keys():
                merge_dict[term] = temp_dict[term]
            else:
                merge_dict[term] = merge_dict[term] or temp_dict[term]
        utils.delete_obj(filename)
        temp_dict = dict()
    filename = os.path.join(relpath, *['CapitalLetters', 'cl'])
    utils.save_obj(merge_dict, filename)
    return merge_dict


def merge_inverted_idx(relpath, merged_caps):
    merge_dict = dict()
    path = os.path.join(relpath, 'Inverted_idx')
    for file in os.listdir(path):
        filename = os.path.join(relpath, *['Inverted_idx', file])
        temp_dict = utils.load_obj(filename.split('.')[0])
        for term in temp_dict:
            if term.lower() in merged_caps:
                if merged_caps[term.lower()]:
                    if term.lower() in merge_dict:
                        df, sum_fij = merge_dict[term.lower()]
                        merge_dict[term.lower()] = (df + temp_dict[term][0], sum_fij + temp_dict[term][1])
                    else:
                        merge_dict[term.lower()] = temp_dict[term]
                else:
                    if term.upper() in merge_dict.keys():
                        df, sum_fij = merge_dict[term.upper()]
                        merge_dict[term.upper()] = (df + temp_dict[term][0], sum_fij + temp_dict[term][1])
                    else:
                        merge_dict[term.upper()] = temp_dict[term]
            else:
                if term not in merge_dict.keys():
                    merge_dict[term] = temp_dict[term]
                else:
                    df, sum_fij = merge_dict[term]
                    merge_dict[term] = (df + temp_dict[term][0], sum_fij + temp_dict[term][1])
        utils.delete_obj(filename)
        temp_dict = dict()
    filename = os.path.join(relpath, *['Inverted_idx', 'inverted'])
    utils.save_obj(merge_dict, filename)
    merge_dict = dict()


def merge_posting(relpath, merged_caps):
    merge_dict = dict()
    path = os.path.join(relpath, 'Posting')
    for letter in [c for c in string.ascii_lowercase] + ['special']:
        letter_files = [file for file in os.listdir(path) if file[0] == letter]
        for file in letter_files:
            filename = os.path.join(relpath, *['Posting', file])
            temp_dict = utils.load_obj(filename.split('.')[0])
            for term in temp_dict:
                if term.lower() in merged_caps:
                    if merged_caps[term.lower()]:                           # lowercase
                        if term.lower() in merge_dict:
                            merge_dict[term.lower()] += temp_dict[term]
                        else:
                            merge_dict[term.lower()] = temp_dict[term]
                    else:                                                   # uppercase
                        if term.upper() in merge_dict:
                            merge_dict[term.upper()] += temp_dict[term]
                        else:
                            merge_dict[term.upper()] = temp_dict[term]
                else:
                    if term in merge_dict:
                        merge_dict[term] += temp_dict[term]
                    else:
                        merge_dict[term] = temp_dict[term]

            utils.delete_obj(filename)
            temp_dict = dict()
        for term in merge_dict:
            merge_dict[term].sort()
        filename = os.path.join(relpath, *['Posting', f'{letter}'])
        utils.save_obj(merge_dict, filename)
        merge_dict = dict()


# check the type of queries - list or text file
def search_and_rank_query(query, inverted_index, k, relpath):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, relpath)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    # input
    config = ConfigClass()
    # run_engine(config)
    if config.toStem:
        relpath = config.saveFilesWithStem
    else:
        relpath = config.saveFilesWithoutStem
    # merge_files(relpath)
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index(relpath)
    for doc_tuple in search_and_rank_query(query, inverted_index, k, relpath):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
