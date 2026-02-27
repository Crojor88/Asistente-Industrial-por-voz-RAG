import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from main import RoboTechRAG
except ImportError as e:
    print(f"Error importando RoboTechRAG: {e}")
    sys.exit(1)

def test():
    print("--- INICIANDO ROBO-TECH RAG (MODO LOCAL) ---")
    print("Aviso: Si es la primera vez, Ollama descargará los modelos (Llava y Llama 3.2).")
    
    rag = RoboTechRAG()
    
    # Pruebas con el PDF que ya tenemos en data/manuals
    pdf_test = "data/manuals/rag_design.pdf"
    
    if os.path.exists(pdf_test):
        print("\n--- PASO 1: Ingestando Manual de Prueba ---")
        rag.ingest_manual(pdf_test, "RoboTech", "DesignDoc")
        
        print("\n--- PASO 2: Realizando Consulta ---")
        query = "¿Cuáles son los componentes principales de este sistema RAG?"
        response = rag.ask(query)
        
        print("\n--- RESPUESTA DEL AGENTE ---")
        print(response)
    else:
        print(f"\nERROR: No se encontró el archivo {pdf_test}.")
        print("Asegúrate de que el archivo existe en la carpeta data/manuals/")

if __name__ == "__main__":
    test()

if __name__ == "__main__":
    test()
