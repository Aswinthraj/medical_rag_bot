import requests
import json
import time

# Wait a moment for server to be ready
time.sleep(2)

print("=" * 60)
print("Testing /ask endpoint")
print("=" * 60)

# Test the /ask endpoint
url = "http://127.0.0.1:8000/ask"
payload = {
    "query": "What is diabetes?",
    "top_k": 3
}

print(f"\nSending request to: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(result.get("answer", "No answer found"))
        print("\n" + "=" * 60)
        print("CONTEXTS RETRIEVED:")
        print("=" * 60)
        for i, context in enumerate(result.get("contexts", []), 1):
            print(f"\n[Context {i}]")
            print(context[:200] + "..." if len(context) > 200 else context)
    else:
        print(f"\nError Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Connection Error: Is the server running on http://127.0.0.1:8000?")
except requests.exceptions.Timeout:
    print("\n❌ Timeout: Request took too long")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
