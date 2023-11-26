import nltk
from flask import Flask, send_from_directory, request, jsonify
from src.index_manager import Index

COLLECTION_NAME="test_collection"

if not nltk.data.find("corpora/stopwords"):
    nltk.download('stopwords')
if not nltk.find("corpora/wordnet"):
    nltk.download('wordnet')

app = Flask(__name__, static_url_path='', static_folder="public")
ind = Index(COLLECTION_NAME, "./public/data")

@app.route('/')
def index():
    return send_from_directory("public", "index.html")

@app.route('/search', methods=('POST',))
def search():
    print(request.get_json())
    query = request.get_json()["query"]
    return jsonify(ind.search_docs(COLLECTION_NAME, query))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
