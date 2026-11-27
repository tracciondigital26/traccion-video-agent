import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from src.script_engine.generator import ScriptEngine
from src.video_engine.renderer import VideoRenderer
from src.trend_radar.radar import TrendRadar
from src.analytics.metrics import MetricsEngine

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "output", "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

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

@app.route("/download/<path:filename>")
def download_video(filename):
    return send_from_directory(VIDEOS_DIR, filename, as_attachment=True)

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
        slot = data.get("slot", "evening")
        custom_topic = data.get("topic") or None

        # 1. Generar historia multiescena completa (5 escenas)
        story = script_engine.generate_story(slot=slot, custom_topic=custom_topic)
        
        timestamp = int(time.time())
        video_filename = f"video_grip_{slot}_{timestamp}.mp4"
        
        # 2. Renderizar video multiescena sincronizado con locución
        video_path = video_renderer.render_full_story_video(story, video_filename)

        # 3. Registrar en base de datos de métricas
        video_id = metrics_engine.register_video({
            "title": story["topic"],
            "slot": slot,
            "style": "Grip Multiescena",
            "hook": story["scene1"]["title"],
            "topic": story["topic"],
            "video_path": video_path,
            "audio_path": ""
        })

        return jsonify({
            "success": True,
            "video_id": video_id,
            "title": story["topic"],
            "hook": story["scene1"]["title"],
            "video_url": f"/videos/{video_filename}",
            "download_url": f"/download/{video_filename}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Agente Grip Video de Tracción Digital iniciado")
    print("🌐 Interfaz accesible en: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
