import chromadb
from chromadb.utils import embedding_functions
import os

class IndexerAgent:
    def __init__(self, db_path="./data/db"):
        self.client = chromadb.PersistentClient(path=db_path)
        # Using a local embedding model (no API needed)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="industrial_manuals",
            embedding_function=self.embedding_fn
        )

    def index_content(self, processed_content, metadata_base):
        """Indexes extracted content into ChromaDB."""
        ids = []
        documents = []
        metadatas = []
        
        for page_data in processed_content:
            page_num = page_data["page"]
            text = page_data["text"]
            diagrams = "\n".join(page_data["diagrams"])
            
            # Combine text and diagram descriptions for holistic context
            combined_text = f"Página {page_num}\n{text}\n{diagrams}"
            
            chunk_id = f"{metadata_base['model']}_p{page_num}_{os.urandom(4).hex()}"
            ids.append(chunk_id)
            documents.append(combined_text)
            metadatas.append({
                **metadata_base,
                "page": page_num
            })
            
        if ids:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            print(f"Indexados {len(ids)} fragmentos para {metadata_base['model']}.")

if __name__ == "__main__":
    # Example usage
    # indexer = IndexerAgent()
    # indexer.index_content(content, {"manufacturer": "Siemens", "model": "S7-1200"})
    pass
