import os

class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\amitv\University\Information retrieval\corpus'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = os.path.realpath("WithStem")
        self.saveFilesWithoutStem = os.path.realpath("WithoutStem")
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
