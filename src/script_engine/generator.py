import random
import re
from typing import Dict, Any, List

FORBIDDEN_WORDS = [
    r"costo", r"costos", r"precio", r"precios", r"barato", r"barata", 
    r"cu[aá]nto cuesta", r"pesos", r"d[oó]lares", r"\$", r"tarifa", r"tarifas"
]

class ScriptEngine:
    """
    Generador de Guiones Multiescena (50-60 segundos) para Tracción Digital.
    Estructurado en 5 escenas dinámicas:
      1. Intro & Gancho (Badge: GRIP TE EXPLICA)
      2. Concepto Clave & Valor (Barra de URL / Píldora + Badges)
      3. Herramienta o Solución en Profundidad (con Icono)
      4. Además / 3 Funciones Clave (con Checkmarks)
      5. Outro de Contacto Oficial (WhatsApp, Redes, Web)
    """
    def __init__(self):
        # Temas de la Tarde (Educativo / Herramientas)
        self.evening_stories = [
            {
                "topic": "Dominio Propio y Google Search Console",
                "scene1": {
                    "badge": "GRIP TE EXPLICA",
                    "title": "Dominio propio y Google Search Console",
                    "speech": "¡Hola! ¿Tu negocio ya tiene su propio lugar en internet? Hoy te explico por qué necesitas un dominio propio y cómo Google te ayuda a crecer.",
                    "subtitle": "¿Tu negocio ya tiene su propio lugar en internet?"
                },
                "scene2": {
                    "title": "Tu dirección en la web",
                    "pill": "tracciondigital.com.mx",
                    "tags": ["Lleva tu nombre", "Fácil de recordar • Más confianza"],
                    "speech": "Un dominio propio lleva el nombre de tu marca, se recuerda fácil y le da muchísima más confianza a tus clientes.",
                    "subtitle": "Lleva tu nombre, se recuerda fácil y da más confianza."
                },
                "scene3": {
                    "icon": "search",
                    "title": "Google Search Console",
                    "subtitle_top": "¿Cómo te ve Google?",
                    "speech": "Pero para saber cómo te encuentran las personas y qué corregir en tu sitio, para eso está Google Search Console.",
                    "subtitle": "Para eso está Search Console: la radiografía de tu web."
                },
                "scene4": {
                    "title": "Además",
                    "features": [
                        "Páginas indexadas en Google",
                        "Mapa del sitio actualizado",
                        "Avisos automáticos de problemas"
                    ],
                    "speech": "Con esta herramienta revisas qué páginas están indexadas, envías tu mapa del sitio y recibes alertas inmediatas si algo falla.",
                    "subtitle": "Revisas indexación, envías tu sitemap y corriges errores a tiempo."
                },
                "scene5": {
                    "title": "Tracción Digital",
                    "speech": "En Tracción Digital configuramos tu web y tus herramientas para que destaques en internet. Escríbenos y con gusto te asesoramos.",
                    "subtitle": "Impulsa tu presencia en internet con Tracción Digital."
                }
            },
            {
                "topic": "¿Por qué tu negocio no aparece en Google Maps?",
                "scene1": {
                    "badge": "GRIP TE EXPLICA",
                    "title": "¿Por qué no sales en Google Maps?",
                    "speech": "¡Hola! ¿Alguna vez has buscado tu negocio en Google Maps y no aparece o está hasta el final? Te cuento el secreto.",
                    "subtitle": "¿Tu negocio aparece cuando buscan tu servicio cerca?"
                },
                "scene2": {
                    "title": "Tu Perfil de Empresa",
                    "pill": "Google Business Profile",
                    "tags": ["Visibilidad Local", "Llamadas directas a tu negocio"],
                    "speech": "El SEO local es lo que permite que clientes en tu misma ciudad o colonia te elijan a ti antes que a tu competencia.",
                    "subtitle": "El SEO local atrae a los clientes más cercanos y listos para comprar."
                },
                "scene3": {
                    "icon": "map",
                    "title": "Optimización Local",
                    "subtitle_top": "¿Qué evalúa Google?",
                    "speech": "Google premia a los negocios que tienen información verificada, horarios claros, fotos reales y reseñas activas.",
                    "subtitle": "Información verificada, fotos y reseñas definen tu ranking."
                },
                "scene4": {
                    "title": "Lo que logras",
                    "features": [
                        "Aparecer en el mapa de tu zona",
                        "Botón directo de cómo llegar y llamada",
                        "Más confianza que perfiles sin verificar"
                    ],
                    "speech": "Así multiplicas las visitas a tu local y las llamadas directas de prospectos que necesitan tus servicios hoy mismo.",
                    "subtitle": "Multiplica visitas, llamadas y clientes en tu zona."
                },
                "scene5": {
                    "title": "Tracción Digital",
                    "speech": "En Tracción Digital optimizamos tu presencia digital completa. Escríbenos y pon tu marca en el mapa.",
                    "subtitle": "Pon tu negocio en el mapa con Tracción Digital."
                }
            },
            {
                "topic": "Velocidad Web: El factor oculto de tus ventas",
                "scene1": {
                    "badge": "GRIP TE EXPLICA",
                    "title": "La velocidad de tu página web",
                    "speech": "¡Hola! ¿Sabías que si tu página web tarda más de 3 segundos en abrir, estás perdiendo más de la mitad de tus prospectos?",
                    "subtitle": "Si tu web es lenta, tus clientes se van con la competencia."
                },
                "scene2": {
                    "title": "Experiencia Móvil",
                    "pill": "Carga en menos de 2 segundos",
                    "tags": ["Optimización Móvil", "Retención de clientes"],
                    "speech": "La mayoría entra desde su celular con datos móviles. Si la pantalla se queda en blanco, cierran la pestaña y no regresan.",
                    "subtitle": "Tus visitantes no esperan: exigen rapidez inmediata en su celular."
                },
                "scene3": {
                    "icon": "speed",
                    "title": "Google PageSpeed",
                    "subtitle_top": "¿Cómo califica Google tu web?",
                    "speech": "Google premia a las páginas ultrarrápidas dándoles mejores posiciones de búsqueda y menor costo en tus visitas.",
                    "subtitle": "Google premia la velocidad y te posiciona más arriba."
                },
                "scene4": {
                    "title": "Claves de velocidad",
                    "features": [
                        "Imágenes comprimidas en nueva generación",
                        "Código limpio sin plugins innecesarios",
                        "Servidores rápidos y seguros"
                    ],
                    "speech": "Con una arquitectura optimizada y código limpio garantizas que cada visita tenga una experiencia impecable y fluida.",
                    "subtitle": "Código limpio, imágenes ligeras y respuesta instantánea."
                },
                "scene5": {
                    "title": "Tracción Digital",
                    "speech": "En Tracción Digital construimos páginas web a la medida, veloces y listas para convertir. Visítanos en tracciondigital.com.mx.",
                    "subtitle": "Diseño web veloz y a medida en tracciondigital.com.mx."
                }
            }
        ]

        # Temas de la Mañana (Conversión / Tracción Digital PyME)
        self.morning_stories = [
            {
                "topic": "Reemplaza el desorden de Excel con un Sistema Web",
                "scene1": {
                    "badge": "TRACCIÓN DIGITAL",
                    "title": "Dile adiós al caos de Excel",
                    "speech": "¡Hola! ¿Tu empresa sigue operando con hojas de Excel gigantescas que se traban, se pierden o tienen errores de fórmulas?",
                    "subtitle": "¿Tu operación sigue dependiendo de archivos de Excel gigantes?"
                },
                "scene2": {
                    "title": "Tu Propio Sistema Web",
                    "pill": "app.tracciondigital.com.mx",
                    "tags": ["Acceso desde cualquier celular", "Cero fórmulas rotas"],
                    "speech": "Tener tus cotizaciones, clientes e inventario en un sistema web personalizado te ahorra horas de trabajo cada semana.",
                    "subtitle": "Cotizaciones, clientes e inventario en un solo lugar seguro."
                },
                "scene3": {
                    "icon": "app",
                    "title": "Software a la Medida",
                    "subtitle_top": "Adaptado exactamente a tu negocio",
                    "speech": "No te adaptes a programas complicados y caros: creamos la herramienta exacta que tu equipo necesita para trabajar mejor.",
                    "subtitle": "Un sistema hecho a tu medida exacta, sin complicaciones."
                },
                "scene4": {
                    "title": "Beneficios reales",
                    "features": [
                        "Cotizaciones automáticas en PDF",
                        "Control de inventario en tiempo real",
                        "Acceso seguro para todo tu equipo"
                    ],
                    "speech": "Generas cotizaciones automáticas, consultas tus datos en tiempo real y tienes control total de tu negocio desde cualquier lugar.",
                    "subtitle": "Automatiza tareas repetitivas y controla tu negocio en tiempo real."
                },
                "scene5": {
                    "title": "Tracción Digital",
                    "speech": "Moderniza tu negocio hoy mismo. Escríbenos por WhatsApp o entra a tracciondigital.com.mx para una asesoría.",
                    "subtitle": "Moderniza tu operación con Tracción Digital."
                }
            },
            {
                "topic": "Landing Page vs Sitio Web: ¿Cuál necesita tu negocio?",
                "scene1": {
                    "badge": "TRACCIÓN DIGITAL",
                    "title": "¿Landing Page o Sitio Web?",
                    "speech": "¡Hola! Muchos confunden una landing page con un sitio web completo y por eso sus campañas de publicidad no funcionan. Aquí te lo explico.",
                    "subtitle": "¿Confundido entre una Landing Page y un Sitio Web?"
                },
                "scene2": {
                    "title": "El Sitio Institucional",
                    "pill": "tracciondigital.com.mx",
                    "tags": ["Presentación Completa", "Catálogo y Servicios"],
                    "speech": "Un sitio web es tu oficina digital completa: habla de tu historia, tus servicios, tus casos de éxito y genera confianza a largo plazo.",
                    "subtitle": "Tu oficina digital con toda la información de tu marca."
                },
                "scene3": {
                    "icon": "target",
                    "title": "La Landing Page",
                    "subtitle_top": "Enfocada en 1 sola acción",
                    "speech": "Una landing page, en cambio, tiene una sola meta: que la persona presione un botón y te mande mensaje o te compre de inmediato.",
                    "subtitle": "Diseñada con un solo objetivo: convertir visitas en prospectos."
                },
                "scene4": {
                    "title": "La estrategia ideal",
                    "features": [
                        "Sitio web para posicionar tu marca",
                        "Landing page para tus anuncios en redes",
                        "Ambos conectados directo a tu WhatsApp"
                    ],
                    "speech": "El secreto está en combinar ambas: tu sitio para posicionarte y landing pages estratégicas para tus campañas publicitarias.",
                    "subtitle": "La combinación perfecta para posicionar y captar clientes."
                },
                "scene5": {
                    "title": "Tracción Digital",
                    "speech": "En Tracción Digital diseñamos soluciones digitales que sí dan resultados. Conéctate con nosotros en tracciondigital.com.mx.",
                    "subtitle": "Soluciones web de alto impacto en tracciondigital.com.mx."
                }
            }
        ]

    def validate_script_rules(self, text: str) -> bool:
        for pattern in FORBIDDEN_WORDS:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True

    def generate_story(self, slot: str = "evening", custom_topic: str = None) -> Dict[str, Any]:
        pool = self.evening_stories if slot == "evening" else self.morning_stories
        chosen = random.choice(pool)

        if custom_topic:
            for s in (self.evening_stories + self.morning_stories):
                if any(w.lower() in s["topic"].lower() for w in custom_topic.split() if len(w) > 4):
                    chosen = s
                    break

        full_text = " ".join([chosen[f"scene{i}"]["speech"] for i in range(1, 6)])
        if not self.validate_script_rules(full_text):
            raise ValueError("El guión contiene términos prohibidos de costos/precios.")

        return chosen

    def generate_script(self, slot: str = "evening", custom_topic: str = None) -> Dict[str, Any]:
        story = self.generate_story(slot=slot, custom_topic=custom_topic)
        return {
            "topic": story["topic"],
            "hook": story["scene1"]["title"],
            "full_speech": " ".join([story[f"scene{i}"]["speech"] for i in range(1, 6)]),
            "story": story
        }
