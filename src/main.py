import os
import ollama
from dotenv import load_dotenv
from agents.ingestion import IngestionAgent
from agents.indexer import IndexerAgent
from agents.consultant import ConsultantAgent
from agents.generator import GeneratorAgent

load_dotenv()

class RoboTechRAG:
    def __init__(self, text_model="llama3.2", vision_model="llava"):
        self._ensure_models([text_model, vision_model])
        self.ingestion = IngestionAgent(model_name=vision_model)
        self.indexer = IndexerAgent()
        self.consultant = ConsultantAgent()
        self.generator = GeneratorAgent(model_name=text_model)

    def _ensure_models(self, models):
        """Checks if models exist in local Ollama, pulls them if not."""
        try:
            res = ollama.list()
            available_models = [m.model for m in res.models]
            # Handle cases where name might include :latest tag
            available_names = [name.split(':')[0] for name in available_models]
            
            for model in models:
                if model not in available_names and model not in available_models:
                    print(f"Modelo '{model}' no encontrado localmente. Iniciando descarga...")
                    print("Esto puede tardar unos minutos (2-3 GB por modelo)...")
                    ollama.pull(model)
                    print(f"Modelo '{model}' descargado con éxito.")
        except Exception as e:
            print(f"Aviso: No se pudo verificar/descargar modelos automáticamente: {e}")
            print("Asegúrate de que Ollama esté ejecutándose.")

    def ingest_manual(self, pdf_path, manufacturer, model):
        """Complete pipeline to ingest a new manual locally."""
        print(f"Ingestando manual: {pdf_path}")
        content = self.ingestion.extract_content(pdf_path)
        metadata = {"manufacturer": manufacturer, "model": model}
        self.indexer.index_content(content, metadata)
        print("Finalizado.")

    def ask(self, query):
        """Complete pipeline to answer a technical query locally."""
        print(f"Consulta: {query}")
        search_results = self.consultant.search(query)
        if not search_results['documents'] or not search_results['documents'][0]:
            return "No se encontró información relevante en los manuales cargados."
            
        context = search_results['documents'][0]
        response = self.generator.generate_response(query, context)
        return response

if __name__ == "__main__":
    # Example usage (uncomment and provide a PDF to test)
    # rag = RoboTechRAG()
    # rag.ingest_manual("data/manuals/sample.pdf", "Siemens", "S7-1200")
    # print(rag.ask("¿Cuál es el voltaje de alimentación de la CPU 1214C DC/DC/DC?"))
    pass
