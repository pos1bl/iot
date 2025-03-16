from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.index = 0

    def startReading(self):
        self.accelerometer_data = self._load_csv(self.accelerometer_filename)
        self.gps_data = self._load_csv(self.gps_filename)
        self.parking_data = self._load_csv(self.parking_filename)
        self.index = 0

        print(f"📌 Загружено {len(self.accelerometer_data)} записей акселерометра")
        print(f"📌 Загружено {len(self.gps_data)} записей GPS")
        print(f"📌 Загружено {len(self.parking_data)} записей паркинга")

    def read(self):
        if self.index >= len(self.accelerometer_data) or self.index >= len(self.gps_data) or self.index >= len(self.parking_data):
            print("⚠️ Данні закінчились, повертаємо пустий об'єкт")
            return AggregatedData(Accelerometer(0, 0, 0), Gps(0, 0), datetime.now()),  None

        acc_values = self.accelerometer_data[self.index]
        gps_values = self.gps_data[self.index]
        parking_values = self.parking_data[self.index]
        self.index += 1

        aggregated_data = AggregatedData(
            Accelerometer(float(acc_values[0]), float(acc_values[1]), float(acc_values[2])),
            Gps(float(gps_values[0]), float(gps_values[1])),
            datetime.now(),
        )

        parking_data = Parking(
            int(parking_values[0]),
            Gps(float(parking_values[1]), float(parking_values[2]))
        )

        return aggregated_data, parking_data

    def stopReading(self):
        """Очищаем данные"""
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.index = 0
        print("📌 Чтение данных остановлено")

    def _load_csv(self, filename):
        """Читает CSV-файл и возвращает список строк"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                csv_reader = reader(file)
                next(csv_reader)  # Пропускаем заголовок
                return [row for row in csv_reader if row]
        except FileNotFoundError:
            print(f"❌ Файл {filename} не найден!")
            return []