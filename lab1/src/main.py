from paho.mqtt import client as mqtt_client
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.parking_schema import ParkingSchema
from file_datasource import FileDatasource
import config

def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc) # Stop execution
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client

def publish(client, topic, parking_topic, datasource, delay):
    datasource.startReading()
    while True:
        time.sleep(delay)
        aggregated_data, parking_data = datasource.read()

        if aggregated_data:
            msg = AggregatedDataSchema().dumps(aggregated_data)
            result = client.publish(topic, msg)
            if result[0] == 0:
                print(f"✅ Sent `{msg}` to topic `{topic}`")
            else:
                print(f"❌ Failed to send data to topic {topic}")

        if parking_data:
            parking_msg = ParkingSchema().dumps(parking_data)
            result = client.publish(parking_topic, parking_msg)
            if result[0] == 0:
                print(f"✅ Sent `{parking_msg}` to topic `{parking_topic}`")
            else:
                print(f"❌ Failed to send data to topic {parking_topic}")

def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Infinity publish data
    publish(client, config.MQTT_TOPIC, config.MQTT_TOPIC_PARKING, datasource, config.DELAY)

if __name__ == '__main__':
    run()