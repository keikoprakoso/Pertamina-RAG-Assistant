"""
Command-line interface for the Company Knowledge Base Assistant
"""
import os
import sys
from rag import RAGSystem

def main():
    print("Company Knowledge Base Assistant - CLI")
    print("=" * 40)
    print("Type 'quit' or 'exit' to stop the program")
    print()
    
    # Initialize RAG system
    rag_system = RAGSystem()
    
    # Check if vector store exists, if not build it
    if not os.path.exists("faiss_index"):
        print("Building vector store from document...")
        rag_system.build_vector_store("pertamina_sop.txt")
    else:
        print("Loading existing vector store...")
        rag_system.load_vector_store()
    
    print("\nReady! Ask questions about the SOP document.")
    print()
    
    while True:
        try:
            question = input("Question (English/Indonesian): ").strip()
            
            if question.lower() in ['quit', 'exit', 'quit()', 'exit()']:
                print("Goodbye!")
                break
            
            if not question:
                continue
                
            print("Processing...")
            answer = rag_system.ask(question)
            print(f"\nAnswer:\n{answer}\n")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    main()