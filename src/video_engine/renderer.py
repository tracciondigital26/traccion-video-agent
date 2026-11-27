import os
import sys
import subprocess
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from src.voice_engine.tts import generate_voiceover, DEFAULT_VOICE

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class VideoRenderer:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.output_dir = os.path.join(self.base_dir, "output", "videos")
        self.temp_dir = os.path.join(self.base_dir, "output", "temp_scenes")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        self.grip_path = os.path.join(self.assets_dir, "grip", "grip_waving.png")
        self.escudo_path = os.path.join(self.assets_dir, "branding", "escudo.png")
        self.bg_path = os.path.join(self.assets_dir, "branding", "bg_clean.png")

        self._init_fonts()

    def _init_fonts(self):
        try:
            self.font_title = ImageFont.truetype("arialbd.ttf", 52)
            self.font_subtitle = ImageFont.truetype("arial.ttf", 36)
            self.font_badge = ImageFont.truetype("arialbd.ttf", 30)
            self.font_pill = ImageFont.truetype("arialbd.ttf", 44)
            self.font_card = ImageFont.truetype("arialbd.ttf", 34)
            self.font_card_sub = ImageFont.truetype("arial.ttf", 26)
            self.font_sub_box = ImageFont.truetype("arialbd.ttf", 38)
        except Exception:
            default = ImageFont.load_default()
            self.font_title = self.font_subtitle = self.font_badge = self.font_pill = self.font_card = self.font_card_sub = self.font_sub_box = default

    def _get_base_image(self) -> Image.Image:
        if os.path.exists(self.bg_path):
            img = Image.open(self.bg_path).convert("RGBA").resize((self.width, self.height))
        else:
            img = Image.new("RGBA", (self.width, self.height), color="#0d131f")
        
        # Superponer el escudo oficial en el header
        if os.path.exists(self.escudo_path):
            escudo = Image.open(self.escudo_path).convert("RGBA")
            escudo_w, escudo_h = escudo.size
            img.paste(escudo, ((self.width - escudo_w) // 2, 60), escudo)
        return img

    def _draw_subtitle_box(self, draw: ImageDraw.Draw, text: str, y: int = 1530):
        margin_x = 70
        box_w = self.width - (margin_x * 2)
        box_h = 160
        draw.rounded_rectangle(
            [(margin_x, y), (margin_x + box_w, y + box_h)],
            radius=28,
            fill="#090d16"
        )
        words = text.split()
        line1, line2 = [], []
        for w in words:
            if len(" ".join(line1 + [w])) <= 32:
                line1.append(w)
            else:
                line2.append(w)
        
        t1 = " ".join(line1)
        t2 = " ".join(line2)
        if t2:
            draw.text((self.width // 2, y + 45), t1, fill="#ffffff", font=self.font_sub_box, anchor="mm")
            draw.text((self.width // 2, y + 105), t2, fill="#ffffff", font=self.font_sub_box, anchor="mm")
        else:
            draw.text((self.width // 2, y + 80), t1, fill="#ffffff", font=self.font_sub_box, anchor="mm")

    def _draw_grip(self, img: Image.Image, x: int, y: int, target_h: int = 620):
        if not os.path.exists(self.grip_path):
            return
        grip = Image.open(self.grip_path).convert("RGBA")
        aspect = grip.width / grip.height
        target_w = int(target_h * aspect)
        grip_resized = grip.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        shadow_w = int(target_w * 0.75)
        shadow_y = y + target_h - 20
        draw.ellipse(
            [(self.width // 2 - shadow_w // 2, shadow_y), (self.width // 2 + shadow_w // 2, shadow_y + 40)],
            fill=(5, 8, 15, 200)
        )
        img.paste(grip_resized, (x - target_w // 2, y), grip_resized)

    def render_scene1(self, sc: Dict[str, Any]) -> Image.Image:
        img = self._get_base_image()
        draw = ImageDraw.Draw(img)

        badge_text = sc.get("badge", "GRIP TE EXPLICA")
        draw.rounded_rectangle([(340, 270), (740, 350)], radius=40, fill="#f59e0b")
        draw.text((540, 310), badge_text, fill="#000000", font=self.font_badge, anchor="mm")

        title = sc.get("title", "")
        # Partir título si es largo
        words = title.split()
        l1, l2 = [], []
        for w in words:
            if len(" ".join(l1 + [w])) <= 24:
                l1.append(w)
            else:
                l2.append(w)
        if l2:
            draw.text((540, 430), " ".join(l1), fill="#ffffff", font=self.font_title, anchor="mm")
            draw.text((540, 495), " ".join(l2), fill="#ffffff", font=self.font_title, anchor="mm")
        else:
            draw.text((540, 450), title, fill="#ffffff", font=self.font_title, anchor="mm")

        self._draw_grip(img, 540, 750, target_h=640)
        self._draw_subtitle_box(draw, sc.get("subtitle", ""))
        return img

    def render_scene2(self, sc: Dict[str, Any]) -> Image.Image:
        img = self._get_base_image()
        draw = ImageDraw.Draw(img)

        draw.text((540, 250), sc.get("title", "Tu dirección en la web"), fill="#ffffff", font=self.font_title, anchor="mm")

        pill_text = sc.get("pill", "tracciondigital.com.mx")
        draw.rounded_rectangle([(70, 320), (1010, 430)], radius=55, fill="#ffffff")
        draw.text((540, 375), f"🔒  {pill_text}", fill="#0f172a", font=self.font_pill, anchor="mm")

        tags = sc.get("tags", ["Lleva tu nombre", "Fácil de recordar • Más confianza"])
        if len(tags) >= 1:
            draw.rounded_rectangle([(340, 470), (740, 540)], radius=35, fill="#3b82f6")
            draw.text((540, 505), tags[0], fill="#ffffff", font=self.font_badge, anchor="mm")
        if len(tags) >= 2:
            draw.rounded_rectangle([(180, 570), (900, 640)], radius=35, fill="#f59e0b")
            draw.text((540, 605), tags[1], fill="#000000", font=self.font_badge, anchor="mm")

        self._draw_grip(img, 540, 750, target_h=620)
        self._draw_subtitle_box(draw, sc.get("subtitle", ""))
        return img

    def render_scene3(self, sc: Dict[str, Any]) -> Image.Image:
        img = self._get_base_image()
        draw = ImageDraw.Draw(img)

        # Icono Lupa
        draw.ellipse([(480, 240), (600, 360)], outline="#38bdf8", width=10)
        draw.line([(570, 330), (630, 390)], fill="#f59e0b", width=14)

        draw.text((540, 460), sc.get("title", "Google Search Console"), fill="#f59e0b", font=self.font_title, anchor="mm")
        draw.text((540, 540), sc.get("subtitle_top", "¿Cómo te ve Google?"), fill="#ffffff", font=self.font_title, anchor="mm")

        self._draw_grip(img, 540, 750, target_h=620)
        self._draw_subtitle_box(draw, sc.get("subtitle", ""))
        return img

    def render_scene4(self, sc: Dict[str, Any]) -> Image.Image:
        img = self._get_base_image()
        draw = ImageDraw.Draw(img)

        draw.text((540, 250), sc.get("title", "Además"), fill="#f59e0b", font=self.font_title, anchor="mm")

        features = sc.get("features", ["Páginas indexadas", "Mapa del sitio", "Avisos de problemas"])
        colors = ["#38bdf8", "#f59e0b", "#38bdf8"]
        y_pos = 330
        for i, feat in enumerate(features[:3]):
            draw.rounded_rectangle([(100, y_pos), (980, y_pos + 85)], radius=25, fill="#162238")
            draw.ellipse([(130, y_pos + 18), (180, y_pos + 68)], fill=colors[i % len(colors)])
            draw.text((155, y_pos + 43), "✓", fill="#000000", font=self.font_badge, anchor="mm")
            draw.text((210, y_pos + 43), feat, fill="#ffffff", font=self.font_card, anchor="lm")
            y_pos += 110

        self._draw_grip(img, 540, 780, target_h=600)
        self._draw_subtitle_box(draw, sc.get("subtitle", ""))
        return img

    def render_scene5(self, sc: Dict[str, Any]) -> Image.Image:
        img = self._get_base_image()
        draw = ImageDraw.Draw(img)

        self._draw_grip(img, 540, 160, target_h=320)
        draw.text((540, 530), "Tracción Digital", fill="#ffffff", font=self.font_title, anchor="mm")

        contacts = [
            ("WhatsApp", "+52 296 162 2434"),
            ("Correo", "contacto@tracciondigital.com.mx\njuancarlosrope@tracciondigital.com.mx"),
            ("Instagram", "@tracciondigital_26"),
            ("TikTok", "@tracciondigital26"),
            ("Facebook", "Tracción Digital")
        ]

        y_pos = 620
        for label, val in contacts:
            h = 120 if "\n" in val else 85
            draw.rounded_rectangle([(90, y_pos), (990, y_pos + h)], radius=22, fill="#162238")
            draw.text((130, y_pos + 20), label, fill="#f59e0b", font=self.font_card_sub, anchor="lm")
            if "\n" in val:
                lines = val.split("\n")
                draw.text((130, y_pos + 52), lines[0], fill="#ffffff", font=self.font_badge, anchor="lm")
                draw.text((130, y_pos + 86), lines[1], fill="#ffffff", font=self.font_badge, anchor="lm")
            else:
                draw.text((130, y_pos + 52), val, fill="#ffffff", font=self.font_card, anchor="lm")
            y_pos += h + 18

        draw.rounded_rectangle([(200, 1370), (880, 1460)], radius=45, fill="#f59e0b")
        draw.text((540, 1415), "tracciondigital.com.mx", fill="#000000", font=self.font_pill, anchor="mm")
        return img

    def _get_audio_duration(self, audio_path: str) -> float:
        cmd = [FFMPEG_EXE, "-i", audio_path]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in result.stderr.splitlines():
            if "Duration:" in line:
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
        return 10.0

    def render_full_story_video(self, story: Dict[str, Any], output_filename: str) -> str:
        scene_files = []
        scene_renderers = [
            self.render_scene1,
            self.render_scene2,
            self.render_scene3,
            self.render_scene4,
            self.render_scene5
        ]

        print("--- RENDERIZANDO VIDEO MULTIESCENA OFICIAL DE 50-60 SEG ---")

        for i in range(1, 6):
            sc_key = f"scene{i}"
            sc_data = story[sc_key]
            
            audio_path = os.path.join(self.temp_dir, f"audio_sc_{i}.mp3")
            generate_voiceover(sc_data["speech"], audio_path, voice=DEFAULT_VOICE, rate="+4%")
            dur = self._get_audio_duration(audio_path)

            frame_img = scene_renderers[i - 1](sc_data)
            frame_path = os.path.join(self.temp_dir, f"frame_sc_{i}.png")
            frame_img.convert("RGB").save(frame_path)

            clip_path = os.path.join(self.temp_dir, f"clip_sc_{i}.mp4")
            cmd = [
                FFMPEG_EXE, "-y",
                "-loop", "1",
                "-i", frame_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "-t", str(dur + 0.3),
                clip_path
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            scene_files.append(clip_path)

        concat_txt = os.path.join(self.temp_dir, "concat_list.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in scene_files:
                f.write(f"file '{os.path.abspath(c)}'\n")

        final_output_path = os.path.join(self.output_dir, output_filename)
        concat_cmd = [
            FFMPEG_EXE, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c", "copy",
            final_output_path
        ]
        subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        print(f"✅ Video oficial multiescena generado con éxito en: {final_output_path}")
        return final_output_path

if __name__ == "__main__":
    from src.script_engine.generator import ScriptEngine
    engine = ScriptEngine()
    story = engine.generate_story("evening", "Google Search Console")
    renderer = VideoRenderer()
    renderer.render_full_story_video(story, "test_full_multiscene.mp4")
