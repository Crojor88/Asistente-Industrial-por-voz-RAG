import pyttsx3
import os

engine = pyttsx3.init()
test_file = "test_audio.wav"

try:
    print("Generando audio...")
    engine.save_to_file("Hola, esto es una prueba de sonido.", test_file)
    engine.runAndWait()
    
    if os.path.exists(test_file):
        size = os.path.getsize(test_file)
        print(f"Archivo generado correctamente: {test_file} (Tamaño: {size} bytes)")
    else:
        print("El archivo no se generó.")
except Exception as e:
    print(f"Error: {e}")
