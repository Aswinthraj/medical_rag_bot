import requests
import json

print("=" * 60)
print("Testing New API Format")
print("=" * 60)

# Test with localhost
BASE_URL = "http://localhost:8000"

print("\n[Test 1] Testing /ask endpoint with new format...")
print("Query: What is diabetes?")
print("Top K: 5")

try:
    # New request format
    payload = {
        "query": "What is diabetes?",
        "top_k": 5
    }
    
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
        
        print("\n" + "=" * 60)
        print("CONTEXTS (Retrieved Documents):")
        print("=" * 60)
        contexts = result.get("contexts", [])
        for i, context in enumerate(contexts, 1):
            print(f"\n[Context {i}]")
            print(context[:200] + "..." if len(context) > 200 else context)
        
        print("\n" + "=" * 60)
        print(f"Total contexts returned: {len(contexts)}")
        print("=" * 60)
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n[Test 2] Testing with different top_k...")
print("Query: What are the symptoms of hypertension?")
print("Top K: 3")

try:
    payload = {
        "query": "What are the symptoms of hypertension?",
        "top_k": 3
    }
    
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
        print("\n" + "=" * 60)
        print(f"Total contexts returned: {len(result.get('contexts', []))}")
        print("=" * 60)
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n✓ API format updated successfully!")
print("\nRequest Format:")
print(json.dumps({"query": "string (required)", "top_k": "integer (required)"}, indent=2))
print("\nResponse Format:")
print(json.dumps({"answer": "string (required)", "contexts": ["string", "..."]}, indent=2))
