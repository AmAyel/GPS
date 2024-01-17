import network
import time
import socket
from machine import Pin, I2C
from time import sleep_ms
from ssd1306 import SSD1306_I2C
from micropyGPS import MicropyGPS 
import bme280
import framebuf
import machine

i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
bme = bme280.BME280(i2c=i2c)

temp = bme.values[0]
pres = bme.values[1]
hum = bme.values[2]

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#ssid='Totalplay-62A3'
#password='62A3B7C7AWWqh7fA'

ssid='AXTEL_1589D4'
password='68395544'
wlan.connect(ssid,password)

print(wlan.ifconfig())


 # Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    

html = html = """<!DOCTYPE HTML><html>
<head>
  <meta http-equiv=\"refresh\" content=\"10\">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
  integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 2.0rem; }
    p { font-size: 2.0rem; }
    .units { font-size: 1.2rem; }
    .bme-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<div style="background-image:url('https://www3.gobiernodecanarias.org/medusa/mediateca/publicaciones/wp-content/uploads/sites/4/2013/10/paisaje_0212.jpg')">
<body>
  <h2 style="fond-size"750%">Ubicacion actual</h2>
  <div style="text-align:center;padding:1em 0;"> <h3><a style="text-decoration:none;
  " href="https://www.zeitverschiebung.net/es/city/3530597"><span style="color:black;"
  >Hora actual en</span><br />Ciudad de Mexico</a></h3> <iframe src=
  "https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=es&size=medium&timezone=America%2FMexico_City"
  width="100%" height="115" frameborder="0" seamless></iframe> </div>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="bme-labels">Temperatura:</span> 
    <span>"""+str(temp)+"""</span>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="bme-labels">Humedad:</span>
    <span>"""+str(hum)+"""</span>
  </p>
  <p>
    <i class="fas fa-tachometer-alt"></i>
    <span class="bme-labels">Presi&oacute;n:</span>
    <span>"""+str(pres)+"""</span>
  </p>

</body>
</html>"""

print(html)


addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print ('listening on: ', addr)

while True:
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    response = html 
    
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()