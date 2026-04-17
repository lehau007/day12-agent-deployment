import requests
import json
import time

url = "https://day12-agent-production-c313.up.railway.app"
api_key = "prod-key-2110"

print("--- 1. Health Check ---")
r = requests.get(f"{url}/health")
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")

print("--- 2. Readiness Check ---")
r = requests.get(f"{url}/ready")
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")

print("--- 3. Authentication Test (Should return 401) ---")
r = requests.post(f"{url}/ask", json={"question": "Hello"})
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")

print("--- 4. API Test with Authentication ---")
r = requests.post(f"{url}/ask", headers={"X-API-Key": api_key}, json={"question": "What is production deployment?"})
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}\n")

print("--- 5. Rate Limiting Test ---")
for i in range(1, 16):
    r = requests.post(f"{url}/ask", headers={"X-API-Key": api_key}, json={"question": f"Test {i}"})
    print(f"Request {i}: {r.status_code}")
    if r.status_code == 429:
        print(f"Response: {r.text}")
