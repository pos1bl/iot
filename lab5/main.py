import asyncio
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock

from pydantic import BaseModel, field_validator
from lineMapLayer import LineMapLayer
from datasource import Datasource
from file_datasource import FileDatasource


# class Point(BaseModel):
#     latitude: float
#     longitude: float
#     road_state: str


class MapViewApp(App):
    def __init__(self, **kwargs):
        # додати необхідні змінні

        super().__init__()
        self.mapview = None
        self.car_marker = None
        # self.datasource = Datasource(1)
        self.datasource = FileDatasource("gpsdata.csv", "roadstate.csv")
        self.datasource.startReading()


    def on_start(self):
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """
        self.route_layer = LineMapLayer()
        self.mapview.add_layer(self.route_layer, mode="scatter")
        self.car_marker = MapMarker(lat=0, lon=0, source="images/car.png")
        self.mapview.add_widget(self.car_marker)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        """
                Викликається регулярно для оновлення мапи
        """
        new_points = self.datasource.get_new_points()
        for point in new_points:
            self.route_layer.add_point((point[0], point[1]))
            self.update_car_marker(point)
            if point[2] == "pothole":
                self.set_pothole_marker((point[0], point[1]))
            if point[2] == "bump":
                self.set_bump_marker((point[0], point[1]))

    def update_car_marker(self, point):
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """

        self.car_marker.lat = point[0]
        self.car_marker.lon = point[1]

    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """
        # lat, lon = point
        marker = MapMarker(lat=point[0], lon=point[1], source="images/pothole.png")
        self.mapview.add_widget(marker)

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліцейського
        :param point: GPS координати
        """
        # lat, lon = point
        marker = MapMarker(lat=point[0], lon=point[1], source="images/bump.png")
        self.mapview.add_widget(marker)

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """

        self.mapview = MapView(zoom=15, lat=50.443, lon=30.512)
        return self.mapview


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
