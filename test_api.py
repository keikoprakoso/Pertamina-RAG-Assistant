"""
Test script for the FastAPI endpoint
"""
import requests
import time

def test_api():
    # Base URL for the API
    base_url = "http://localhost:8000"
    
    # Test root endpoint
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API. Make sure the server is running.")
        return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test health endpoint
    print("\nTesting health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint status: {response.status_code}")
        print(f"Health endpoint response: {response.json()}")
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test ask endpoint
    print("\nTesting ask endpoint...")
    test_questions = [
        "How do I safely shut down the turbine?",
        "Apa langkah-langkah untuk mematikan turbin dengan aman?",
        "What should I do before engaging the braking system?"
    ]
    
    for question in test_questions:
        print(f"\nAsking: {question}")
        try:
            response = requests.post(
                f"{base_url}/ask",
                json={"question": question}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Answer: {result['answer']}")
                print(f"Timestamp: {result['timestamp']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"ERROR: {e}")
        
        # Add a small delay between requests
        time.sleep(1)

if __name__ == "__main__":
    test_api()