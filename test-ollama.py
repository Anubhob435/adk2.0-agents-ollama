import json
import requests

# Ngrok endpoint URL (note: remove trailing slash if present)
url = "https://4894-34-125-62-10.ngrok-free.app/api/chat"

# Request headers (ngrok-skip-browser-warning avoids the free-tier interstitial page)
headers = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true",
}

# Payload
payload = {
    "model": "gemma4:12b",
    "messages": [
        {
            "role": "user",
            "content": "Hello! Tell me 5 fun fact.",
        }
    ],
    "stream": False,
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    print("Response from Gemma 3:")
    print(result.get("message", {}).get("content"))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Server response: {response.text}")
except requests.exceptions.RequestException as err:
    print(f"Request failed: {err}")