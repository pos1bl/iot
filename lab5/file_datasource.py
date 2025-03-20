from csv import reader

class FileDatasource:
    def __init__(self, gps_filename: str, road_state_filename: str) -> None:
        self.gps_filename = gps_filename
        self.road_state_filename = road_state_filename
        self.gps_data = []
        self.road_state_data = []
        self.index = 0
        self.counter = 0

    def startReading(self):
        self.gps_data = self._load_csv(self.gps_filename)
        self.road_state_data = self._load_csv(self.road_state_filename)
        self.index = 0

        print(f"📌 Завантажено {len(self.gps_data)} записів GPS")
        print(f"📌 Завантажено {len(self.road_state_data)} записів стану дороги")



    def stopReading(self):
        """Очищуємо дані"""
        self.gps_data = []
        self.road_state_data = []
        self.index = 0
        print("📌 Очистку даних зупинено")

    def _load_csv(self, filename):
        """Читає CSV-файл та повертає список рядків"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                csv_reader = reader(file)
                next(csv_reader)
                return [row for row in csv_reader if row]
        except FileNotFoundError:
            print(f"❌ Файл {filename} не знайдено")
            return []

#get_new_points для роботи зі справжніми даними
    def get_points(self):
        """Повертає список точок GPS та стану дороги у форматі (latitude, longitude, road_state)"""
        points = []
        # Перевіряємо, що кількість записів в GPS і стані дороги однакова
        if len(self.gps_data) == len(self.road_state_data):
            for i in range(len(self.gps_data)):
                try:
                    latitude = float(self.gps_data[i][0])  # Конвертуємо у float
                    longitude = float(self.gps_data[i][1])  # Конвертуємо у float
                    road_state = (self.road_state_data[i][0])  # Беремо перший елемент
                    points.append((latitude, longitude, road_state))
                except ValueError:
                    print(f"⚠️ Некоректні дані в GPS файлі: {self.gps_data[i]}")
        else:
            print("⚠️ Кількість записів в GPS та файлі стану дороги не співпадає.")
        return points

#get_new_points зі штучним обмеженням виданих даних для симуляції реальної роботи застосунку
    def get_new_points(self):
      points = []
      if self.counter < len(self.gps_data):
          for i in range(1):
              if self.counter < len(self.gps_data):
                  try:
                      latitude = float(self.gps_data[self.counter][0])
                      longitude = float(self.gps_data[self.counter][1])
                      road_state = (self.road_state_data[self.counter][0])
                      points.append((latitude, longitude, road_state))
                      self.counter += 1  # Збільшуємо лічильник
                  except ValueError:
                      print(f"⚠️ Некоректні дані в GPS файлі: {self.gps_data[self.counter]}")
      return points
