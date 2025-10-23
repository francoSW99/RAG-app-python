# 🌐 Guía de la Interfaz Web con Streamlit

## Inicio Rápido

### Ejecutar la Aplicación Web

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Características

### 🎨 Interfaz Web Moderna
- Diseño limpio y minimalista en tonos grises
- Soporte para modo claro/oscuro
- Interfaz de chat en tiempo real
- Citación de fuentes expandibles

### ⚙️ Configuración Interactiva
- **Entrada de API Key**: Ingresa tu API key de Groq directamente en el sidebar
- **Selección de Modelo**: Elige entre diferentes modelos de Groq
  - `llama-3.3-70b-versatile` (Recomendado - El más reciente y mejor)
  - `llama-3.1-70b-versatile` (Excelente calidad)
  - `llama-3.1-8b-instant` (El más rápido)
  - `gemma2-9b-it` (Compacto)
- **Número de Fuentes**: Ajusta cuántos fragmentos de documentos recuperar (1-10)
- **Temperatura**: Controla la creatividad de las respuestas (0.0 = enfocado, 1.0 = creativo)

### 💬 Funciones del Chat
- **Historial Persistente**: El historial de chat se mantiene durante la sesión
- **Visualización de Fuentes**: Cada respuesta muestra las fuentes con:
  - Nombre del documento
  - Número de página
  - Porcentaje de relevancia
- **Limpiar Historial**: Botón para resetear la conversación

## Uso Paso a Paso

### 1. Prepara tus Documentos
```bash
# Coloca tus archivos PDF en la carpeta documents
cp tus-archivos/*.pdf documents/
```

### 2. Inicia la Aplicación
```bash
streamlit run app.py
```

