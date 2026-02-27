import fitz  # PyMuPDF
import os
from PIL import Image
import io
import ollama
from dotenv import load_dotenv

load_dotenv()

class IngestionAgent:
    def __init__(self, model_name="llava"):
        self.model_name = model_name
        # Ensure model is available (will pull if not present during first run)
        # Note: In a real app we might want to check this explicitly

    def extract_content(self, pdf_path):
        """Extracts text, tables (as text), and images from PDF."""
        doc = fitz.open(pdf_path)
        content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Extract images
            images = page.get_images(full=True)
            image_descriptions = []
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Use Ollama/Llava to describe the image
                description = self.describe_technical_image(image_bytes)
                image_descriptions.append(f"[DIAGRAMA {img_index}]: {description}")
            
            page_content = {
                "page": page_num + 1,
                "text": text,
                "diagrams": image_descriptions
            }
            content.append(page_content)
            
        return content

    def describe_technical_image(self, image_bytes):
        """Uses local Ollama/Llava to generate a technical description of a diagram."""
        try:
            prompt = "Describe este diagrama técnico industrial de forma detallada. Indica si es un esquema de cableado, un diagrama de bloques de software (Ladder/ST), un gráfico de rendimiento o una foto de hardware. Identifica puertos, voltajes y componentes clave."
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                images=[image_bytes]
            )
            return response['response']
        except Exception as e:
            return f"Error describiendo imagen con {self.model_name}: {str(e)}"

    def browse_and_download(self, query):
        """Placeholder for browser automation logic."""
        print(f"Buscando manuales para: {query}...")
        pass

if __name__ == "__main__":
    # Example usage
    # agent = IngestionAgent(api_key="YOUR_API_KEY")
    # content = agent.extract_content("path/to/manual.pdf")
    pass
