import time
import ssl
import json
import RPi.GPIO as GPIO
import dht11
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

sensor = dht11.DHT11(pin=17)

aws_endpoint = "aiim54esx7tpq-ats.iot.eu-north-1.amazonaws.com"
aws_port = 8883
cert_path = "/home/raspberry/certs/"

ca_path = cert_path + "AmazonRootCA1.pem"
cert_path_crt = cert_path + "91f05bac667df00ead5606057d9626264814292e52a17636f942f58287da5203-certificate.pem.crt"
key_path = cert_path + "91f05bac667df00ead5606057d9626264814292e52a17636f942f58287da5203-private.pem.key"
mqtt_topic = "rpi/sensor"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT bağlantısı başarılı.")
    else:
        print(f"MQTT bağlantısı başarısız, hata kodu: {rc}")

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT bağlantısı başarılı.")
    else:
        print(f"MQTT bağlantı hatası, kod: {rc}")

def on_publish(client, userdata, mid):
    print(f"Mesaj yayınlandı, mid: {mid}")

mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.tls_set(ca_certs=ca_path,
                    certfile=cert_path_crt,
                    keyfile=key_path,
                    tls_version=ssl.PROTOCOL_TLSv1_2)

try:
    mqtt_client.connect(aws_endpoint, aws_port)
    print("MQTT broker bağlantısı başarılı.")
except Exception as e:
    print("MQTT broker bağlantısı başarısız:", e)
    exit(1)

mqtt_client.loop_start()
time.sleep(10)

influx_token = "nLb4FP8OKWK7OX98P5XS8Pwm5ahKaG_sPx7MKatoIb8AFxAzBDC4ovXyj_Qu34TiXcO2SHPrJfuuRRG4xaebcg=="
influx_org = "olcum"
influx_bucket = "sensor"
influx_url = "http://localhost:8086"

client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

try:
    while True:
        result = sensor.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            print(f"Tarih: {timestamp}")
            print(f"Sıcaklık: {temperature}°C")
            print(f"Nem: {humidity}%")

            payload = {
                "timestamp": timestamp,
                "temperature_C": temperature,
                "humidity_percent": humidity
            }

            point = (
                Point("dht11_measurement")
                .field("temperature", temperature)
                .field("humidity", humidity)
            )
            write_api.write(bucket=influx_bucket, org=influx_org, record=point)

            pub_result = mqtt_client.publish(mqtt_topic, json.dumps(payload), qos=1)
            if pub_result.rc == 0:
                print(f"MQTT mesajı yayınlandı: {mqtt_topic}")
            else:
                print(f"MQTT mesajı yayınlanamadı, rc={pub_result.rc}")

        else:
            print("DHT11 verisi geçersiz.")

        time.sleep(15)

except KeyboardInterrupt:
    print("Program sonlandırıldı.")
except Exception as e:
    print("Hata oluştu:", e)
finally:
    GPIO.cleanup()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()