import pandas as pd
import matplotlib.pyplot as plt

# Încarcă datele colectate
df = pd.read_csv("telemetry_data.csv")
df["received_at"] = pd.to_datetime(df["received_at"])

# Grafic 1: Umiditatea pe adâncimi la Vale vs. Creastă
plt.figure(figsize=(9, 4.5))
valley = df[df["node_id"] == "station_valley_01"]
crest = df[df["node_id"] == "station_crest_05"]

plt.plot(valley["received_at"], valley["moisture_60cm"], label="Vale (Y=5m) - Adâncime 60cm", color="#1f77b4", lw=2)
plt.plot(valley["received_at"], valley["moisture_25cm"], label="Vale (Y=5m) - Adâncime 25cm", color="#1f77b4", ls="--")
plt.plot(crest["received_at"], crest["moisture_60cm"], label="Creastă (Y=95m) - Adâncime 60cm", color="#d62728", lw=2)
plt.plot(crest["received_at"], crest["moisture_25cm"], label="Creastă (Y=95m) - Adâncime 25cm", color="#d62728", ls="--")

plt.title("Comparație Dinamică Umiditate Sol: Baza Pantei vs. Creastă")
plt.xlabel("Timp")
plt.ylabel("Umiditate Sol (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("grafic_umiditate_panta.png", dpi=200)

# Grafic 2: Profilul vertical al solului funcție de poziția pe pantă
plt.figure(figsize=(8, 4))
latest = df.groupby("node_id").last().sort_values("position_y_m")
plt.plot(latest["position_y_m"], latest["moisture_5cm"], marker="o", label="Strat 5 cm")
plt.plot(latest["position_y_m"], latest["moisture_25cm"], marker="s", label="Strat 25 cm")
plt.plot(latest["position_y_m"], latest["moisture_60cm"], marker="^", label="Strat 60 cm")

plt.title("Profilul Umidității Solului de-a lungul Pantei (30°)")
plt.xlabel("Poziție pe Pantă Y (metri: 0=Vale, 100=Creastă)")
plt.ylabel("Umiditate (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("grafic_profil_teren.png", dpi=200)
print("Graficele au fost salvate cu succes!")