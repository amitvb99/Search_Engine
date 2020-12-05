import os


class ConfigClass:
    def __init__(self, output_path, stem=False):
        self.corpusPath = r'C:\Users\amitv\University\Information retrieval\corpus'
        self.savedFileMainFolder = output_path

        self.saveFilesWithStem = os.path.join(self.savedFileMainFolder, "WithStem")
        if not os.path.exists(self.saveFilesWithStem):
            os.mkdir(self.saveFilesWithStem)
        if not os.path.exists(self.saveFilesWithStem + '\\Posting'):
            os.mkdir(self.saveFilesWithStem + '\\Posting')
        if not os.path.exists(self.saveFilesWithStem + '\\Inverted_idx'):
            os.mkdir(self.saveFilesWithStem + '\\Inverted_idx')
        if not os.path.exists(self.saveFilesWithStem + '\\CapitalLetters'):
            os.mkdir(self.saveFilesWithStem + '\\CapitalLetters')

        self.saveFilesWithoutStem = os.path.join(self.savedFileMainFolder, "WithoutStem")
        if not os.path.exists(self.saveFilesWithoutStem):
            os.mkdir(self.saveFilesWithoutStem)
        if not os.path.exists(self.saveFilesWithoutStem + '\\Posting'):
            os.mkdir(self.saveFilesWithoutStem + '\\Posting')
        if not os.path.exists(self.saveFilesWithoutStem + '\\Inverted_idx'):
            os.mkdir(self.saveFilesWithoutStem + '\\Inverted_idx')
        if not os.path.exists(self.saveFilesWithoutStem + '\\CapitalLetters'):
            os.mkdir(self.saveFilesWithoutStem + '\\CapitalLetters')
        self.toStem = stem

        # print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
