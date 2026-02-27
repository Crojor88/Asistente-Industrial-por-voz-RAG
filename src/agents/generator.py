import ollama
from dotenv import load_dotenv
import re

load_dotenv()

class GeneratorAgent:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name

    def generate_response(self, query, context_documents):
        """Generates a technical response using local Ollama model."""
        context_str = "\n---\n".join(context_documents)
        
        prompt = f"""
        Actúa como un experto en Automatización Industrial y Robótica.
        Utilizando el CONTEXTO proporcionado (que incluye texto y descripciones de diagramas de manuales oficiales), responde a la PREGUNTA del usuario.
        
        REGLAS:
        1. Formato: Markdown industrial limpio.
        2. Incluye siempre una sección de 'Citas y Referencias'.
        3. Si incluyes código (Ladder/ST/FBD), asegúrate de que sea compatible con el fabricante mencionado.
        4. Si el contexto menciona un diagrama, descríbelo o haz referencia a él.
        5. Si la información no es suficiente, indícalo claramente.
        
        CONTEXTO:
        {context_str}
        
        PREGUNTA:
        {query}
        """
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"Error generando respuesta con {self.model_name}: {str(e)}"

    def validate_code(self, code, language="ST"):
        """Simple validation logic for PLC code syntax."""
        if language == "ST":
            if ":=" not in code:
                return False, "Falta operador de asignación ':='"
            if not code.strip().endswith(";"):
                return False, "Falta punto y coma final ';'"
        return True, "Código válido"

if __name__ == "__main__":
    # generator = GeneratorAgent()
    # response = generator.generate_response("query", ["context 1", "context 2"])
    pass
