import multiprocessing
import socket
import time
import json
import math
import random

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 8888
SLOPE_ANGLE_DEG = 30.0  # Panta solului
SLOPE_RAD = math.radians(SLOPE_ANGLE_DEG)

def run_sensor_station(node_id: str, position_y: float, interval_sec: float = 1.0):
    """
    Simulează o stație meteo/agricolă pe o pantă.
    position_y: poziția pe pantă (0m = baza văii, 100m = vârful crestei).
    """
    # Altitudinea calculată trigonometric
    elevation = position_y * math.sin(SLOPE_RAD)
    
    # Stare internă pentru umiditatea din sol la 3 adâncimi
    # Baza pantei are umiditate inițială mai mare din cauza acumulării
    base_factor = 1.0 - (position_y / 150.0)
    moist_5cm = 25.0 * base_factor
    moist_25cm = 35.0 * base_factor
    moist_60cm = 40.0 * base_factor

    # Conectare TCP către Gateway
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect((GATEWAY_HOST, GATEWAY_PORT))
            print(f"[{node_id}] Conectat cu succes la Gateway ({GATEWAY_HOST}:{GATEWAY_PORT})")
            break
        except ConnectionRefusedError:
            time.sleep(1.0)

    step = 0
    try:
        while True:
            step += 1
            sim_time = step * interval_sec

            # 1. Mediu aer (sinusoidă pentru ciclul zi/noapte + zgomot senzor)
            air_temp = 18.0 + 8.0 * math.sin(sim_time / 20.0) + random.uniform(-0.3, 0.3)
            solar_rad = max(0.0, 750.0 * math.sin(sim_time / 20.0)) + random.uniform(0, 15)
            air_humidity = max(20.0, min(95.0, 65.0 - (air_temp - 18.0) * 2.0 + random.uniform(-2, 2)))
            
            # Episod periodic de ploaie (simulat la fiecare 60 de pași)
            is_raining = (step % 60) > 45
            rain_mm = random.uniform(2.0, 6.0) if is_raining else 0.0

            # 2. Modelul fizic de sol și pantă:
            # - Apa de ploaie care se infiltrează este redusă de panta de 30 grade (runoff)
            # - Baza pantei (position_y mic) primește aport suplimentar de la scurgerea de sus
            runoff_loss = math.sin(SLOPE_RAD) * 0.4
            effective_rain = rain_mm * (1.0 - runoff_loss)
            runoff_accumulation = (100.0 - position_y) / 100.0 * (rain_mm * runoff_loss)

            # Dinamica pe verticală (3 straturi):
            # Stratul 1 (5cm): răspuns rapid la ploaie, uscat rapid de soare/temperatură
            evap = (solar_rad / 300.0) * 0.4
            moist_5cm += (effective_rain + runoff_accumulation) * 1.2 - evap
            moist_5cm = max(10.0, min(60.0, moist_5cm))

            # Stratul 2 (25cm): percolare gravitațională lentă din stratul 1
            percolation_1_to_2 = (moist_5cm - moist_25cm) * 0.08
            moist_25cm += percolation_1_to_2
            moist_25cm = max(15.0, min(55.0, moist_25cm))

            # Stratul 3 (60cm): tampon adânc, variații reduse
            percolation_2_to_3 = (moist_25cm - moist_60cm) * 0.03
            moist_60cm += percolation_2_to_3
            moist_60cm = max(20.0, min(50.0, moist_60cm))

            # 3. Construire pachet JSON
            payload = {
                "node_id": node_id,
                "position_y": round(position_y, 2),
                "elevation": round(elevation, 2),
                "air_temperature": round(air_temp, 2),
                "air_humidity": round(air_humidity, 2),
                "solar_radiation": round(solar_rad, 2),
                "rain_mm": round(rain_mm, 2),
                "soil_moisture": {
                    "depth_5cm": round(moist_5cm, 2),
                    "depth_25cm": round(moist_25cm, 2),
                    "depth_60cm": round(moist_60cm, 2)
                }
            }

            # 4. Transmitere către Gateway
            message = json.dumps(payload) + "\n"
            sock.sendall(message.encode("utf-8"))

            # Așteaptă confirmarea (ACK)
            ack = sock.recv(1024)

            time.sleep(interval_sec)

    except (BrokenPipeError, ConnectionResetError):
        print(f"[{node_id}] Conexiunea cu Gateway-ul a fost întreruptă.")
    finally:
        sock.close()

if __name__ == "__main__":
    # Configurație stații: plasate pe o lungime de teren de 100 metri
    stations_config = [
        {"node_id": "station_valley_01", "position_y": 5.0},   # Baza pantei (valea)
        {"node_id": "station_lower_02",  "position_y": 25.0},  # Panta inferioară
        {"node_id": "station_mid_03",    "position_y": 50.0},  # Mijlocul pantei
        {"node_id": "station_upper_04",  "position_y": 75.0},  # Panta superioară
        {"node_id": "station_crest_05",  "position_y": 95.0},  # Creasta / Vârful
    ]

    processes = []
    print(f"[MAIN] Se pornesc {len(stations_config)} procese senzor...")

    for config in stations_config:
        p = multiprocessing.Process(
            target=run_sensor_station,
            args=(config["node_id"], config["position_y"], 1.0)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()