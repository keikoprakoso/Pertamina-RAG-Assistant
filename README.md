# Geothermal Knowledge Base Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)

A Retrieval-Augmented Generation (RAG) Q&A bot for geothermal energy operations with bilingual support (English & Indonesian).

## 🌋 Project Overview

This system allows geothermal energy professionals to ask questions about internal documents (SOPs & procedures) and receive clear bilingual answers based on real context, not just generic LLM hallucinations.

Built with modern technologies including FastAPI, OpenAI embeddings, and FAISS vector database, this assistant provides accurate information retrieval and natural language responses.

## 🚀 Features

- **Document Ingestion**: Processes geothermal SOP documents and splits them into semantic chunks
- **Semantic Search**: Uses OpenAI embeddings for intelligent document retrieval
- **Vector Database**: Implements FAISS for efficient similarity search
- **RAG Architecture**: Combines retrieval and generation for accurate answers
- **Bilingual Support**: Provides responses in both English and Indonesian
- **Modern UI**: Clean dark-themed web interface with responsive design
- **REST API**: FastAPI backend with interactive documentation
- **Q&A Logging**: Records all interactions with timestamps for traceability

## 📁 Project Structure

```
geothermal-knowledge-base-assistant/
├── app.py                 # Main FastAPI application
├── rag.py                 # RAG system implementation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── pertamina_sop.txt      # Geothermal SOP document
├── test_rag.py            # Test script
├── cli.py                 # Command-line interface
├── setup.py               # Setup script
├── run.sh                 # Run script (Unix/Linux/macOS)
├── run.bat                # Run script (Windows)
├── init_vector_store.py   # Vector store initialization script
├── test_api.py            # API test script
├── frontend/              # Web frontend files
│   ├── index.html         # Main HTML file
│   ├── style.css          # Dark-themed styling
│   └── script.js          # Frontend logic
├── faiss_index/           # FAISS vector database (generated)
├── logs/                  # Log files (generated)
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/account/api-keys))

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/geothermal-knowledge-base-assistant.git
   cd geothermal-knowledge-base-assistant
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key

### Running the Application

1. Start the FastAPI server:
   ```bash
   python3 app.py
   ```

2. Access the web interface at: http://localhost:8000/static/index.html

3. API documentation available at: http://localhost:8000/docs

## 🖥️ Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000/static/index.html`
2. Type your question in the input field (in English or Indonesian)
3. Click "Send" or press Enter
4. View the bilingual response in the chat history

### API Usage

To ask a question via API, send a POST request to `/ask`:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the safety protocols for geothermal well drilling?"}'
```

Or using Python requests:

```python
import requests

response = requests.post("http://localhost:8000/ask", 
                         json={"question": "What are the safety protocols for geothermal well drilling?"})
print(response.json())
```

## 📚 Available Topics

The system covers the following geothermal energy topics:
- Geothermal Well Drilling Safety Protocol
- Steam Field Operations Manual
- Power Plant Startup Procedure
- Environmental Monitoring Requirements
- Maintenance Schedule for Geothermal Equipment
- Emergency Response for Hydrogen Sulfide Release
- Personnel Training for Geothermal Operations
- Water Management in Geothermal Systems

## 🧪 Testing

Run the test script to verify the system works:
```bash
python3 test_rag.py
```

Or use the command-line interface:
```bash
python3 cli.py
```

## 🏗️ Development

To extend the system:

1. Modify `rag.py` to customize the RAG pipeline
2. Adjust chunking parameters in the `split_document` method
3. Modify the prompt in `generate_answer` for different response formats
4. Add more preprocessing steps for document ingestion

## 📖 How It Works

1. **Document Ingestion**: The system reads the SOP document and splits it into chunks
2. **Embedding**: Each chunk is converted to embeddings using OpenAI's text-embedding-ada-002 model
3. **Vector Storage**: Embeddings are stored in a FAISS vector database for efficient similarity search
4. **Retrieval**: When a question is asked, it's converted to an embedding and similar chunks are retrieved
5. **Generation**: The retrieved context is used to construct a prompt for OpenAI's GPT-3.5-turbo model
6. **Response**: The model generates a bilingual answer based on the context

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for embeddings and language models
- [Facebook AI](https://ai.facebook.com/) for FAISS vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework# Pertamina-RAG-Assistant
# Pertamina-RAG-Assistant
