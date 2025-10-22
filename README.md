# RAG App - Retrieval-Augmented Generation with OpenAI

Un sistema completo de **Retrieval-Augmented Generation (RAG)** que permite consultar documentos PDF utilizando inteligencia artificial. Este proyecto demuestra cómo integrar búsqueda semántica con modelos de lenguaje para generar respuestas contextualizadas basadas en documentos específicos.

## ¿Qué es RAG?

**Retrieval-Augmented Generation** es una técnica que mejora las respuestas de los modelos de lenguaje (LLMs) al combinar su conocimiento interno con información extraída de documentos externos. En lugar de depender únicamente del conocimiento con el que fue entrenado el modelo, RAG permite:

- Acceder a información actualizada y específica de tu dominio
- Generar respuestas basadas en documentos internos (políticas, manuales, reportes, etc.)
- Reducir alucinaciones al fundamentar las respuestas en datos reales
- Crear asistentes especializados sin necesidad de reentrenar modelos

## Arquitectura del Sistema

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
   │ Base de datos│ <──  │   chroma_db     │ <──  │   OpenAI     │
   │  vectorial   │      │.save_to_chroma()│      │  Embeddings  │
   │  (ChromaDB)  │      └─────────────────┘      └──────────────┘
   └──────────────┘

2. CONSULTA Y GENERACIÓN (Runtime)
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │   Usuario    │ ──>  │    Búsqueda     │ ──>  │  Documentos  │
   │   pregunta   │      │   semántica     │      │  relevantes  │
   │              │      │  (ChromaDB)     │      │  (top-k)     │
   └──────────────┘      └─────────────────┘      └──────────────┘
                                                           │
                                                           ▼
   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
   │   Respuesta  │ <──  │   ChatOpenAI    │ <──  │   Prompt     │
   │    final     │      │    (GPT-3.5+)   │      │ + Contexto   │
   └──────────────┘      └─────────────────┘      └──────────────┘
```

## Estructura del Proyecto

```
RAG-app-python/
├── main.py                 # Punto de entrada principal
├── src/
│   ├── file_processor.py   # Procesamiento y chunking de PDFs
│   └── chroma_db.py        # Gestión de la base de datos vectorial
├── documents/              # Carpeta donde colocas tus PDFs (debe crearse)
├── chroma/                 # Base de datos vectorial (se genera automáticamente)
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## Descripción de Archivos

### `main.py`
**Orquestador principal del sistema RAG**

Este archivo coordina todo el flujo de trabajo:

1. **Configuración inicial**: Establece la API key de OpenAI
2. **Procesamiento**: Llama a `chunk_pdfs()` para convertir PDFs en fragmentos
3. **Embedding**: Inicializa el modelo `text-embedding-3-large` de OpenAI
4. **Almacenamiento**: Guarda los vectores en ChromaDB
5. **Consulta**: Realiza búsqueda semántica con la pregunta del usuario
6. **Generación**: Construye un prompt con el contexto y genera la respuesta

**Ejemplo de uso en el código:**
```python
# Define tu pregunta
query = "What are the recommended steps for fertilizing a vegetable garden?"

# Busca los 3 documentos más relevantes
docs = db.similarity_search_with_score(query, k=3)

# Genera respuesta con ChatOpenAI
model = ChatOpenAI()
response = model.predict(prompt)
```

### `src/file_processor.py`
**Módulo de procesamiento de documentos**

**Responsabilidad**: Convertir PDFs en chunks (fragmentos) procesables.

**¿Qué hace?**
- Lee todos los PDFs de la carpeta `documents/`
- Divide el texto en fragmentos de 800 caracteres
- Mantiene un overlap de 100 caracteres entre chunks para preservar contexto
- Añade índices de inicio para rastreabilidad

**Parámetros importantes:**
- `chunk_size=800`: Tamaño óptimo para búsqueda semántica
- `chunk_overlap=100`: Evita perder información en los bordes
- `RecursiveCharacterTextSplitter`: Divide respetando estructura del texto

**¿Por qué es necesario?**
Los modelos de embeddings tienen límites de tokens. Dividir documentos largos en chunks permite:
- Búsquedas más precisas
- Mejor rendimiento de embeddings
- Respuestas más focalizadas

### `src/chroma_db.py`
**Módulo de gestión de base de datos vectorial**

**Responsabilidad**: Almacenar y gestionar los embeddings en ChromaDB.

**¿Qué hace?**
- Elimina la base de datos anterior (si existe) para evitar duplicados
- Crea embeddings para cada chunk usando OpenAI
- Almacena los vectores en ChromaDB localmente
- Provee interfaz para búsquedas de similitud

**ChromaDB**: Base de datos vectorial open-source optimizada para:
- Búsqueda por similitud coseno
- Almacenamiento eficiente de embeddings
- Consultas rápidas en grandes volúmenes de datos

