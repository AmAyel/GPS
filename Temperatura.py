from machine import Pin, I2C
from time import sleep_ms
from ssd1306 import SSD1306_I2C
import bme280
import framebuf
import machine
import time

ANCHO = 128
ALTO = 64
i2c = I2C(1, scl=Pin(19), sda=Pin(18))
oled = SSD1306_I2C(ANCHO, ALTO, i2c)
bme = bme280.BME280(i2c=i2c)

oled.rect(0,0,127,15,1)
oled.rect(0,16,127,47,1)
oled.text("Tiempo",39,4)


while True:
    temp = bme.values[0]
    pres = bme.values[1]
    hum = bme.values[2]
    
    oled.fill_rect(1,17,125,40,0)
    
    oled.text("Temp:", 5, 25)
    oled.text(temp, 45, 25)
    oled.text("Pres:", 5, 35)
    oled.text(pres, 45,35)
    oled.text("Hum:", 5, 45)
    oled.text(hum, 45, 45)
    
    oled.show()
    sleep_ms(500)

  
    


