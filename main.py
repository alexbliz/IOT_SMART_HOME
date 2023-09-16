import random
import time
import paho.mqtt.client as mqtt
import board
import busio


# הגדרת הברוקר MQTT
mqtt_broker_address = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic = "smart_bins"

# פונקציה לשליחת המידע לשרת MQTT
def send_sensor_data(sensor_type, sensor_value):
    client = mqtt.Client(f"SmartBin_{sensor_type}")
    client.connect(mqtt_broker_address, mqtt_port)
    client.publish(f"{mqtt_topic}/{sensor_type}", str(sensor_value))
    client.disconnect()

# סנסור משקל
i2c = busio.I2C(board.SCL, board.SDA)
sensor = BH1750(i2c)
weight_sensor = random.randint(0, 100)  # נתון דמי לצורך הדוגמה

# סנסור אינפרה
ultrasonic_sensor = HCSR04(trigger_pin=board.D2, echo_pin=board.D3)
infrared_sensor = False  # נתון דמי לצורך הדוגמה

while True:
    # קריאה לחיישן משקל ושליחת הערך לשרת MQTT
    weight_value = sensor.lux
    send_sensor_data("weight", weight_value)
    
    # קריאה לחיישן אינפרה ושליחת הערך לשרת MQTT
    try:
        distance = ultrasonic_sensor.distance
        if distance < 10:  # לדוגמה, ערך זה מציין מרחק מינימלי כאשר הזבל הגיע לחלק העליון של הפח
            infrared_sensor = True
        else:
            infrared_sensor = False
    except RuntimeError:
        infrared_sensor = False
    
    send_sensor_data("infrared", infrared_sensor)
    
    time.sleep(10)  # שנייה אחת = 10 שניות
