import asyncio
import os
import edge_tts

DEFAULT_VOICE = "es-MX-DaliaNeural"  # Voz femenina mexicana, dulce y expresiva
ALTERNATIVE_VOICE = "es-MX-CarlotaNeural"

async def _synthesize_async(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+5%", pitch: str = "+0Hz"):
    """
    Sintetiza texto a voz usando Microsoft Edge TTS (100% gratuito, calidad neural de estudio).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def generate_voiceover(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+5%"):
    """
    Función síncrona para generar locución.
    """
    return asyncio.run(_synthesize_async(text, output_path, voice=voice, rate=rate))

if __name__ == "__main__":
    test_text = "¡Hola! Soy Grip, la mascota de Tracción Digital. Hoy te enseño cómo hacer crecer tu negocio en internet sin complicaciones."
    test_file = os.path.join("output", "test_grip_voice.mp3")
    print(f"Generando voz con {DEFAULT_VOICE}...")
    generate_voiceover(test_text, test_file)
    print(f"Audio generado con éxito en: {test_file}")
