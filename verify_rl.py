import urllib.request
import json
import time

def advance_tick():
    req = urllib.request.Request("http://localhost:8000/api/simulation/tick", method="POST")
    with urllib.request.urlopen(req) as response:
        pass

def get_brain():
    req = urllib.request.Request("http://localhost:8000/api/simulation/brain", method="GET")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

print("Running 100 ticks to train RL...")
for i in range(100):
    advance_tick()
    if i % 20 == 0:
        print(f"Tick {i}")

brain = get_brain()
print("Q-Table Dump:")
print(json.dumps(brain, indent=2))

if len(brain) > 0:
    print("PASS: Q-Table is populating.")
else:
    print("FAIL: Q-Table is empty.")
