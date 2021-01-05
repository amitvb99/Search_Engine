from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import os
import pandas as pd
import csv
import time


def run_engine(config, indexer):
    """
    :return:
    """
    number_of_documents = 0

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(config)

    doc = r.read_file('benchmark_data_train.snappy.parquet')
    for document in doc:
        parsed_document = p.parse_doc(document)
        indexer.add_new_doc(parsed_document)
        number_of_documents += 1
    capital_letters = p.caps_dict
    indexer.change_inverted_by_caps(capital_letters)
    indexer.save_index('idx_bench')


def search_and_rank_query(query, indexer, parser, k=None):
    searcher = Searcher(parser=parser, indexer=indexer)
    n_relevant, ranked_doc_ids = searcher.search(query, k)
    return n_relevant, ranked_doc_ids


def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    config = ConfigClass(corpus_path, output_path, stemming)
    indexer = Indexer(config)
    run_engine(config, indexer)
    if isinstance(queries, list):
        queries_list = queries
    else:
        # queries_list = []
        # queries_file = open(queries, encoding='utf8')
        # lines = [l for l in queries_file.readlines() if l is not '\n']
        # for line in lines:
        #     queries_list.append(line[line.index('.') + 1: -1])
        queries_df = pd.read_table(queries)
        queries_list = list(queries_df['information_need'].values)

    lst_to_csv = [['Query_num', 'Tweet_id', 'Score']]
    for num, query in enumerate(queries_list):
        stime = time.time()
        print(f'query {num+1}')
        n_relevant, ranked_doc_ids = search_and_rank_query(query=query, parser=Parse(config), indexer=indexer, k=num_docs_to_retrieve)
        for tweet_id, score in ranked_doc_ids:
            print(f'Tweet id: {tweet_id}, Score: {score}')
            lst_to_csv.append([num+1, tweet_id, score])
        print(f'time for query no. {num+1} is {time.time() - stime}')

    with open('data\\analysis_data.csv', 'w', newline='') as file:
        file.truncate()
        writer = csv.writer(file)
        writer.writerows(lst_to_csv)
