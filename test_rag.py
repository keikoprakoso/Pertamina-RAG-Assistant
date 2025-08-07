"""
Test script for the RAG system
"""
import os
from rag import RAGSystem

def main():
    # Initialize RAG system
    rag_system = RAGSystem()
    
    # Build vector store from document
    print("Building vector store...")
    rag_system.build_vector_store("pertamina_sop.txt")
    
    # Test questions
    test_questions = [
        "How do I safely shut down the turbine?",
        "What are the steps to close the main steam valve?",
        "Berapa lama saya harus menunggu sebelum mengaktifkan sistem pengereman?",
        "What is the maximum RPM before shutdown?"
    ]
    
    print("\nTesting RAG system:")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 30)
        answer = rag_system.ask(question)
        print(f"Answer: {answer}")
        print("=" * 50)

if __name__ == "__main__":
    main()