# Sensor stuff
import Adafruit_DHT

# Time stuff
import time
import datetime

#Configuration
mqttBrokerHost = "orzhova"
mqttClientId = "bedroom_sensor"
mqttTopic = "bedroom"

#MQTT Stuff
import paho.mqtt.client as mqtt
mqttClient = mqtt.Client(mqttClientId)
print("Connecting to MQTT broker")
mqttClient.connect(mqttBrokerHost)
mqttClient.reconnect_delay_set(1, 120)
mqttClient.loop_start();
print("Connection to MQTT broker established")
    
# Sensors
print("Initializing sensors")
pin = 4
DHT_Sensor = Adafruit_DHT.DHT22

print("Initializing variables")
updateSecondsInterval = 5
fasterUpdateInterval = 2

def getTemperatureAndUpdateStuff():
	print("----------------------------------------")
	print("Reading DHT sensor")
	humidity, temperature = Adafruit_DHT.read_retry(DHT_Sensor, pin)
	print("Reading DHT sensor finished")
    
	print('{datetime}: Temp: {temperature} °C - {humidity} %'.format(
		datetime=str(datetime.datetime.now()),
		temperature=temperature,
		humidity=humidity)
	)
	
	if temperature is not None and humidity is not None :
		#Send MQTT publish
		publishTemperature = mqttClient.publish(mqttTopic + "/temperature", round(temperature, 2))
		publishTemperature.wait_for_publish()
		
		publishHumidity =  mqttClient.publish(mqttTopic + "/humidity", round(humidity, 2))
		publishHumidity.wait_for_publish()
		print("MQTT publishes done")
	else:
		raise Exception("Sensor data reading error") 
 
if __name__ == "__main__":
    print("Starting sensor reading loop")
    while True:
        fasterReload = False
        try:
            getTemperatureAndUpdateStuff()
        except Exception as e:
            print(e)
            fasterReload = True
        finally:
            if fasterReload :
                time.sleep(fasterUpdateInterval)
            else:
                time.sleep(updateSecondsInterval)

        
