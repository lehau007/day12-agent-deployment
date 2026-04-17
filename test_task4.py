import requests
import json

BASE_URL = "http://localhost:8000"

def test_security():
    print("--- 1. Testing 401 Unauthorized ---")
    r = requests.post(f"{BASE_URL}/ask", json={"question": "Hello"})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}\n")

    print("--- 2. Logging in to get JWT Token ---")
    r = requests.post(f"{BASE_URL}/auth/token", json={"username": "student", "password": "demo123"})
    token = r.json().get("access_token")
    print(f"Token obtained: {token[:30]}...\n")

    headers = {"Authorization": f"Bearer {token}"}

    print("--- 3. Testing 200 OK with Token ---")
    r = requests.post(f"{BASE_URL}/ask", headers=headers, json={"question": "What is Docker?"})
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}\n")

    print("--- 4. Testing 429 Rate Limiting (Spamming 12 requests) ---")
    for i in range(12):
        r = requests.post(f"{BASE_URL}/ask", headers=headers, json={"question": f"Spam {i}"})
        if r.status_code == 429:
            print(f"Request {i+1}: {r.status_code} - Too Many Requests ✅")
            print(f"Detail: {r.json()['detail']['error']}")
            break
        else:
            print(f"Request {i+1}: {r.status_code} OK")

if __name__ == "__main__":
    try:
        test_security()
    except Exception as e:
        print(f"Error: {e}")
