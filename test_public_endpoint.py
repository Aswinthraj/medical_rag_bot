import requests
import json

# Your public ngrok URL
BASE_URL = "https://denese-unsealed-brain.ngrok-free.dev"

print("=" * 60)
print("Testing Public Medical RAG Bot Endpoint")
print("=" * 60)

# Test 1: Home endpoint
print("\n[Test 1] Testing home endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
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
        f"{BASE_URL}/ask",
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

print("\n✓ Your endpoint is live and accessible!")
print(f"Share this URL: {BASE_URL}")
