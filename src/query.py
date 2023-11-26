import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

class Query:
    def __init__(self, text: str, vocabulary: dict[str, int]):
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        text = text.lower()
        text = re.sub(r'\b[0-9]+\b', '', text)
        tokens = word_tokenize(text)
        self.ind = {}
        self.active_indices = False
        self.strict_words = []
        for tok in tokens:
            stemmed_tok = stemmer.stem(tok)
            if not tok in stop_words and tok.isalnum() and stemmed_tok in vocabulary:
                if re.search(f'"{tok}"', text):
                    self.strict_words.append(stemmed_tok)
                if stemmed_tok in self.ind:
                    self.ind[stemmed_tok] += 1
                else:
                    self.ind.update({stemmed_tok: 1})
        self.size = len(self.ind)


    def tovector(self, feature_names: list[str], idf: list[float]) -> list[float]:
        vec = []
        self.active_indices = []
        for ind, feature in enumerate(feature_names):
            if feature in self.ind:
                self.active_indices.append(ind)
                vec.append((self.ind[feature]/self.size)*idf[ind])
            else:
                vec.append(0)
        return vec

    def get_active_indices(self, feature_names: list[str]) -> list[int]:
        if self.active_indices:
            return self.active_indices
        else:
            self.active_indices = []
            for ind, feature in enumerate(feature_names):
                if feature in self.ind:
                    self.active_indices.append(ind)
            return self.active_indices

    def get_strict_indices(self, feature_names: list[str]) -> list[int]:
        print(re.findall(r'"(\w*)"', self.text))