## Algoritmo RAG - Paso a Paso

### Fase 1: Preparación (Offline)

```python
# 1. Cargar y procesar documentos
processed_documents = chunk_pdfs()
# Resultado: Lista de objetos Document con texto fragmentado

# 2. Generar embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
# Modelo de OpenAI que convierte texto en vectores de 3072 dimensiones

# 3. Guardar en base de datos vectorial
db = save_to_chroma_db(processed_documents, embedding_model)
# ChromaDB almacena pares (texto, vector) para búsqueda rápida
```

### Fase 2: Consulta (Runtime)

```python
# 1. Buscar documentos relevantes
query = "¿Cómo fertilizar un jardín?"
docs = db.similarity_search_with_score(query, k=3)
# Retorna los 3 chunks más similares semánticamente

# 2. Construir contexto
context = "\n\n---\n\n".join([doc.page_content for doc, _score in docs])
# Une los chunks relevantes en un solo string

# 3. Crear prompt estructurado
prompt = f"""
Contexto: {context}
Pregunta: {query}
Responde basándote SOLO en el contexto proporcionado.
"""

# 4. Generar respuesta
model = ChatOpenAI()
response = model.predict(prompt)
# GPT genera respuesta fundamentada en los documentos
```

## Cómo Funciona la Búsqueda Semántica

1. **Embedding de la pregunta**: La consulta se convierte en un vector numérico
2. **Similitud coseno**: Se compara con todos los vectores almacenados en ChromaDB
3. **Ranking**: Se ordenan los chunks por similitud (score)
4. **Top-k retrieval**: Se seleccionan los k documentos más relevantes

**Ventaja sobre búsqueda tradicional**: No busca palabras exactas, sino **significado**.
- Pregunta: "¿Cómo nutrir plantas?"
- Encuentra: "fertilización de jardines" (aunque no use las mismas palabras)

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- Cuenta de OpenAI con API key

### Pasos

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

4. **Configurar API Key de OpenAI**

   Opción A: Variable de entorno
   ```bash
   # Windows
   set OPENAI_API_KEY=tu-api-key-aqui

   # Linux/Mac
   export OPENAI_API_KEY=tu-api-key-aqui
   ```

   Opción B: Modificar directamente en `main.py` (línea 11)
   ```python
   os.environ["OPENAI_API_KEY"] = "tu-api-key-aqui"
   ```

5. **Agregar documentos PDF**
   ```bash
   mkdir documents
   # Copia tus archivos PDF en esta carpeta
   ```

6. **Ejecutar el proyecto**
   ```bash
   python main.py
   ```

## Personalización

### Cambiar la pregunta

Modifica la variable `query` en `main.py` (línea 25):
```python
query = "Tu pregunta aquí"
```

### Ajustar número de documentos recuperados

Modifica el parámetro `k` en `main.py` (línea 28):
```python
docs = db.similarity_search_with_score(query, k=5)  # Ahora recupera 5 documentos
```

### Cambiar tamaño de chunks

Edita `src/file_processor.py` (línea 14-16):
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Chunks más grandes
    chunk_overlap=200,  # Mayor overlap para mejor contexto
    length_function=len,
    add_start_index=True,
)
```

### Usar un modelo diferente de OpenAI

Modifica `main.py` (línea 46):
```python
model = ChatOpenAI(model="gpt-4")  # Usar GPT-4 para mejor calidad
```

## Dependencias Principales

- **langchain**: Framework para construir aplicaciones con LLMs
- **langchain-openai**: Integración de OpenAI con LangChain
- **langchain-community**: Loaders y utilidades comunitarias
- **chromadb**: Base de datos vectorial para embeddings
- **pypdf**: Lector de archivos PDF

## Limitaciones Actuales

- La base de datos se recrea cada vez que ejecutas el programa (no es persistente entre ejecuciones)
- Solo soporta archivos PDF
- Requiere conexión a internet (llamadas a API de OpenAI)
- Costos asociados al uso de la API de OpenAI

## Mejoras Futuras

- [ ] Persistencia de ChromaDB entre ejecuciones
- [ ] Soporte para múltiples formatos (DOCX, TXT, Markdown)
- [ ] Interfaz web con Streamlit o Gradio
- [ ] Sistema de caché para reducir llamadas a la API
- [ ] Soporte para modelos locales (Llama, Mistral)
- [ ] Evaluación de calidad de respuestas

## Recursos Adicionales

- [Documentación de LangChain](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Artículo original en Medium](https://cristianfdev.medium.com/how-to-make-a-rag-retrieval-augmented-generation-in-python-e23b1e4d3dee)

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

---

**Nota**: Este proyecto es una implementación educativa de RAG. Para uso en producción, considera implementar manejo de errores robusto, logging, y medidas de seguridad adicionales.
