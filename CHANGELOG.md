# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Versionamiento Semántico](https://semver.org/lang/es/).

## [No publicado]

### Cambiado
- Se rediseñó completamente la interfaz gráfica del chatbot (public/chatbot.html) con diseño moderno: tipografía Inter, sistema de variables CSS, animaciones suaves, botones de acción rápida, indicador de estado en línea, diseño responsive y mejor contraste visual
- Se eliminó la persona "Carlos" del system prompt de IA y se reemplazó por un asistente técnico profesional sin nombre propio
- Se extrajo la carga de diccionarios y reglas a módulo compartido (src/services/data_loader.py) eliminando duplicación entre gemini.py y ai_agent.py
- Se corrigió requirements.txt con todas las dependencias reales del proyecto y versiones pinneadas

### Agregado
- Se creó archivo .env.example con placeholders seguros para facilitar configuración en nuevos ambientes

### Seguridad
- Se corrigió SQL Injection crítico: todas las consultas ahora usan bind variables (queries parametrizadas) en lugar de concatenación de strings
- Se agregó validación y sandbox para SQL generado por IA: allowlist de tablas, blocklist de operaciones destructivas, límite de complejidad
- Se eliminó exposición de errores internos al cliente: mensajes genéricos en respuestas HTTP, detalles solo en logs internos
- Se agregó sanitización de input del usuario: límite de longitud (2000 chars), eliminación de caracteres de control
- Se restringió CORS a orígenes configurables (variable ALLOWED_ORIGINS) en lugar de allow_origins=["*"]
- Se limitó métodos HTTP permitidos a GET y POST

### Cambiado
- Se implementó connection pooling para Oracle (min=2, max=10) eliminando el problema de agotamiento de conexiones bajo carga
- Se migró llamadas HTTP a Gemini de `requests` (síncrono/bloqueante) a `httpx` (async) para no bloquear el event loop de FastAPI
- Se agregó shutdown graceful con cierre del pool de conexiones Oracle al detener el servidor
- Se eliminó estado global mutable compartido (HISTORIAL_SESION) que causaba race conditions entre usuarios concurrentes
- Se actualizó requirements.txt con todas las dependencias reales del proyecto (langchain, chromadb, httpx, sentence-transformers)
- Se agregó validación de tamaño de payload en historial (máximo 20 items) y consulta (máximo 2000 caracteres)
- Se mejoró el prompt de IA con estructura de diagnóstico técnico (CAUSA, REGLA, SOLUCIÓN, VALIDACIÓN)
- Se migró el motor de IA de Gemini a Groq REST API (llama-3.3-70b-versatile) por cuota agotada en Gemini
- Se implementó contexto de conversación de 3 mensajes en toda la cadena (frontend → chat_directo → ai_agent → gemini)
- Se normalizó el formato del historial para aceptar tanto {role/content} del frontend como {texto} interno
- Se enriquece automáticamente el texto del usuario con identificadores del historial cuando el mensaje actual no los contiene
