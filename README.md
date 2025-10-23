# RAG App - Chatbot Inteligente 100% Gratuito 🤖

Un sistema completo de **Retrieval-Augmented Generation (RAG)** que permite consultar documentos PDF utilizando inteligencia artificial **completamente gratis**. Este proyecto utiliza **Groq** (LLM gratuito) y **HuggingFace** (embeddings locales gratuitos) para crear un asistente conversacional que responde preguntas basándose en tus documentos.

## ✨ Características Principales

- 🆓 **100% Gratuito** - Sin costos de API (Groq + HuggingFace)
- 🌐 **Interfaz Web Moderna** - App web con Streamlit (además de CLI)
- 💬 **Chat Interactivo** - Haz múltiples preguntas en una sesión
- 📄 **Citación de Fuentes** - Muestra páginas exactas y relevancia porcentual
- 🔒 **Privacidad** - Embeddings locales, tus documentos no salen de tu PC
- ⚡ **Rápido** - Groq ofrece una de las inferencias más rápidas del mercado
- 🎯 **Preciso** - Respuestas basadas SOLO en tus documentos
- ⚙️ **Configurable** - Ajusta modelo, temperatura y fuentes desde la interfaz

## 🆕 Novedades en esta Versión

### Migración Completa a Stack Gratuito
- ❌ **Eliminado**: OpenAI (embeddings + LLM de pago)
- ✅ **Agregado**: Groq (LLM gratuito con llama-3.3-70b)
- ✅ **Agregado**: HuggingFace (embeddings locales con all-MiniLM-L6-v2)

### Chat Interactivo
- Interfaz conversacional en terminal
- Historial de preguntas en una sola sesión
- Comandos de salida: `exit`, `quit`, `salir`, `q`

### Transparencia de Fuentes
```
📚 Information retrieved from:
  📄 Tu_Documento.pdf - Page 23 (85.2% relevance to your question)
  📄 Tu_Documento.pdf - Page 45 (78.6% relevance to your question)
  📄 Tu_Documento.pdf - Page 67 (72.3% relevance to your question)
```

## ¿Qué es RAG?

**Retrieval-Augmented Generation** es una técnica que mejora las respuestas de los modelos de lenguaje (LLMs) al combinar su conocimiento interno con información extraída de documentos externos. En lugar de depender únicamente del conocimiento con el que fue entrenado el modelo, RAG permite:

- ✅ Acceder a información actualizada y específica de tu dominio
- ✅ Generar respuestas basadas en documentos internos (políticas, manuales, reportes, etc.)
- ✅ Reducir alucinaciones al fundamentar las respuestas en datos reales
- ✅ Crear asistentes especializados sin necesidad de reentrenar modelos

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLUJO DE DATOS RAG                          │
└─────────────────────────────────────────────────────────────────┘

1. PROCESAMIENTO DE DOCUMENTOS (Offline)
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │   PDFs en    │ ──>  │ file_processor  │ ──>  │   Chunks     │
   │  /documents  │      │    .chunk_pdfs()│      │  (fragmentos)│
   └──────────────┘      └─────────────────┘      └──────────────┘
                                                           │
                                                           ▼
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │ Base de datos│ <──  │   chroma_db     │ <──  │ HuggingFace  │
   │  vectorial   │      │.save_to_chroma()│      │  Embeddings  │
   │  (ChromaDB)  │      └─────────────────┘      │   (LOCAL)    │
   └──────────────┘                                └──────────────┘

2. CONSULTA Y GENERACIÓN (Runtime)
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │   Usuario    │ ──>  │    Búsqueda     │ ──>  │  Documentos  │
   │   pregunta   │      │   semántica     │      │  relevantes  │
   │              │      │  (ChromaDB)     │      │  + páginas   │
   └──────────────┘      └─────────────────┘      └──────────────┘
                                                           │
                                                           ▼
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │   Respuesta  │ <──  │   Groq LLM      │ <──  │   Prompt     │
   │  + Fuentes   │      │  (llama-3.3)    │      │ + Contexto   │
   └──────────────┘      └─────────────────┘      └──────────────┘
