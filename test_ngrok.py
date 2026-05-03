import requests
import json

# Test ngrok URL
url = "https://denese-unsealed-brain.ngrok-free.dev/ask"
data = {
    "query": "What is cancer?",
    "top_k": 5
}

print("Testing ngrok public URL...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\n" + "="*60)

try:
    # Add headers to bypass ngrok warning
    headers = {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print("\nAnswer:")
        print(result.get('answer', 'No answer')[:500])
        print(f"\nContexts: {len(result.get('contexts', []))} sources")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text[:500])
except Exception as e:
    print(f"\n❌ Exception: {e}")
