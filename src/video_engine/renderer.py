import os
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class VideoRenderer:
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output", "videos")
        os.makedirs(self.output_dir, exist_ok=True)
        self.grip_img_path = os.path.join(self.assets_dir, "grip", "grip_waving.png")

    def _get_audio_duration(self, audio_path: str) -> float:
        """Obtiene la duración exacta del audio usando ffprobe/ffmpeg."""
        cmd = [
            FFMPEG_EXE, "-i", audio_path
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        # Parse Duration: 00:00:15.32
        for line in result.stderr.splitlines():
            if "Duration:" in line:
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
        return 15.0

    def create_frame(self, t: float, total_duration: float, title: str, text: str, style: str = "Grip") -> Image.Image:
        """
        Crea un frame vertical 1080x1920 para el tiempo t.
        """
        # 1. Fondo degradado Tech de Tracción Digital
        img = Image.new("RGB", (self.width, self.height), color="#0b132b")
        draw = ImageDraw.Draw(img)

        # Gradiente simulado
        for y in range(0, self.height, 4):
            factor = y / self.height
            r = int(11 * (1 - factor) + 28 * factor)
            g = int(19 * (1 - factor) + 37 * factor)
            b = int(43 * (1 - factor) + 65 * factor)
            draw.rectangle([(0, y), (self.width, y + 4)], fill=(r, g, b))

        # Cuadrícula o líneas sutiles de fondo
        grid_color = (255, 255, 255, 12)
        for x in range(0, self.width, 120):
            draw.line([(x, 0), (x, self.height)], fill=(20, 35, 70), width=1)
        for y in range(0, self.height, 120):
            draw.line([(0, y), (self.width, y)], fill=(20, 35, 70), width=1)

        # 2. Header Superior (Marca & Badge)
        # Badge Tracción Digital
        draw.rounded_rectangle([(140, 100), (self.width - 140, 190)], radius=30, fill="#1c2541", outline="#00a8ff", width=3)
        draw.text((self.width // 2, 145), "TRACCIÓN DIGITAL • tracciondigital.com.mx", fill="#48cae4", anchor="mm")

        # 3. Título / Gancho Principal (Hook Box)
        draw.rounded_rectangle([(80, 240), (self.width - 80, 480)], radius=35, fill=(15, 23, 42), outline="#fca311", width=4)
        
        # Partir el título en líneas
        words = title.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 26:
                cur.pop()
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))

        y_title = 310
        for line in lines[:3]:
            draw.text((self.width // 2, y_title), line, fill="#ffffff", anchor="mm")
            y_title += 60

        # 4. Modo Grip vs Modo B-Roll
        if style == "Grip" and os.path.exists(self.grip_img_path):
            grip = Image.open(self.grip_img_path).convert("RGBA")
            # Escalar a tamaño apropiado (ej. altura ~850px)
            aspect = grip.width / grip.height
            target_h = 850
            target_w = int(target_h * aspect)
            grip_resized = grip.resize((target_w, target_h), Image.Resampling.LANCZOS)

            # Efecto sutil de flotación / respiración con onda senoidal
            bob = int(math.sin(t * 3.0) * 15)
            x_pos = (self.width - target_w) // 2
            y_pos = 960 + bob

            # Sombra de Grip
            shadow_w = int(target_w * 0.7)
            draw.ellipse([
                (self.width // 2 - shadow_w // 2, 1780),
                (self.width // 2 + shadow_w // 2, 1840)
            ], fill=(5, 10, 25))

            img.paste(grip_resized, (x_pos, y_pos), grip_resized)

            # Globo de diálogo o texto de subtítulo flotante
            draw.rounded_rectangle([(80, 540), (self.width - 80, 880)], radius=30, fill="#1e293b", outline="#38bdf8", width=3)
            # Texto explicativo adaptativo
            text_lines = []
            cur_t = []
            for w in text.split():
                cur_t.append(w)
                if len(" ".join(cur_t)) > 32:
                    cur_t.pop()
                    text_lines.append(" ".join(cur_t))
                    cur_t = [w]
            if cur_t:
                text_lines.append(" ".join(cur_t))

            yt = 620
            for tl in text_lines[:4]:
                draw.text((self.width // 2, yt), tl, fill="#f8fafc", anchor="mm")
                yt += 55

        else:
            # Modo Tech / B-Roll
            draw.rounded_rectangle([(80, 560), (self.width - 80, 1300)], radius=35, fill="#0f172a", outline="#00a8ff", width=4)
            draw.text((self.width // 2, 650), "💡 CLAVE DEL DÍA", fill="#fca311", anchor="mm")
            
            # Texto en caja grande
            text_lines = []
            cur_t = []
            for w in text.split():
                cur_t.append(w)
                if len(" ".join(cur_t)) > 28:
                    cur_t.pop()
                    text_lines.append(" ".join(cur_t))
                    cur_t = [w]
            if cur_t:
                text_lines.append(" ".join(cur_t))

            yt = 770
            for tl in text_lines[:6]:
                draw.text((self.width // 2, yt), tl, fill="#f1f5f9", anchor="mm")
                yt += 65

        # 5. Footer con Llamado a la Acción (CTA)
        draw.rounded_rectangle([(100, 1820), (self.width - 100, 1890)], radius=25, fill="#fca311")
        draw.text((self.width // 2, 1855), "👉 Más información en tracciondigital.com.mx", fill="#000000", anchor="mm")

        return img

    def render_video(self, audio_path: str, title: str, text: str, output_filename: str, style: str = "Grip") -> str:
        """
        Renderiza el video completo MP4 sincronizado con el audio.
        """
        duration = self._get_audio_duration(audio_path)
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Generar un frame base optimizado o secuencia
        base_frame = self.create_frame(0.0, duration, title, text, style=style)
        temp_frame_path = os.path.join(self.output_dir, "_temp_frame.png")
        base_frame.save(temp_frame_path)

        # Ensamblar con FFmpeg: imagen fija animada + audio sincronizado
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", temp_frame_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", str(duration + 0.5),
            output_path
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)

        return output_path

if __name__ == "__main__":
    renderer = VideoRenderer()
    sample_audio = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output", "test_grip_voice.mp3")
    if os.path.exists(sample_audio):
        print("Renderizando video de prueba con Grip...")
        vid = renderer.render_video(
            sample_audio, 
            "¿Para qué sirve Google Search Console?", 
            "Es la herramienta oficial de Google que te dice cómo te buscan tus clientes y qué corregir en tu web.",
            "test_video_grip.mp4",
            style="Grip"
        )
        print("Video renderizado con éxito en:", vid)
    else:
        print("No se encontró el audio de prueba.")
