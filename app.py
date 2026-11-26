import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from src.script_engine.generator import ScriptEngine
from src.voice_engine.tts import generate_voiceover, DEFAULT_VOICE
from src.video_engine.renderer import VideoRenderer
from src.trend_radar.radar import TrendRadar
from src.analytics.metrics import MetricsEngine

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "output", "videos")
AUDIOS_DIR = os.path.join(BASE_DIR, "output", "audios")
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(AUDIOS_DIR, exist_ok=True)

script_engine = ScriptEngine()
video_renderer = VideoRenderer()
trend_radar = TrendRadar()
metrics_engine = MetricsEngine()

@app.route("/")
def index():
    trends = trend_radar.scan_viral_trends()
    videos = metrics_engine.list_all_videos()
    return render_template("index.html", trends=trends, videos=videos)

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

@app.route("/api/trends", methods=["GET"])
def get_trends():
    return jsonify(trend_radar.scan_viral_trends())

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    return jsonify(metrics_engine.list_all_videos())

@app.route("/api/generate", methods=["POST"])
def generate_video_api():
    try:
        data = request.json or {}
        slot = data.get("slot", "morning")
        style = data.get("style", "Grip")
        custom_topic = data.get("topic") or None

        # 1. Generar guión con reglas estrictas (sin costos)
        script_data = script_engine.generate_script(slot=slot, custom_topic=custom_topic)
        
        timestamp = int(time.time())
        audio_filename = f"voice_{slot}_{timestamp}.mp3"
        audio_path = os.path.join(AUDIOS_DIR, audio_filename)
        
        # 2. Sintetizar locución femenina dulce con Edge-TTS
        generate_voiceover(script_data["full_speech"], audio_path, voice=DEFAULT_VOICE)

        # 3. Renderizar Video 1080x1920 con Grip o B-roll
        video_filename = f"video_{slot}_{timestamp}.mp4"
        video_path = video_renderer.render_video(
            audio_path=audio_path,
            title=script_data["hook"],
            text=f"{script_data['problem']} {script_data['solution']}",
            output_filename=video_filename,
            style=style
        )

        # 4. Registrar en base de datos de métricas
        video_id = metrics_engine.register_video({
            "title": script_data["topic"],
            "slot": slot,
            "style": style,
            "hook": script_data["hook"],
            "topic": script_data["topic"],
            "video_path": video_path,
            "audio_path": audio_path
        })

        return jsonify({
            "success": True,
            "video_id": video_id,
            "title": script_data["topic"],
            "hook": script_data["hook"],
            "speech": script_data["full_speech"],
            "video_url": f"/videos/{video_filename}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Agente Grip Video de Tracción Digital iniciado")
    print("🌐 Interfaz accesible en: http://localhost:5000 o http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
