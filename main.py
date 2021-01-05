import search_engine
# import search_engine_best

if __name__ == '__main__':
    corpus_path = 'C:\\Users\\amitv\\University\\Information retrieval\\corpus'
    output_path = 'C:\\Users\\amitv\\University\\Information retrieval\\output'
    stemming = False
    queries = 'C:\\Users\\amitv\\University\\Information retrieval\\Search_Engine\\data\\queries_train.tsv'
    num_docs_to_retrieve = 100
    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
    # srarch_engine_best.main()
