import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"

# FAISS Configuration
FAISS_INDEX_PATH = "faiss_index/index.faiss"

# Logging Configuration
LOG_FILE_PATH = "logs/qa_log.txt"