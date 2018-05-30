import machine
import ubinascii
from simple import MQTTClient
from machine import Pin

# Configuracion de pines GPIO para salida
led = Pin(16, Pin.OUT)
pin = Pin(2, Pin.OUT)

# Diccionario con los parametros de configuracion del servidor MQTT
CONFIG = {
#test.mosquitto.org
#iot.eclipse.org
    "MQTT_BROKER": "iot.eclipse.org",
    "USER": "",
    "PASSWORD": "",
    "PORT": 1883,
    "TOPIC": b"test",
    # Identificador unico del chip
    "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}
#Creamos una intancia de network.STA_IF, statation interface
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('conectando a la red...')
        sta_if.active(True)
        sta_if.connect('Xnf25', 't3z25Y.+')
        #sta_if.connect('LA ESQUINA', 'LRE01486')
        while not sta_if.isconnected():
            pass
    print('Configuracion de red:', sta_if.ifconfig())

# Funcion para manejar la informacion recibida
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))

    if msg == b"on":
        pin.off()
        led.on()
    elif msg == b"off":
        pin.on()
        led.off()


def listen():
    # Creamos una instancia de MQTTClient
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'],
                        port=CONFIG['PORT'])
    # Vinculamos un call back Handler que es la funcion que se llamara al recivir un mensaje
    client.set_callback(onMessage)
    client.connect()
    client.publish("test", "ESP8266 is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))

    try:
        while True:
            msg = client.wait_msg()
            # msg = (client.check_msg())
    finally:
        client.disconnect()

do_connect()
listen()
