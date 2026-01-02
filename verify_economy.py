import urllib.request
import json
import time

def get_state():
    req = urllib.request.Request("http://localhost:8000/api/simulation/state", method="GET")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def advance_tick():
    req = urllib.request.Request("http://localhost:8000/api/simulation/tick", method="POST")
    with urllib.request.urlopen(req) as response:
        pass

initial_state = get_state()
initial_wealth = 0
citizen = next((a for a in initial_state['agents'] if a['type'] == 'citizen'), None)
if citizen:
    initial_wealth = citizen.get('wealth', 0)
    print(f"Initial Wealth: {initial_wealth}")

advance_tick()
time.sleep(1)

new_state = get_state()
new_citizen = next((a for a in new_state['agents'] if a['id'] == citizen['id']), None)
if new_citizen:
    print(f"New Wealth: {new_citizen.get('wealth', 0)}")
    if new_citizen.get('wealth', 0) >= initial_wealth:
        print("PASS: Wealth increased or stayed same")
    else:
        print("FAIL: Wealth decreased strangely")
