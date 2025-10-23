# 🌐 Streamlit Web Interface Guide

## Quick Start

### Run the Web App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Features

### 🎨 Modern Web Interface
- Clean, responsive design
- Dark/Light mode support
- Real-time chat interface
- Expandable source citations

### ⚙️ Interactive Configuration
- **API Key Input**: Enter your Groq API key directly in the sidebar
- **Model Selection**: Choose between different Groq models
  - `llama-3.3-70b-versatile` (Recommended - Latest and best)
  - `llama-3.1-70b-versatile` (Excellent quality)
  - `llama-3.1-8b-instant` (Fastest)
  - `gemma2-9b-it` (Compact)
- **Source Count**: Adjust how many document chunks to retrieve (1-10)
- **Temperature**: Control response creativity (0.0 = focused, 1.0 = creative)

### 💬 Chat Features
- **Persistent History**: Chat history maintained during session
- **Source Display**: Each response shows sources with:
  - Document name
  - Page number
  - Relevance percentage
- **Clear History**: Button to reset conversation

## Step-by-Step Usage

### 1. Prepare Your Documents
```bash
# Place your PDF files in the documents folder
cp your-files/*.pdf documents/
```

### 2. Start the App
```bash
streamlit run app.py
```

### 3. Configure in Sidebar
1. Enter your Groq API key (get it from [console.groq.com](https://console.groq.com/))
2. Choose your preferred model
3. Adjust settings (optional)

### 4. Initialize System
Click the "🚀 Initialize RAG System" button

Wait for:
- ✅ Document processing
- ✅ Embedding model loading
- ✅ ChromaDB creation
- ✅ LLM initialization

### 5. Start Chatting!
Type your questions in the chat input at the bottom

## Example Questions

### For Academic Papers
- "Summarize the methodology section"
- "What are the main findings of this research?"
- "Compare the results with previous studies"

### For Books
- "What are the main themes discussed in chapter 3?"
- "Summarize the author's argument about [topic]"
- "What examples does the author provide for [concept]?"

### For Technical Documentation
- "How do I configure [feature]?"
- "What are the system requirements?"
- "Explain the architecture diagram"

## Tips for Best Results

### 📝 Writing Good Questions
- Be specific and clear
- Reference specific topics or concepts
- Ask one thing at a time

### 🎯 Optimizing Retrieval
- Increase source count (k) for complex questions
- Use lower temperature (0.0-0.3) for factual answers
- Use higher temperature (0.5-0.8) for creative responses

### 🔧 Troubleshooting

#### "System not initialized" Error
- Make sure you clicked "Initialize RAG System"
- Check that documents/ folder contains PDF files
- Verify API key is correct

#### Slow Response Times
- Large PDFs take time to process initially
- First query loads the embedding model (~90MB)
- Subsequent queries are faster

#### "No relevant information found"
- Try rephrasing your question
- Increase the number of sources
- Ensure your question relates to document content

## Keyboard Shortcuts

- `Ctrl + Enter`: Send message
- `Ctrl + K`: Focus on chat input
- `Ctrl + Shift + R`: Rerun app (refresh)

## Advanced Configuration

### Custom Styling
Edit the CSS in `app.py` lines 21-39:

```python
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

### Change Default Settings
Modify the default values in sidebar controls (lines 65-95)

### Add Custom Models
Add to model selection dropdown (line 71):

```python
model_name = st.selectbox(
    "LLM Model",
    ["llama-3.3-70b-versatile", "your-custom-model"],
)
```

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repository
4. Add secrets:
   ```toml
   # .streamlit/secrets.toml
   GROQ_API_KEY = "your-api-key-here"
   ```
5. Deploy!

### Deploy to Other Platforms

#### Heroku
```bash
# Add Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
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

## Performance Tips

### Faster Loading
- Use smaller embedding models for testing
- Cache the ChromaDB database
- Process documents offline

### Memory Optimization
- Limit chunk size in file_processor.py
- Use CPU-only torch version for embeddings
- Clear chat history periodically

## Security Notes

⚠️ **Important for Deployment**:
- Never commit `.env` file
- Use Streamlit secrets for production
- Implement rate limiting for public deployments
- Add authentication if needed

## Comparison: CLI vs Web Interface

| Feature | CLI (main.py) | Web (app.py) |
|---------|---------------|--------------|
| **Interface** | Terminal | Browser |
| **Ease of Use** | Technical users | Everyone |
| **History** | Session only | Persistent during session |
| **Configuration** | Code/env vars | Interactive UI |
| **Deployment** | Local only | Can deploy online |
| **Sources** | Text format | Expandable boxes |
| **Setup** | Faster | Slightly slower |

## FAQs

### Can I use both CLI and Web interfaces?
Yes! They both use the same backend. Run `python main.py` for CLI or `streamlit run app.py` for web.

### Will my documents be uploaded to the cloud?
No! Everything runs locally. Only LLM calls go to Groq API.

### Can I customize the look?
Yes! Edit the CSS in the app.py file.

### How do I update models?
Just select a different model from the sidebar and re-initialize.

## Support

- **Issues**: [GitHub Issues](https://github.com/francoSW99/RAG-app-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/francoSW99/RAG-app-python/discussions)

---

Made with ❤️ using Streamlit | Powered by Groq + HuggingFace
