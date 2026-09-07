import random
import time
import requests


charger_names = ["Charger-01", "Charger-02"]

while True:
    for charger_name in charger_names:

        # Simulate Charger-02 being offline
        if charger_name == "Charger-02":
            continue

        voltage = 480
        current = random.uniform(80, 100)
        power_kw = round((voltage * current) / 1000, 2)
        temperature = round(random.uniform(65, 75), 1)
        status = "charging"

        data = {
            "name": charger_name,
            "voltage": voltage,
            "current": round(current, 2),
            "power_kw": power_kw,
            "temperature": temperature,
            "status": status
        }

        response = requests.post(
            "https://ev-energy-monitor.onrender.com/sensors",
            json=data
        )

        print(response.status_code, data)

    time.sleep(5)