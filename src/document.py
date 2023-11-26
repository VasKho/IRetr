import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

class Document:
    def __init__(self, title, file):
        self.title: str = title[:-4]
        self.tf_idf = []
        self.words_num = 0
        self.text = file.read()
        self.text = self.__process()
        self.url = ""

    def __process(self) -> list[str]:
        """Remove stop words from text and stemm words."""
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        normalized = []
        text = self.text.lower()
        text = re.sub(r'\b[0-9]+\b', '', text)
        tokens = word_tokenize(text)
        text_list = " ".join([stemmer.stem(tok) for tok in tokens if not tok in stop_words and tok.isalnum()])
        self.words_num = len(text_list)
        return text_list

    def set_url(self, url):
        self.url = url

    def get_url(self) -> str:
        return self.url
