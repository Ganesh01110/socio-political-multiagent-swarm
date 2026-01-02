import traceback
from app.core.engine import simulation_instance

try:
    print("Forcing one tick...")
    simulation_instance.start()
    res = simulation_instance.advance()
    print("Tick success!")
    print(res)
except Exception:
    traceback.print_exc()
