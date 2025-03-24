import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Завантаження даних
gps_data = pd.read_csv("lab5/gpsdata.csv", names=["latitude", "longitude"])
accel_data = pd.read_csv("lab1/src/data/accelerometer.csv")
road_data = pd.read_csv("lab5/roadstate.csv", names=["road_condition"])

# Усереднення акселерометра для відповідності GPS
accel_data = accel_data.iloc[::(len(accel_data) // len(gps_data)), :].reset_index(drop=True)

# Об'єднання даних
merged_data = pd.concat([gps_data, road_data, accel_data], axis=1).dropna()

# Візуалізація стану дороги
plt.figure(figsize=(10, 5))
sns.countplot(data=merged_data, x="road_condition", hue="road_condition", palette="coolwarm", legend=False)
plt.title("Розподіл стану дорожнього покриття")
plt.xlabel("Стан дороги")
plt.ylabel("Кількість вимірювань")
plt.savefig("road_condition_distribution.png")
plt.close()

# Візуалізація акселерометричних даних
plt.figure(figsize=(12, 6))
plt.plot(merged_data["x"], label="X", alpha=0.7)
plt.plot(merged_data["y"], label="Y", alpha=0.7)
plt.plot(merged_data["z"], label="Z", alpha=0.7)
plt.title("Дані акселерометра")
plt.xlabel("Час")
plt.ylabel("Прискорення")
plt.legend()
plt.savefig("accelerometer_data.png")
plt.close()

# Теплова карта проблемних ділянок
m = folium.Map(location=[gps_data["latitude"].mean(), gps_data["longitude"].mean()], zoom_start=12)
heat_data = [[row["latitude"], row["longitude"]] for _, row in merged_data[merged_data["road_condition"] == "pothole"].iterrows()]
HeatMap(heat_data).add_to(m)
m.save("road_heatmap.html")

# Гістограма прискорень
plt.figure(figsize=(10, 5))
sns.histplot(merged_data["x"], kde=True, color="blue", label="X")
sns.histplot(merged_data["y"], kde=True, color="red", label="Y")
sns.histplot(merged_data["z"], kde=True, color="green", label="Z")
plt.title("Гістограма значень акселерометра")
plt.xlabel("Прискорення")
plt.ylabel("Кількість")
plt.legend()
plt.savefig("acceleration_histogram.png")
plt.close()

# Лінійний графік середнього прискорення за станом дороги
plt.figure(figsize=(10, 5))
avg_accel = merged_data.groupby("road_condition")[["x", "y", "z"]].mean()
avg_accel.plot(kind="bar", figsize=(10, 5))
plt.title("Середнє значення прискорення за типом покриття")
plt.xlabel("Стан дороги")
plt.ylabel("Середнє прискорення")
plt.legend(["X", "Y", "Z"])
plt.savefig("avg_acceleration_by_road_condition.png")
plt.close()

# Тренди зміни стану дорожнього покриття
plt.figure(figsize=(12, 5))
plt.plot(merged_data.index, merged_data["road_condition"].astype("category").cat.codes, marker="o", linestyle="-")
plt.title("Динаміка зміни стану дорожнього покриття")
plt.xlabel("Час (записи)")
plt.ylabel("Стан дороги (коди)")
plt.savefig("road_condition_trend.png")
plt.close()

# Теплова карта інтенсивності вібрацій
m_vibration = folium.Map(location=[gps_data["latitude"].mean(), gps_data["longitude"].mean()], zoom_start=12)
heat_vibration = [[row["latitude"], row["longitude"], abs(row["x"]) + abs(row["y"]) + abs(row["z"])] for _, row in merged_data.iterrows()]
HeatMap(heat_vibration).add_to(m_vibration)
m_vibration.save("vibration_heatmap.html")

# Кореляція між станом дороги і прискореннями
plt.figure(figsize=(10, 5))
numeric_data = merged_data.select_dtypes(include=["number"])  # Виключаємо текстові колонки
sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Кореляція між параметрами")
plt.savefig("correlation_matrix.png")
plt.close()

# Середня швидкість зміни прискорень
plt.figure(figsize=(10, 5))
delta_accel = merged_data[["x", "y", "z"]].diff().abs().mean()
delta_accel.plot(kind="bar", color=["blue", "red", "green"])
plt.title("Середня швидкість зміни прискорення")
plt.xlabel("Ось")
plt.ylabel("Середня зміна прискорення")
plt.savefig("acceleration_change_rate.png")
plt.close()

# Розподіл точок збору GPS-даних
m_gps = folium.Map(location=[gps_data["latitude"].mean(), gps_data["longitude"].mean()], zoom_start=12)
for _, row in gps_data.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=3, color="blue").add_to(m_gps)
m_gps.save("gps_data_distribution.html")

print("✅ Аналітичні дашборди створені. Графіки збережені у файлах, карти збережені в 'road_heatmap.html', 'vibration_heatmap.html' та 'gps_data_distribution.html'")
