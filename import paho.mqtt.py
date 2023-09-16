import paho.mqtt.client as mqtt

# הגדרת הברוקר MQTT
mqtt_broker_address = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic_weight = "smart_bins/weight"
mqtt_topic_infrared = "smart_bins/infrared"

# פונקציה לטיפול בהודעות MQTT מחיישן משקל
def on_weight_message(client, userdata, message):
    weight_value = float(message.payload.decode())
    print(f"Received weight sensor data: {weight_value} lux")
    # כאן תוכל להוסיף פעולות נוספות בהתאם למידע מחיישן משקל

# פונקציה לטיפול בהודעות MQTT מחיישן אינפרה
def on_infrared_message(client, userdata, message):
    infrared_value = bool(int(message.payload.decode()))
    print(f"Received infrared sensor data: {infrared_value}")
    # כאן תוכל להוסיף פעולות נוספות בהתאם למידע מחיישן אינפרה

# התחברות לברוקר
client = mqtt.Client("SmartApp")
client.connect(mqtt_broker_address, mqtt_port)

# הרשמה לקבלת הודעות מחיישנים
client.subscribe([(mqtt_topic_weight, 0), (mqtt_topic_infrared, 0)])
client.message_callback_add(mqtt_topic_weight, on_weight_message)
client.message_callback_add(mqtt_topic_infrared, on_infrared_message)

# השארת האפליקציה פועלת
print("אפליקציה חכמה מחכה לנתונים מהפחים...")
client.loop_forever()
