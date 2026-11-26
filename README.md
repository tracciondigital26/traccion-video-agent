# 🚀 Agente Autónomo de Video - Tracción Digital

Sistema de generación, optimización y publicación automática de video contenido vertical (9:16) para TikTok, Instagram Reels y Facebook.

---

## 🎯 Objetivos y Reglas de Negocio

1. **Promoción de Tracción Digital (`tracciondigital.com.mx`):**
   - Sitios web institucionales, landing pages de alta conversión, aplicaciones a la medida (reemplazo de hojas de Excel desordenadas) y soporte digital.
2. **Estrategia Diaria en Dos Turnos:**
   - **Mañana (08:30 AM) - Conversión:** Enfocado en los dolores de PyMEs y profesionistas (pérdida de clientes por no tener web, lentitud, desorden operativo). CTA a `tracciondigital.com.mx`.
   - **Tarde (06:30 PM) - Educación de Alto Valor:** Guías rápidas y explicaciones técnicas sencillas (Google Search Console, SEO local, métricas, rendimiento web).
3. **Estilos Visuales Alternados:**
   - **Día A:** B-Roll dinámico tecnológico (pantallas, código, clips modernos, títulos gigantes y subtítulos animados).
   - **Día B:** Presentado por **Grip** (la mascota oficial de Tracción Digital), interactuando con elementos en pantalla.
4. **Voz:** Femenina, dulce, natural y llamativa (100% gratuita con síntesis neuronal `es-MX-DaliaNeural`).
5. **Regla Inquebrantable:** 🚫 **CERO mención de costos, precios o tarifas.**
6. **Bucle de Aprendizaje y Espionaje:**
   - Analiza tendencias y competidores virales del sector marketing/web en México y Latinoamérica.
   - Evalúa el desempeño (retención, likes, compartidos) y ajusta los ganchos automáticamente para replicar lo que funciona.

---

## 🏗️ Arquitectura de Carpetas

```
Agentevideo/
├── assets/
│   ├── broll/       # Videos de stock y clips de fondo
│   ├── fonts/       # Fuentes tipográficas virales (ej. Montserrat, Arial Black)
│   ├── grip/        # Ilustraciones y poses de Grip (la mascota)
│   └── music/       # Pistas de fondo en volumen bajo (sin copyright)
├── data/
│   └── metrics.db   # Base de datos SQLite con el historial de rendimiento de videos
├── output/
│   ├── scripts/     # Guiones generados
│   └── videos/      # Videos 1080x1920 listos para publicación
├── src/
│   ├── analytics/   # Motor de métricas y optimización continua
│   ├── publisher/   # Programador y publicador para TikTok / Meta
│   ├── script_engine/ # Generador de guiones (Mañana vs Tarde)
│   ├── trend_radar/ # Scraper de tendencias virales y competidores
│   ├── video_engine/# Ensamblador de video (Modo B-roll y Modo Grip)
│   └── voice_engine/# Síntesis de voz femenina con Edge-TTS
├── requirements.txt
└── .env.example
```
