import search_engine

if __name__ == '__main__':
    corpus_path = 'C:\\Users\\amitv\\University\\Information retrieval\\corpus'
    output_path = 'C:\\Users\\amitv\\University\\Information retrieval\\output'
    stemming = False
    queries = 'C:\\Users\\amitv\\University\\Information retrieval\\queries.txt'
    num_docs_to_retrieve = 2000
    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
