import requests

url = "http://localhost:8000/analyze"
payload = {
    "input": "Read about flow states and productivity.",
    "output": "Created a new time-blocking schedule based on that.",
    "energy": 7,
    "focus": 8,
    "mood": 6
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response:", response.json())