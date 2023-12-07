from os import listdir, path
from src.document import Document
from src.query import Query
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sklearn.feature_extraction.text import TfidfVectorizer

class Index:
    def __init__(self, name: str, data_dir: str):
        self.data_dir = data_dir
        self.vectorizer = TfidfVectorizer()
        self.documents = list()
        self.vec_dim = 0

        self.__load_documents()
        self.__init_collection(name, self.vec_dim)
        self.__load_vectors(name, self.vectors)


    def __init_collection(self, name: str, vector_size: int):
        self.client = QdrantClient(":memory:")
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


    def __load_documents(self):
        corpus = []
        for doc_name in listdir(self.data_dir):
            with open(path.join(self.data_dir, doc_name), "rt") as f:
                doc = Document(doc_name, f)
                doc.set_url(path.join("/", path.basename(self.data_dir), doc_name))
                self.documents.append(doc)
                corpus.append(doc.text)
        self.vectors = self.vectorizer.fit_transform(corpus).toarray()
        self.vec_dim = len(self.vectors[0])


    def __load_vectors(self, name: str, vectors: list):
        self.client.upsert(
            collection_name=name,
            points=[
                PointStruct(
                    id=idx,
                    vector=vector.tolist(),
                    payload={"url": self.documents[idx].get_url() }
                )
                for idx, vector in enumerate(vectors)
            ]
        )


    def search_docs(self, collection_name: str, query: str):
        q = Query(query, self.vectorizer.vocabulary_)
        feature_names = self.vectorizer.get_feature_names_out()
        vec = q.tovector(feature_names, self.vectorizer.idf_)
        hits = self.client.search(
            collection_name=collection_name,
            query_vector=vec,
            with_vectors=True,
            limit=5
        )
        res = []
        tmp_res = {}
        active_indices = q.get_active_indices(feature_names)
        num_arr = []
        for hit in hits:
            num = 0
            for i in range(len(vec)):
                if vec[i] != 0 and hit.vector[i] != 0:
                    num += 1
            words = [feature_names[word_ind] for word_ind in active_indices if hit.vector[word_ind] > 0]
            if not set(q.strict_words) <= set(words):
                continue
            print("Score: "+str(hit.score))
            tmp_res.update({hit.score+num*100: {
                "name": self.documents[hit.id].title,
                "words": words,
                "url": hit.payload["url"],
            }})
        res = [x for x in dict(sorted(tmp_res.items(), reverse=True)).values()]
        recs = []
        with open("./public" + res[0]["url"], "rt") as top_file:
            doc = Document("", top_file)
            vector = self.vectorizer.transform([doc.text]).toarray()[0]
            hits = self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                with_vectors=True,
                limit=8
            )
            hits = [x for x in hits if x.payload["url"] not in [y["url"] for y in res]]
            tmp_recs = {}
            for hit in hits:
                tmp_recs.update({hit.score: {
                    "name": self.documents[hit.id].title,
                    "words": words,
                    "url": hit.payload["url"],
                }})
            recs = [x for x in dict(sorted(tmp_recs.items(), reverse=True)).values()]
                
            
            
        #return { results: [x for x in res.values()], recommendations: [x for x in recommentations.values()]}
        return { "results": res, "recommendations": recs }