### 3. Configura en el Sidebar
1. Ingresa tu API key de Groq (obtén una gratis en [console.groq.com](https://console.groq.com/))
2. Elige tu modelo preferido
3. Ajusta la configuración (opcional)

### 4. Inicializa el Sistema
Haz clic en el botón "🚀 Initialize RAG System"

Espera a que:
- ✅ Se procesen los documentos
- ✅ Se cargue el modelo de embeddings
- ✅ Se cree la base de datos ChromaDB
- ✅ Se inicialice el LLM

### 5. ¡Comienza a Chatear!
Escribe tus preguntas en el input de chat en la parte inferior

## Ejemplos de Preguntas

### Para Papers Académicos
- "Resume la sección de metodología"
- "¿Cuáles son los principales hallazgos de esta investigación?"
- "Compara los resultados con estudios previos"

### Para Libros
- "¿Cuáles son los temas principales discutidos en el capítulo 3?"
- "Resume el argumento del autor sobre [tema]"
- "¿Qué ejemplos proporciona el autor para [concepto]?"

### Para Documentación Técnica
- "¿Cómo configuro [funcionalidad]?"
- "¿Cuáles son los requisitos del sistema?"
- "Explica el diagrama de arquitectura"

## Consejos para Mejores Resultados

### 📝 Escribir Buenas Preguntas
- Sé específico y claro
- Referencia temas o conceptos específicos
- Pregunta una cosa a la vez

### 🎯 Optimizar la Recuperación
- Aumenta el número de fuentes (k) para preguntas complejas
- Usa temperatura baja (0.0-0.3) para respuestas factuales
- Usa temperatura alta (0.5-0.8) para respuestas creativas

### 🔧 Solución de Problemas

#### Error "System not initialized"
- Asegúrate de hacer clic en "Initialize RAG System"
- Verifica que la carpeta documents/ contenga archivos PDF
- Confirma que la API key sea correcta

#### Tiempos de Respuesta Lentos
- Los PDFs grandes tardan en procesarse inicialmente
- La primera consulta carga el modelo de embeddings (~90MB)
- Las consultas siguientes son más rápidas

#### "No se encontró información relevante"
- Intenta reformular tu pregunta
- Aumenta el número de fuentes
- Asegúrate de que tu pregunta se relacione con el contenido del documento

## Atajos de Teclado

- `Ctrl + Enter`: Enviar mensaje
- `Ctrl + K`: Enfocar en el input de chat
- `Ctrl + Shift + R`: Reejecutar app (refrescar)

## Configuración Avanzada

### Estilos Personalizados
Edita el CSS en `app.py` líneas 23-80:

```python
st.markdown("""
<style>
    /* Tus estilos personalizados aquí */
</style>
""", unsafe_allow_html=True)
```

### Cambiar Configuración Predeterminada
Modifica los valores por defecto en los controles del sidebar (líneas 74-103)

### Agregar Modelos Personalizados
Añade al dropdown de selección de modelo (línea 76):

```python
model_name = st.selectbox(
    "LLM Model",
    ["llama-3.3-70b-versatile", "tu-modelo-personalizado"],
)
```

## Despliegue

### Desplegar en Streamlit Cloud (Gratis)

1. Sube tu código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io/)
3. Conecta tu repositorio
4. Agrega secrets:
   ```toml
   # .streamlit/secrets.toml
   GROQ_API_KEY = "tu-api-key-aqui"
   ```
5. ¡Despliega!

### Desplegar en Otras Plataformas

#### Heroku
```bash
# Agrega Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Despliega
git push heroku main
```

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Consejos de Rendimiento

### Carga Más Rápida
- Usa modelos de embeddings más pequeños para pruebas
- Cachea la base de datos ChromaDB
- Procesa documentos offline

### Optimización de Memoria
- Limita el tamaño de chunks en file_processor.py
- Usa versión CPU-only de torch para embeddings
- Limpia el historial de chat periódicamente

## Notas de Seguridad

⚠️ **Importante para Despliegues**:
- Nunca hagas commit del archivo `.env`
- Usa secrets de Streamlit para producción
- Implementa rate limiting para despliegues públicos
- Agrega autenticación si es necesario

## Comparación: CLI vs Interfaz Web

| Característica | CLI (main.py) | Web (app.py) |
|----------------|---------------|--------------|
| **Interfaz** | Terminal | Navegador |
| **Facilidad de Uso** | Usuarios técnicos | Cualquier persona |
| **Historial** | Solo sesión | Persistente durante sesión |
| **Configuración** | Código/vars entorno | UI Interactiva |
| **Despliegue** | Solo local | Se puede desplegar online |
| **Fuentes** | Formato texto | Cajas expandibles |
| **Setup** | Más rápido | Ligeramente más lento |

## Preguntas Frecuentes

### ¿Puedo usar ambas interfaces CLI y Web?
¡Sí! Ambas usan el mismo backend. Ejecuta `python main.py` para CLI o `streamlit run app.py` para web.

### ¿Mis documentos se suben a la nube?
¡No! Todo se ejecuta localmente. Solo las llamadas al LLM van a la API de Groq.

### ¿Puedo personalizar el aspecto?
¡Sí! Edita el CSS en el archivo app.py.

### ¿Cómo actualizo los modelos?
Simplemente selecciona un modelo diferente del sidebar y re-inicializa.

## Paleta de Colores

### Esquema Minimalista en Grises
- **Header**: Degradado gris oscuro (#4a5568 → #2d3748)
- **Mensajes del usuario**: Gris claro (#e2e8f0)
- **Mensajes del asistente**: Gris medio (#edf2f7)
- **Cajas de fuentes**: Gris muy claro (#f7fafc)
- **Texto principal**: Negro oscuro (#1a202c)
- **Texto secundario**: Gris medio (#4a5568)
- **Borde de fuentes**: Gris oscuro (#4a5568)

### Filosofía de Diseño
- Minimalista y profesional
- Colores que combinan en tonos grises
- Alto contraste para legibilidad
- Consistencia visual en todos los elementos

## Soporte

- **Issues**: [GitHub Issues](https://github.com/francoSW99/RAG-app-python/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/francoSW99/RAG-app-python/discussions)

---

Hecho con ❤️ usando Streamlit | Powered by Groq + HuggingFace
