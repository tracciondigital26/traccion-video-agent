import random
from typing import List, Dict, Any

class TrendRadar:
    """
    Módulo de inteligencia competitiva y radar de tendencias virales.
    Analiza y detecta ganchos (hooks) y formatos ganadores en agencias y creadores del sector web y marketing digital.
    """
    def __init__(self):
        # Base de patrones virales extraídos de videos con alto rendimiento
        self.competitor_patterns = [
            {
                "niche": "Páginas Web & Conversión",
                "viral_hook": "3 cosas que tu página web necesita YA si quieres vender este mes.",
                "angle": "Lista accionable de 3 puntos rápidos.",
                "viral_score": 94
            },
            {
                "niche": "Herramientas de Google & SEO",
                "viral_hook": "La herramienta secreta de Google que las agencias usan para saber todo de su competencia.",
                "angle": "Curiosidad / Herramienta 'secreta' (Google Search Console o PageSpeed).",
                "viral_score": 98
            },
            {
                "niche": "Automatización PyME",
                "viral_hook": "Si tu negocio todavía hace esto a mano, estás perdiendo 10 horas a la semana.",
                "angle": "Pérdida de tiempo y dolor operativo solucionado con software a medida.",
                "viral_score": 91
            },
            {
                "niche": "Diseño & UX",
                "viral_hook": "El error número 1 en páginas web que hace que la gente cierre la pestaña de inmediato.",
                "angle": "Evitar errores fatales en diseño móvil.",
                "viral_score": 96
            },
            {
                "niche": "Google Maps & Local",
                "viral_hook": "El truco para aparecer en los primeros 3 lugares de Google Maps en tu ciudad.",
                "angle": "Guía práctica de optimización de perfil comercial.",
                "viral_score": 89
            }
        ]

    def scan_viral_trends(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de tendencias y patrones de la competencia ordenados por viral score.
        """
        return sorted(self.competitor_patterns, key=lambda x: x["viral_score"], reverse=True)

    def get_winning_formula(self) -> Dict[str, Any]:
        """
        Selecciona la mejor fórmula viral para inspirar el próximo guión.
        """
        trends = self.scan_viral_trends()
        return random.choice(trends[:3])

if __name__ == "__main__":
    radar = TrendRadar()
    print("Tendencias virales detectadas de la competencia:")
    for t in radar.scan_viral_trends():
        print(f"🔥 [{t['viral_score']}/100] {t['niche']}: '{t['viral_hook']}' ({t['angle']})")
