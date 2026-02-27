import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from main import RoboTechRAG
except ImportError as e:
    print(f"Error importando RoboTechRAG: {e}")
    sys.exit(1)

def bulk_ingest():
    rag = RoboTechRAG()
    
    manuals = [
        {"path": "data/manuals/schneider_ic60n_manual.pdf", "mfr": "Schneider Electric", "model": "iC60N"},
        {"path": "data/manuals/schneider_iid_manual.pdf", "mfr": "Schneider Electric", "model": "iID"},
        {"path": "data/manuals/schneider_gv2_manual.pdf", "mfr": "Schneider Electric", "model": "GV2"},
        {"path": "data/manuals/siemens_s7-1200_manual.pdf", "mfr": "Siemens", "model": "S7-1200"}
    ]
    
    for manual in manuals:
        if os.path.exists(manual["path"]):
            # Check if file is not empty or HTML error page
            if os.path.getsize(manual["path"]) > 1000:
                print(f"\n--- Ingestando {manual['model']} ---")
                try:
                    rag.ingest_manual(manual["path"], manual["mfr"], manual["model"])
                except Exception as e:
                    print(f"Error ingrestando {manual['model']}: {e}")
            else:
                print(f"Aviso: El archivo {manual['path']} parece estar corrupto o es muy pequeño.")
        else:
            print(f"Archivo no encontrado: {manual['path']}")

if __name__ == "__main__":
    bulk_ingest()
