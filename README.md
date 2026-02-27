# RoboTech RAG

Sistema de Retrieval Augmented Generation (RAG) especializado para consulta de manuales técnicos de robótica e industrial.

## ¿Qué es?

**RoboTech RAG** es un sistema de inteligencia artificial local que permite ingestar, indexar y consultar manuales técnicos de robots y equipos industriales de forma inteligente. Utiliza modelos de lenguaje locales (Ollama) para procesar documentos PDF y responder preguntas técnicas específicas.

## ¿Para qué sirve?

- **Ingestión de manuales**: Extrae contenido de PDFs incluyendo texto, tablas y diagramas técnicos
- **Indexación semántica**: Almacena el contenido en una base de datos vectorial para búsqueda rápida
- **Consulta inteligente**: Responde preguntas técnicas usando el contexto de los manuales cargados
- **Procesamiento de imágenes**: Describe diagramas técnicos, esquemas de cableado y diagramas Ladder/ST mediante visión artificial local

## Arquitectura

El sistema está compuesto por 4 agentes:

```
RoboTechRAG
├── IngestionAgent    → Extrae contenido de PDFs (texto + imágenes)
├── IndexerAgent      → Indexa contenido en ChromaDB (base vectorial)
├── ConsultantAgent   → Busca información relevante por similitud semántica
└── GeneratorAgent    → Genera respuestas usando Ollama local
```

### Tecnologías utilizadas

- **Ollama**: Modelos LLM locales (Llama 3.2, LLaVA)
- **ChromaDB**: Base de datos vectorial para búsqueda semántica
- **Sentence-Transformers**: Modelo de embeddings (all-MiniLM-L6-v2)
- **PyMuPDF**: Extracción de contenido PDF
- **Python**: Lenguaje principal

## Requisitos previos

1. **Ollama instalado y ejecutándose**
   - Descarga: https://ollama.com
   - Modelos necesarios: `llama3.2` y `llava`

2. **Python 3.11+**

3. **Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Crojor88/RoboTech-RAG.git
   cd RoboTech-RAG
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura el archivo `.env` (copia de `.env.example`):
   ```
   # Por ahora no requiere API keys (usa Ollama local)
   ```

5. Asegúrate de tener Ollama instalado y ejecutándose:
   ```bash
   ollama serve
   ```

## Uso

### Inicializar el sistema

```python
from src.main import RoboTechRAG

# Por defecto usa llama3.2 (texto) y llava (imágenes)
rag = RoboTechRAG()
```

### Ingestar un manual

```python
# Ingestar un manual PDF
rag.ingest_manual(
    pdf_path="data/manuals/mi_manual.pdf",
    manufacturer="Siemens",
    model="S7-1200"
)
```

### Realizar consultas

```python
# Preguntar al sistema
respuesta = rag.ask("¿Cuál es el voltaje de alimentación de la CPU 1214C?")
print(respuesta)
```

### Filtrar por fabricante

```python
# Buscar solo en manuales de un fabricante específico
results = consultant.search(
    "¿Cómo conectar un sensor PNP?",
    manufacturer="Siemens"
)
```

## Estructura del proyecto

```
Sistema RAG/
├── src/
│   ├── main.py              # Clase principal RoboTechRAG
│   └── agents/
│       ├── ingestion.py      # Extracción de PDF
│       ├── indexer.py       # Indexación en ChromaDB
│       ├── consultant.py    # Búsqueda semántica
│       └── generator.py     # Generación de respuestas
├── data/
│   ├── db/                  # Base de datos ChromaDB
│   └── manuals/             # PDFs de manuales
├── Informacion/             # Documentación del sistema
├── requirements.txt         # Dependencias Python
└── test_rag.py              # Pruebas del sistema
```

## Ejemplo completo

```python
from src.main import RoboTechRAG

# Inicializar
rag = RoboTechRAG()

# Cargar un manual
rag.ingest_manual(
    "data/manuals/s7-1200_manual.pdf",
    "Siemens",
    "S7-1200"
)

# Realizar preguntas técnicas
print(rag.ask("¿Cómo programo un temporizador en TIA Portal?"))
print(rag.ask("¿Qué tipo de fuente necesito para el PLC 1214C?"))
```

## Limitaciones

- Requiere Ollama ejecutándose localmente
- Los primeros arranques pueden tardar en descargar modelos (~2-3 GB cada uno)
- El rendimiento depende del hardware disponible (RAM/GPU)
- Solo soporta PDFs por ahora

## Licencia

MIT License

## Autor

Desarrollado como proyecto de automatización industrial con IA.
