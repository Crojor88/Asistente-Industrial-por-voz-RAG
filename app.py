import os
import sys
import tempfile
import time
import numpy as np
import soundfile as sf
import pyttsx3
from faster_whisper import WhisperModel
import gradio as gr

# Add src to path to import RAG components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from main import RoboTechRAG

# --- Configuration & Initialization ---
print("Inicializando modelos locales (esto puede tardar unos segundos)...")

# 1. Initialize RAG System (Ollama llama3.2 + SentenceTransformers)
rag = RoboTechRAG()

# 2. Initialize STT (Faster-Whisper: tiny or base model for speed on CPU)
# Use 'cpu' and 'int8' for broader compatibility without complex CUDA setups initially
stt_model = WhisperModel("tiny", device="cpu", compute_type="int8")

# 3. Initialize TTS (pyttsx3 - Native Windows Voice)
tts_engine = pyttsx3.init()
# Try to set a Spanish voice if available
voices = tts_engine.getProperty('voices')
for voice in voices:
    if "spanish" in voice.name.lower() or "es" in voice.id.lower() or "helena" in voice.name.lower():
        tts_engine.setProperty('voice', voice.id)
        break
tts_engine.setProperty('rate', 150) # Speed of speech

print("¡Sistemas inicializados!")

# --- Audio Processing Functions ---

def transcribe_audio(audio_tuple):
    """Converts numpy audio array from Gradio to text using Faster-Whisper."""
    if audio_tuple is None:
        return ""
    
    sample_rate, audio_data = audio_tuple
    
    # Gradio might send int16 or float32. Whisper expects float32 between -1 and 1
    if audio_data.dtype != np.float32:
        audio_data = audio_data.astype(np.float32)
        if np.max(np.abs(audio_data)) > 1.0:
            audio_data /= 32768.0 # Normalize int16
    
    # Ensure mono channel for whisper
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    # We need to save it to a temporary valid wav file because faster-whisper 
    # handles files more reliably than raw numpy arrays in some versions
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio_data, sample_rate)
        tmp_path = tmp.name

    try:
        segments, info = stt_model.transcribe(tmp_path, language="es")
        text = " ".join([segment.text for segment in segments])
    finally:
        os.remove(tmp_path)
    
    return text.strip()

import multiprocessing

def _tts_worker(text, output_file):
    """Isolated worker process for pyttsx3 to prevent thread blocking/freezing."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "spanish" in voice.name.lower() or "es" in voice.id.lower() or "helena" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

def text_to_speech(text):
    """Converts text to an audio file using pyttsx3 in an isolated process."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_file = tmp.name
    
    # Run pyttsx3 in a separate process to avoid COM threading issues on Windows
    # which causes the engine to freeze on the second request in Gradio threads
    process = multiprocessing.Process(target=_tts_worker, args=(text, output_file))
    process.start()
    process.join()  # Wait for the audio file to be completely generated
    
    return output_file

# --- Gradio Chatbot Logic ---

def process_interaction(audio_input, text_input, history):
    """Main function handling the logic when user sends a message (voice or text)."""
    
    # 1. Determine Input
    user_query = ""
    if audio_input is not None:
        user_query = transcribe_audio(audio_input)
    elif text_input:
        user_query = text_input
        
    if not user_query:
        return history, None, "", None
        
    print(f"\n[Usuario]: {user_query}")
    
    # Update history with user query
    history.append({"role": "user", "content": user_query})
    
    # 2. Get Response from RAG
    # We yield an intermediate state to show it's "thinking"
    thinking_message = "Consultando manuales industriales locales..."
    history.append({"role": "assistant", "content": thinking_message})
    yield history, None, "", None
    
    try:
        response_text = rag.ask(user_query)
    except Exception as e:
        response_text = f"Error al procesar la consulta: {str(e)}"
    
    print(f"[Asistente RAG]: {response_text[:100]}...")
    
    # Update the thinking message with the real answer
    history[-1]["content"] = response_text
    
    # 3. Generate Audio Response
    # We clean the text lightly for TTS (remove markdown bolding, etc.)
    text_for_tts = response_text.replace("*", "").replace("#", "")
    audio_output_path = text_to_speech(text_for_tts)
    
    # Return updated history, clear inputs, and provide audio output
    yield history, None, "", audio_output_path


# --- Gradio UI Layout ---

with gr.Blocks(title="RoboTech RAG") as demo:
    gr.Markdown("# 🤖 RoboTech RAG - Asistente Industrial")
    gr.Markdown("Consultas técnicas mediante voz o texto sobre diagramas PLC, manuales eléctricos y configuraciones (100% Local).")
    
    chatbot = gr.Chatbot(height=500)
    
    with gr.Row():
        with gr.Column(scale=8):
            text_input = gr.Textbox(placeholder="Escribe tu consulta aquí...", show_label=False)
        with gr.Column(scale=1):
            audio_input = gr.Audio(sources=["microphone"], type="numpy", label="Hablar")
            
    with gr.Row():
        submit_btn = gr.Button("Enviar", variant="primary")
        clear_btn = gr.Button("Limpiar Historial")
        
    # Audio component to play the TTS response
    audio_output = gr.Audio(label="Respuesta de voz", autoplay=True)
    
    # Event wiring
    submit_btn.click(
        process_interaction,
        inputs=[audio_input, text_input, chatbot],
        outputs=[chatbot, audio_input, text_input, audio_output]
    )
    
    text_input.submit(
        process_interaction,
        inputs=[audio_input, text_input, chatbot],
        outputs=[chatbot, audio_input, text_input, audio_output]
    )
    
    clear_btn.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    # Launch on localhost
    print("Iniciando servidor web local...")
    # Queue is required for yield (streaming interface updates)
    demo.launch(server_name="127.0.0.1", server_port=7860, prevent_thread_lock=False, theme=gr.themes.Soft())
