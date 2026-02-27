import chromadb
from chromadb.utils import embedding_functions

class ConsultantAgent:
    def __init__(self, db_path="./data/db"):
        self.client = chromadb.PersistentClient(path=db_path)
        # MUST match the model used in IndexerAgent
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_collection(
            name="industrial_manuals",
            embedding_function=self.embedding_fn
        )

    def search(self, query, manufacturer=None, n_results=3):
        """Performs search in ChromaDB with optional metadata filtering."""
        where_clause = {}
        if manufacturer:
            where_clause["manufacturer"] = manufacturer
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None
        )
        return results

if __name__ == "__main__":
    # consultant = ConsultantAgent()
    # res = consultant.search("¿Cómo conectar un sensor PNP a un S7-1200?")
    pass
