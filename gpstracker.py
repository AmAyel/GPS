from machine import Pin, UART, I2C
import utime, time
import machine
import time
import micropyGPS
from ssd1306 import SSD1306_I2C          
from micropyGPS import MicropyGPS

led_pin = machine.Pin(14, machine.Pin.OUT)

# Inicializa el objeto micropyGPS
gps = micropyGPS.MicropyGPS(9, 'dd')

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

modulo_gps = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

Zona_Horaria = -3
gps = MicropyGPS(Zona_Horaria)

def convertir(secciones):
    if (secciones[0] == 0): # secciones[0] contiene los grados
        return None
    # secciones[1] contiene los minutos    
    data = secciones[0]+(secciones[1]/60.0)
    # secciones[2] contiene 'E', 'W', 'N', 'S'
    if (secciones[2] == 'S'):
        data = -data
    if (secciones[2] == 'W'):
        data = -data

    data = '{0:.6f}'.format(data) # 6 digitos decimales
    return str(data)

while True:
    largo = modulo_gps.any()
    if largo > 0:
        b = modulo_gps.read(largo)
        for x in b:
            msg = gps.update(chr(x))
    
    latitud = convertir(gps.latitude)
    longitud = convertir(gps.longitude)
    
    if (latitud == None or longitud == None):
        oled.fill(0)
        oled.text("Datos no", 35, 25)
        oled.text("disponibles", 22, 40)
        oled.show()
        continue
    
    t = gps.timestamp
    #t[0] => horas : t[1] => minutos : t[2] => segundos
    horario = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    
    
    oled.fill(0)
    oled.text('Satelites: ' + str(gps.satellites_in_use), 10, 0)
    oled.text('Lat:'+ latitud, 0, 18)
    oled.text('Lon:'+ longitud, 0, 36)
    oled.text('Horario:'+ horario, 0, 54)
    oled.show()

