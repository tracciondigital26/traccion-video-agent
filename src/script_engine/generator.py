import random
import re
from typing import Dict, Any, List

# Lista de palabras prohibidas bajo la regla inquebrantable
FORBIDDEN_WORDS = [
    r"costo", r"costos", r"precio", r"precios", r"barato", r"barata", 
    r"cu[aá]nto cuesta", r"pesos", r"d[oó]lares", r"\$", r"tarifa", r"tarifas"
]

class ScriptEngine:
    def __init__(self, brand_name: str = "Tracción Digital", website: str = "tracciondigital.com.mx"):
        self.brand_name = brand_name
        self.website = website
        
        # Plantillas de temas para la Mañana (Promoción, Conversión, Soluciones PyME)
        self.morning_topics = [
            {
                "topic": "Páginas Web Lentas que Pierden Clientes",
                "hook": "¿Sabías que si tu página web tarda más de 3 segundos en cargar, el 50% de tus clientes se van con tu competencia?",
                "problem": "La mayoría de las páginas hechas al aventón están llenas de código pesado y plugins lentos que solo asustan a quien entra.",
                "solution": "En Tracción Digital diseñamos sitios web optimizados, ultra veloces y pensados exactamente para convertir visitas en prospectos calificados directo a tu WhatsApp.",
                "cta": "Deja de perder clientes por una web rota. Visita tracciondigital.com.mx y dale a tu negocio el impulso digital que merece."
            },
            {
                "topic": "Sustituir Excel con una Aplicación a Medida",
                "hook": "¿Tu negocio sigue dependiendo de un archivo de Excel gigante que se congela todo el tiempo?",
                "problem": "Tener tus cotizaciones, inventario y clientes en hojas de cálculo regadas es la forma más fácil de cometer errores y perder dinero.",
                "solution": "En Tracción Digital desarrollamos sistemas web internos y cotizadores personalizados, diseñados a la medida exacta de tu flujo de trabajo.",
                "cta": "Automatiza tu operación y dile adiós al caos. Entra a tracciondigital.com.mx y descubre lo fácil que es modernizarte."
            },
            {
                "topic": "Depender únicamente de Recomendaciones de Boca en Boca",
                "hook": "Depender únicamente de que te recomienden de boca en boca es el mayor riesgo para tu empresa.",
                "problem": "El boca a boca es excelente, pero ¿qué pasa en las semanas donde nadie recomienda a nadie? Tu flujo de clientes se detiene.",
                "solution": "Con el paquete de Arranque Digital de Tracción Digital, unificamos tu página web, tu perfil de Google y tus redes para que te encuentren todos los días sin parar.",
                "cta": "Pon a trabajar internet a favor de tu marca. Conoce nuestras soluciones en tracciondigital.com.mx."
            },
            {
                "topic": "Landing Pages que sí Venden",
                "hook": "¿Lanzas publicidad en redes pero nadie te contacta? El problema no es tu anuncio, es a dónde los mandas.",
                "problem": "Mandar a tus prospectos a una página confusa o sin llamado claro a la acción es tirar tu esfuerzo a la basura.",
                "solution": "Creamos landing pages de alto impacto, enfocadas en un solo objetivo: que el usuario presione un botón y te mande mensaje.",
                "cta": "Empieza a captar clientes de verdad. Conecta con nosotros en tracciondigital.com.mx."
            }
        ]

        # Plantillas de temas para la Tarde (Educativo, Herramientas, SEO, Google Search Console)
        self.evening_topics = [
            {
                "topic": "Para qué sirve Google Search Console",
                "hook": "Si tienes una página web y no usas Google Search Console, estás navegando a ciegas en internet.",
                "problem": "Muchos piensan que con subir su web ya van a aparecer en Google, pero la realidad es que Google ni siquiera sabe que existes si no se lo notificas.",
                "solution": "Google Search Console es la herramienta gratuita de Google que te dice exactamente con qué palabras te buscan, en qué posición estás y si tu web tiene errores de rastreo. Es como una radiografía en tiempo real de tu visibilidad.",
                "cta": "¿Quieres que tu página domine los primeros lugares de Google? Síguenos para más consejos y visita tracciondigital.com.mx."
            },
            {
                "topic": "Qué es el SEO Local y Google Business Profile",
                "hook": "¿Por qué tu competencia aparece primero cuando alguien busca tu servicio en Google Maps?",
                "problem": "No es suerte ni magia: tienen su ficha de Google optimizada y tú probablemente la tienes abandonada o sin verificar.",
                "solution": "El SEO local ayuda a que las personas en tu misma ciudad o zona encuentren tu negocio cuando necesitan una solución urgente.",
                "cta": "Aprende a posicionar tu marca en tu localidad. Síguenos y conoce más trucos en tracciondigital.com.mx."
            },
            {
                "topic": "Diferencia entre Landing Page y Sitio Web",
                "hook": "¿Confundido entre una Landing Page y un Sitio Web completo? Aquí te lo explico en 30 segundos.",
                "problem": "Usar la herramienta equivocada hace que tus campañas publicitarias no funcionen como esperabas.",
                "solution": "Un sitio web es como tu oficina digital con varias salas: catálogo, misión, blog. Una landing page es una puerta única diseñada para un solo propósito: que te dejen sus datos o te compren de inmediato.",
                "cta": "¿Cuál necesita tu negocio hoy? Déjanos un comentario o visítanos en tracciondigital.com.mx."
            },
            {
                "topic": "Por qué la velocidad de tu web define tu éxito",
                "hook": "Cada segundo que tarda en abrir tu sitio web reduce un 20% tu tasa de conversión.",
                "problem": "Imágenes sin comprimir, servidores obsoletos y scripts pesados hacen que tu visitante se desespere antes de ver tu producto.",
                "solution": "Optimizar los tiempos de respuesta y usar tecnologías modernas garantiza que tu usuario tenga una experiencia fluida e inmediata.",
                "cta": "Pon a prueba tu web y acelera tu crecimiento digital con nosotros en tracciondigital.com.mx."
            }
        ]

    def validate_script_rules(self, text: str) -> bool:
        """Verifica que el guión no contenga ninguna mención de costos o precios."""
        for pattern in FORBIDDEN_WORDS:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True

    def generate_script(self, slot: str = "morning", custom_topic: str = None) -> Dict[str, Any]:
        """
        Genera un guión estructurado.
        slot: 'morning' (conversión) o 'evening' (educativo)
        """
        topic_pool = self.morning_topics if slot == "morning" else self.evening_topics
        chosen = random.choice(topic_pool)

        # Si viene un tema personalizado de tendencia/competencia
        if custom_topic:
            chosen_topic = custom_topic
        else:
            chosen_topic = chosen["topic"]

        hook = chosen["hook"]
        problem = chosen["problem"]
        solution = chosen["solution"]
        cta = chosen["cta"]

        full_speech = f"{hook} {problem} {solution} {cta}"

        # Validación estricta
        if not self.validate_script_rules(full_speech):
            raise ValueError("El guión generado violó la regla de no mencionar costos o precios.")

        return {
            "slot": slot,
            "topic": chosen_topic,
            "hook": hook,
            "problem": problem,
            "solution": solution,
            "cta": cta,
            "full_speech": full_speech,
            "character": "Grip" if random.choice([True, False]) else "B-Roll Tech"
        }

if __name__ == "__main__":
    engine = ScriptEngine()
    print("--- GUION MAÑANA (Conversión) ---")
    m_script = engine.generate_script("morning")
    print(f"Tema: {m_script['topic']}")
    print(f"Estilo: {m_script['character']}")
    print(f"Texto completo:\n{m_script['full_speech']}\n")

    print("--- GUION TARDE (Educativo - ej. Google Search Console) ---")
    e_script = engine.generate_script("evening")
    print(f"Tema: {e_script['topic']}")
    print(f"Estilo: {e_script['character']}")
    print(f"Texto completo:\n{e_script['full_speech']}")
