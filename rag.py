import os
import faiss
import numpy as np
from typing import List, Tuple
import tiktoken
from openai import OpenAI
import config

class RAGSystem:
    def __init__(self):
        # Initialize OpenAI client without proxies parameter
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.embedding_model = config.OPENAI_EMBEDDING_MODEL
        self.chat_model = config.OPENAI_CHAT_MODEL
        self.index = None
        self.chunks = []
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def split_document(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split document into chunks with overlap
        """
        # Split text into sentences (simplified approach)
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            tokens = self.tokenizer.encode(current_chunk + sentence)
            if len(tokens) <= chunk_size:
                current_chunk += sentence + ". "
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # Start new chunk with overlap from previous
                overlap_text = " ".join(current_chunk.split()[-overlap:]) if current_chunk else ""
                current_chunk = overlap_text + sentence + ". "
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for text chunks using OpenAI API
        """
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            embeddings.append(response.data[0].embedding)
        
        return np.array(embeddings)
    
    def build_vector_store(self, document_path: str) -> None:
        """
        Ingest document, create chunks, generate embeddings and store in FAISS
        """
        # Read document
        with open(document_path, 'r', encoding='utf-8') as f:
            document_text = f.read()
        
        # Split into chunks
        self.chunks = self.split_document(document_text)
        print(f"Document split into {len(self.chunks)} chunks")
        
        # Create embeddings
        embeddings = self.create_embeddings(self.chunks)
        print(f"Created embeddings of shape: {embeddings.shape}")
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))
        
        # Save index
        os.makedirs(os.path.dirname(config.FAISS_INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, config.FAISS_INDEX_PATH)
        
        print("Vector store built and saved")
    
    def load_vector_store(self) -> None:
        """
        Load existing FAISS index
        """
        if os.path.exists(config.FAISS_INDEX_PATH):
            self.index = faiss.read_index(config.FAISS_INDEX_PATH)
            # Reload chunks from document
            with open('pertamina_sop.txt', 'r', encoding='utf-8') as f:
                document_text = f.read()
            self.chunks = self.split_document(document_text)
            print("Vector store loaded")
        else:
            print("No existing vector store found")
    
    def retrieve_relevant_chunks(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Retrieve top-k most relevant chunks for a query
        """
        # Create embedding for query
        query_embedding = self.create_embeddings([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)
        
        # Return chunks with distances
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], float(distances[0][i])))
        
        return results
    
    def generate_answer(self, query: str, context_chunks: List[str]) -> str:
        """
        Generate answer using OpenAI GPT with provided context
        """
        # Construct prompt with context
        context = "\n\n".join([f"[Context {i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        prompt = f"""
        You are a helpful assistant for Pertamina company employees. Answer the question based ONLY on the provided context. 
        If the information is not in the context, say that you don't have enough information.
        Provide your answer in both English and Indonesian.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def ask(self, question: str) -> str:
        """
        Main method to ask a question and get an answer
        """
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(question)
        
        # Extract just the text from chunks (ignore distances)
        context_texts = [chunk for chunk, _ in relevant_chunks]
        
        # Generate answer
        answer = self.generate_answer(question, context_texts)
        
        return answer