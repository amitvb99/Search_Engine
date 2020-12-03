import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()

    def read_corpus(self):
        """
        This function is reading the corpus directory.
        :return: a list of dataframes with all tweets in the corpus.
        """
        docs = []
        for root, dirs, files in os.walk(self.corpus_path):
            for file in files:
                # path = root + os.sep + file
                # if path.endswith('.parquet'):
                if file.endswith('.parquet'):
                    docs += self.read_file(file)
        return docs