```

## 📁 Estructura del Proyecto

```
RAG-app-python/
├── main.py                 # Chat interactivo con RAG
├── .env.example            # Template para configuración
├── .env                    # Tu API key (NO se sube a GitHub)
├── src/
│   ├── file_processor.py   # Procesamiento y chunking de PDFs
│   └── chroma_db.py        # Gestión de la base de datos vectorial
├── documents/              # 📁 Coloca tus PDFs aquí
├── chroma/                 # Base de datos vectorial (se genera automáticamente)
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- Cuenta gratuita en Groq ([console.groq.com](https://console.groq.com/))

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/francoSW99/RAG-app-python.git
   cd RAG-app-python
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar API Key de Groq (Gratis)**

   a. Obtén tu API key gratuita en: [https://console.groq.com/](https://console.groq.com/)

   b. Copia el archivo de configuración:
   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```

   c. Edita `.env` y agrega tu API key:
   ```
   GROQ_API_KEY=gsk_tu_api_key_aqui
   ```

5. **Agregar tus documentos PDF**
   ```bash
   # Copia tus archivos PDF a la carpeta documents/
   ```

6. **Ejecutar el chatbot**

   **Opción A: Interfaz Web (Recomendado)**
   ```bash
   streamlit run app.py
   ```
   Se abrirá automáticamente en tu navegador en `http://localhost:8501`

   **Opción B: Interfaz de Terminal**
   ```bash
   python main.py
   ```

## 💬 Interfaces Disponibles

### 🌐 Interfaz Web (Streamlit) - **Recomendado**

La forma más fácil e intuitiva de usar el chatbot:

```bash
streamlit run app.py
```

**Características de la interfaz web:**
- 🎨 Diseño moderno y responsive
- ⚙️ Configuración interactiva (modelo, temperatura, fuentes)
- 💬 Chat con historial visual
- 📊 Gráficos de relevancia expandibles
- 🔄 Fácil reinicio y ajuste de parámetros
- 📱 Funciona en cualquier dispositivo con navegador

![Streamlit Interface](https://via.placeholder.com/800x400?text=Streamlit+RAG+Interface)

### 💻 Interfaz de Terminal (CLI)

Para usuarios que prefieren la línea de comandos:

```bash
python main.py
```

**Ejemplo de uso:**
```
================================================================================
RAG CHATBOT - Powered by Groq + HuggingFace (100% FREE)
================================================================================
Documents loaded: 45 chunks
Type 'exit', 'quit', or 'salir' to end the conversation
================================================================================

Your question: ¿Cuáles son las técnicas principales del libro?

Thinking...

Answer:
Basado en el contexto proporcionado, las técnicas principales incluyen:

1. **La Ley de Pareto (80/20)**: Enfócate en el 20% de tareas que generan el
   80% de resultados.

2. **Método ABCDE**: Categoriza tareas por prioridad - A (críticas), B (importantes),
   C (opcionales), D (delegar), E (eliminar).

3. **Comer la Rana**: Realiza tu tarea más difícil primero cada mañana.

Source: Administración del tiempo - Tracy Brayan.pdf

📚 Information retrieved from:
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 23 (89.5% relevance to your question)
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 45 (82.1% relevance to your question)
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 67 (75.8% relevance to your question)

================================================================================
```

📖 **[Ver guía completa de Streamlit](STREAMLIT_GUIDE.md)**

## ⚙️ Personalización

### Cambiar el número de fuentes consultadas

Modifica `k` en `main.py` (línea 79):
```python
docs = db.similarity_search_with_score(query, k=5)  # Consulta 5 chunks
```

### Cambiar el modelo de Groq

Modifica en `main.py` (línea 32):
```python
model = ChatGroq(
    model="llama-3.1-70b-versatile",  # Otros: llama-3.1-8b-instant, gemma2-9b-it
    temperature=0,
)
```

Modelos disponibles en Groq (todos gratuitos):
- `llama-3.3-70b-versatile` - **Recomendado**, mejor calidad y más reciente
- `llama-3.1-70b-versatile` - Excelente calidad, muy confiable
- `llama-3.1-8b-instant` - Más rápido, ideal para prototipos
- `gemma2-9b-it` - Compacto y eficiente

### Cambiar tamaño de chunks

Edita `src/file_processor.py` (líneas 14-16):
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Chunks más grandes (más contexto)
    chunk_overlap=200,  # Mayor overlap
    length_function=len,
    add_start_index=True,
)
```

### Usar modelo de embeddings diferente

Modifica en `main.py` (línea 20):
```python
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # Mejor para español
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

## 🔧 Dependencias Principales

### Stack Gratuito
- **groq** - API gratuita para LLM (llama-3.3-70b)
- **langchain-groq** - Integración de Groq con LangChain
- **sentence-transformers** - Embeddings locales gratuitos
- **langchain-huggingface** - Integración de HuggingFace con LangChain

### Core
- **langchain** - Framework para aplicaciones con LLMs
- **chromadb** - Base de datos vectorial local
- **pypdf** - Lector de archivos PDF
- **python-dotenv** - Manejo seguro de variables de entorno

## 📊 Comparación con Versión Anterior

| Característica | Versión Anterior (OpenAI) | Versión Actual (Groq + HF) |
|----------------|---------------------------|----------------------------|
| **Costo LLM** | $0.002 por 1K tokens | 🆓 **Gratis** |
| **Costo Embeddings** | $0.13 por 1M tokens | 🆓 **Gratis** |
| **Privacidad Embeddings** | Datos enviados a OpenAI | ✅ **100% Local** |
| **Interfaz** | Un query y termina | ✅ **Chat Interactivo** |
| **Fuentes** | No mostraba | ✅ **Páginas + %** |
| **Velocidad** | Rápido | ⚡ **Muy rápido** |
| **Internet** | Siempre requerido | Solo LLM (embeddings offline) |

## 🔐 Seguridad

- ✅ API keys en archivo `.env` (no se sube a GitHub)
- ✅ `.env` incluido en `.gitignore`
- ✅ Template `.env.example` para setup
- ✅ Validación de API key al inicio
- ✅ Mensajes de error claros si falta configuración

## ❓ FAQ

### ¿Es realmente gratis?
Sí, Groq ofrece API gratuita con límites generosos. HuggingFace ejecuta localmente, sin costos.

### ¿Qué tan rápido es Groq?
Groq es uno de los LLMs más rápidos disponibles, ~10x más rápido que GPT-4 en muchos casos.

### ¿Funciona offline?
Los embeddings funcionan offline después de la primera descarga. El LLM (Groq) requiere internet.

### ¿Puedo usar mis propios PDFs?
Sí, solo colócalos en la carpeta `documents/` y ejecuta el programa.

### ¿Qué idiomas soporta?
El sistema soporta múltiples idiomas. Para mejor rendimiento en español, usa el embedding `paraphrase-multilingual-MiniLM-L12-v2`.

### ¿Cuántos documentos puedo procesar?
Depende de tu RAM. El modelo de embeddings es ligero (~90MB). Puedes procesar cientos de PDFs.

## 🎯 Casos de Uso

- 📚 **Asistente de estudio** - Pregunta sobre libros y apuntes
- 🏢 **Documentación interna** - Consulta manuales de empresa
- ⚖️ **Análisis legal** - Busca en contratos y regulaciones
- 🔬 **Investigación** - Consulta papers académicos
- 📖 **Análisis de libros** - Extrae insights de libros técnicos

## 🚧 Limitaciones Conocidas

- La base de datos ChromaDB se recrea en cada ejecución (fácil de hacer persistente)
- Solo soporta archivos PDF (fácil agregar DOCX, TXT, etc.)
- El LLM requiere conexión a internet
- Límites de rate de Groq (generosos pero existen)

## 🛣️ Roadmap

- [x] Interfaz web con Streamlit ✅
- [ ] Persistencia de ChromaDB entre ejecuciones
- [ ] Soporte para DOCX, TXT, Markdown
- [ ] Sistema de caché para reducir llamadas a Groq
- [ ] Modo multimodal (imágenes en PDFs)
- [ ] Exportar conversaciones
- [ ] Métricas de calidad de respuestas
- [ ] Upload de PDFs desde la interfaz web
- [ ] Autenticación para deployments públicos

## 📚 Recursos

- [Documentación de Groq](https://console.groq.com/docs)
- [Documentación de LangChain](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

Franco SW - [@francoSW99](https://github.com/francoSW99)

## 🙏 Agradecimientos

- Groq por proporcionar API gratuita de LLM
- HuggingFace por modelos de embeddings gratuitos
- LangChain por el excelente framework
- ChromaDB por la base de datos vectorial

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!

**Nota**: Este es un proyecto educativo. Para uso en producción, considera implementar manejo de errores robusto, logging, monitoreo, y medidas de seguridad adicionales.
