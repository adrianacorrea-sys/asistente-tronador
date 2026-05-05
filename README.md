# Asistente Técnico Tronador

Sistema de soporte técnico inteligente para el sistema **Tronador** de Seguros Bolívar. Integra consultas a Oracle, búsqueda en Jira/GitHub y análisis con IA (Gemini) para diagnosticar errores y guiar la resolución de incidentes.

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (HTML)                    │
│              public/chatbot.html                     │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP POST /consultar-con-clarificacion
┌──────────────────────▼──────────────────────────────┐
│                FastAPI (src/main.py)                 │
│         Validación · CORS · Error Handling          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│           Chat Directo (Orquestador)                │
│     Clasificación de intención · Enrutamiento       │
└───────┬──────────────┬──────────────┬───────────────┘
        │              │              │
┌───────▼───────┐ ┌────▼────┐ ┌──────▼──────┐
│  AI Agent     │ │ Gemini  │ │  Oracle DB  │
│ SQL Generator │ │ REST API│ │ OPS$PUMA    │
└───────────────┘ └─────────┘ └─────────────┘
```

## Características

- **Diagnóstico inteligente**: Analiza errores con contexto de tablas, reglas de negocio y conocimiento histórico
- **Generación SQL segura**: Queries parametrizadas con allowlist de tablas y blocklist de operaciones destructivas
- **Clasificación de intención**: Filtra consultas fuera de dominio y detecta identificadores técnicos
- **Base de conocimiento**: Embeddings con ChromaDB para enriquecer respuestas con documentación interna
- **Memoria conversacional**: Mantiene contexto de la conversación (últimos 6 mensajes)
- **Interfaz corporativa**: UI responsive con identidad visual de Seguros Bolívar

## Requisitos

- Python 3.12+
- Acceso a Oracle (Tronador - esquema OPS$PUMA)
- API Key de Google Gemini
- Conexión a red corporativa (VPN si aplica)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-org/pb3Graf.git
cd pb3Graf

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Copiar el archivo de ejemplo y completar con credenciales reales:

```bash
copy .env.example .env
```

Variables requeridas:

| Variable | Descripción |
|----------|-------------|
| `ORACLE_USER` | Usuario de Oracle (Tronador) |
| `ORACLE_PASSWORD` | Contraseña de Oracle |
| `ORACLE_HOST` | Host del servidor Oracle |
| `ORACLE_PORT` | Puerto (default: 1521) |
| `ORACLE_SERVICE_NAME` | Nombre del servicio Oracle |
| `GEMINI_API_KEY` | API Key de Google Gemini |
| `JIRA_EMAIL` | Email para autenticación en Jira |
| `JIRA_API_TOKEN` | Token de API de Jira |
| `JIRA_BASE_URL` | URL base de Jira |
| `GITHUB_TOKEN` | Token de acceso a GitHub |
| `GITHUB_REPO` | Repositorio de GitHub (org/repo) |
| `ALLOWED_ORIGINS` | Orígenes CORS permitidos |

## Ejecución

```bash
python src/main.py
```

El servidor se inicia en `http://localhost:8000`

## Estructura del Proyecto

```
pb3Graf/
├── public/
│   └── chatbot.html            # Interfaz del chat
├── src/
│   ├── main.py                 # Entry point FastAPI
│   ├── db/
│   │   └── oracle.py           # Connection pool + queries parametrizadas
│   ├── services/
│   │   ├── ai_agent.py         # Generación SQL + procesamiento de casos
│   │   ├── chat_directo.py     # Orquestador de flujo conversacional
│   │   ├── data_loader.py      # Carga centralizada de diccionarios/reglas
│   │   ├── gemini.py           # Integración con Gemini REST API
│   │   ├── github.py           # Búsqueda de soluciones en GitHub
│   │   ├── intent_validator.py # Clasificación de intención
│   │   └── jira.py             # Integración con Jira
│   └── knowledge/
│       └── trainer.py          # Entrenamiento de base de conocimiento
├── conocimiento/               # Documentos SQL y técnicos para RAG
├── .env.example                # Template de variables de entorno
├── requirements.txt            # Dependencias Python
├── CHANGELOG.md                # Historial de cambios
└── README.md                   # Este archivo
```

## Seguridad

- Queries parametrizadas (bind variables) — prevención de SQL injection
- Allowlist de tablas permitidas para consultas
- Blocklist de operaciones destructivas (INSERT, UPDATE, DELETE, DROP)
- Sanitización de input del usuario (longitud máxima, caracteres de control)
- CORS restringido a orígenes configurados
- Errores genéricos al cliente, detalles solo en logs internos
- Validación de SQL generado por IA antes de ejecución

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Interfaz del chatbot |
| GET | `/health` | Health check |
| POST | `/consultar` | Consulta directa sin historial |
| POST | `/consultar-con-clarificacion` | Consulta con memoria conversacional |

## Tecnologías

| Componente | Tecnología |
|------------|-----------|
| Backend | Python 3.12 + FastAPI |
| Base de datos | Oracle (OPS$PUMA) |
| IA | Google Gemini 2.5 Flash |
| Embeddings | ChromaDB + sentence-transformers |
| Frontend | HTML5 + CSS3 + JavaScript (vanilla) |
| HTTP Async | httpx |

## Autores

- Adriana Correa — Desarrollo e integración

## Licencia

Uso interno — Seguros Bolívar
