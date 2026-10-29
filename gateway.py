import asyncio
import json
import csv
import os
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8888
CSV_FILE = "telemetry_data.csv"

# Contoare pentru statistici / PDF
total_packets_received = 0
start_time = None

def init_csv():
    """Inițializează fișierul CSV cu antetul corespunzător."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "received_at", "node_id", "position_y_m", "elevation_m",
                "air_temp_c", "air_humidity_pct", "solar_radiation_wm2", "rain_mm",
                "moisture_5cm", "moisture_25cm", "moisture_60cm"
            ])

async def handle_sensor_node(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Tratează conexiunea TCP asincronă cu o stație senzor."""
    global total_packets_received
    peer = writer.get_extra_info("peername")
    
    while True:
        line = await reader.readline()
        if not line:
            break  # Nodul a închis conexiunea
        
        try:
            data = json.loads(line.decode("utf-8").strip())
            total_packets_received += 1
            
            # 1. Salvare în fișier CSV
            with open(CSV_FILE, mode="a", newline="") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([
                    datetime.now().isoformat(),
                    data["node_id"],
                    data["position_y"],
                    data["elevation"],
                    data["air_temperature"],
                    data["air_humidity"],
                    data["solar_radiation"],
                    data["rain_mm"],
                    data["soil_moisture"]["depth_5cm"],
                    data["soil_moisture"]["depth_25cm"],
                    data["soil_moisture"]["depth_60cm"]
                ])

            # 2. Log formatat în consolă (perfect pentru screenshot)
            now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            soil = data["soil_moisture"]
            print(
                f"[{now}] [GATEWAY-RX] Node: {data['node_id']} (Y={data['position_y']:>4.1f}m) | "
                f"Air: {data['air_temperature']:>4.1f}°C, {data['air_humidity']:>4.1f}% | "
                f"Rain: {data['rain_mm']:>4.1f}mm | "
                f"Soil: [5cm: {soil['depth_5cm']:>4.1f}%, 25cm: {soil['depth_25cm']:>4.1f}%, 60cm: {soil['depth_60cm']:>4.1f}%]"
            )
            
            # Trimite confirmare (ACK) către nod
            response = {"status": "ACK", "node_id": data["node_id"]}
            writer.write((json.dumps(response) + "\n").encode("utf-8"))
            await writer.drain()

        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(f"[ERR] Eroare la procesarea pachetului: {e}")
            break

    writer.close()
    await writer.wait_closed()

async def stats_monitor():
    """Afișează periodic randamentul gateway-ului (Throughput)."""
    while True:
        await asyncio.sleep(5)
        elapsed = datetime.now() - start_time
        rate = total_packets_received / elapsed.total_seconds() if elapsed.total_seconds() > 0 else 0
        print(f"\n--- [GATEWAY STATS] Total: {total_packets_received} pachete | Rata: {rate:.2f} pachete/sec ---\n")

async def main():
    global start_time
    init_csv()
    start_time = datetime.now()
    server = await asyncio.start_server(handle_sensor_node, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"============================================================")
    print(f"[GATEWAY] Pornit pe {addr[0]}:{addr[1]} (Event Loop: asyncio)")
    print(f"[GATEWAY] Salvare date în: {CSV_FILE}")
    print(f"============================================================\n")

    async with server:
        await asyncio.gather(server.serve_forever(), stats_monitor())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[GATEWAY] Oprire la cererea utilizatorului.")