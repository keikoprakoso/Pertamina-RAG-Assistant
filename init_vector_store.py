"""
Script to initialize the FAISS vector store from the SOP document
"""
from rag import RAGSystem

def main():
    print("Initializing vector store...")
    rag_system = RAGSystem()
    rag_system.build_vector_store("pertamina_sop.txt")
    print("Vector store initialized successfully!")

if __name__ == "__main__":
    main()