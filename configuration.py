import os


class ConfigClass:
    def __init__(self, corpus_path='',
                 output_path='C:\\Users\\amitv\\University\\Information retrieval\\output', stem=False):
        self._download_model = False
        self._model_url = None
        self.corpusPath = corpus_path
        self.savedFileMainFolder = output_path
        self.google_news_vectors_negative300_path = '../../../../GoogleNews-vectors-negative300.bin'
        self.glove_twitter_27B_25d_path = '../../../../glove.twitter.27B.25d.txt'

        self.saveFilesWithStem = os.path.join(self.savedFileMainFolder, "WithStem")
        if not os.path.exists(self.saveFilesWithStem):
            os.mkdir(self.saveFilesWithStem)
        if not os.path.exists(self.saveFilesWithStem + os.sep + 'Posting'):
            os.mkdir(self.saveFilesWithStem + os.sep + 'Posting')
        if not os.path.exists(self.saveFilesWithStem + os.sep + 'Inverted_idx'):
            os.mkdir(self.saveFilesWithStem + os.sep + 'Inverted_idx')
        if not os.path.exists(self.saveFilesWithStem + os.sep + 'CapitalLetters'):
            os.mkdir(self.saveFilesWithStem + os.sep + 'CapitalLetters')

        self.saveFilesWithoutStem = os.path.join(self.savedFileMainFolder, "WithoutStem")
        if not os.path.exists(self.saveFilesWithoutStem):
            os.mkdir(self.saveFilesWithoutStem)
        if not os.path.exists(self.saveFilesWithoutStem + os.sep + 'Posting'):
            os.mkdir(self.saveFilesWithoutStem + os.sep + 'Posting')
        if not os.path.exists(self.saveFilesWithoutStem + os.sep + 'Inverted_idx'):
            os.mkdir(self.saveFilesWithoutStem + os.sep + 'Inverted_idx')
        if not os.path.exists(self.saveFilesWithoutStem + os.sep + 'CapitalLetters'):
            os.mkdir(self.saveFilesWithoutStem + os.sep + 'CapitalLetters')
        self.toStem = stem

        # print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
    
    def get_model_url(self):
        return self._model_url

    def get_download_model(self):
        return self._download_model
