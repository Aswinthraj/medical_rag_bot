import requests
import json

print("=" * 60)
print("Testing Medical RAG Bot API")
print("=" * 60)

# Test 1: Home endpoint
print("\n[Test 1] Testing home endpoint...")
try:
    response = requests.get("http://localhost:8000/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Ask endpoint
print("\n[Test 2] Testing /ask endpoint...")
print("Question: What is diabetes?")

try:
    payload = {"question": "What is diabetes?"}
    response = requests.post(
        "http://localhost:8000/ask",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(result.get("answer", "No answer found"))
        print("=" * 60)
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n[Test 3] Testing with another question...")
print("Question: What are the symptoms of hypertension?")

try:
    payload = {"question": "What are the symptoms of hypertension?"}
    response = requests.post(
        "http://localhost:8000/ask",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(result.get("answer", "No answer found"))
        print("=" * 60)
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
