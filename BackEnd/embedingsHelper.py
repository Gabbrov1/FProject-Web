import requests
from hyperdb import HyperDB
import numpy as np

class CodeEmbeddingDB:
    
    def __init__(self, save_path="./Saves/embedingSaves.pickle.gz"):
        self.save_path = save_path
        self.db = HyperDB(embedding_function=self.nomic_embedding)

    def nomic_embedding(self, documents):
        embeddings = []
        for doc in documents:
            text = doc if isinstance(doc, str) else doc["source"]
            response = requests.post("http://localhost:11434/api/embeddings",
                                    json={"model": "nomic-embed-text", "prompt": text})
            embeddings.append(np.array(response.json()["embedding"], dtype=np.float32))
        return embeddings

    def upload(self, data):
        documents = [{"name": item["name"], "source": item["source"]} for item in data]
        self.db = HyperDB(documents, embedding_function=self.nomic_embedding)
        self.db.save(self.save_path)
            

    def load(self):
        self.db.load(self.save_path)
        #print(f"Loaded {len(self.db.documents)} documents, vectors shape: {self.db.vectors}")

    def query(self, data, top_k=5):
        return self.db.query(data, top_k=top_k)