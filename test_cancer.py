import requests
import json

# Test locally
url = "http://localhost:8000/ask"
data = {
    "query": "What is cancer?",
    "top_k": 5
}

print("Testing cancer query...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\n" + "="*60)

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print("\nAnswer:")
        print(result.get('answer', 'No answer'))
        print(f"\nContexts: {len(result.get('contexts', []))} sources")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ Exception: {e}")
