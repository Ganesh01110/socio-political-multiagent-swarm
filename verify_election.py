import urllib.request
import json

req = urllib.request.Request("http://localhost:8000/api/simulation/election", method="POST")
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
