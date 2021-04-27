from PIL import Image, ImageFont, ImageDraw, ImageOps
from inky import InkyWHAT
from datetime import datetime, timedelta
import math
import numpy as np
import json
import ifaddr
from requests import get


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def clockhand(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 150

   radian_angle = math.pi * (angle-90) / 180.0
   x = offset + length * math.cos(radian_angle)
   y = offset + length * math.sin(radian_angle)
   return [(offset,offset),(x,y)]

def tick(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 150

   radian_angle = math.pi * angle / 180.0
   x = int(offset + 110 * math.cos(radian_angle))
   y = int(offset + 110 * math.sin(radian_angle))

   sX = int(x-length * math.cos(radian_angle))
   sY = int(y-length * math.sin(radian_angle))


   return [(sX,sY),(x,y)]

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

def setDisplayTimer(settings):
    deviceRef.update(
        { 
            "last-update-start": datetime.now().isoformat()
        }
    )
   
    colourBackground = inky_display.WHITE
    colourForeground = inky_display.BLACK

    if(settings["dark-mode"]):
        colourBackground = inky_display.BLACK
        colourForeground = inky_display.WHITE

    colourSpecial = inky_display.RED

    inky_display.set_border(colourBackground)

    img = Image.new("P", (300, 400), colourBackground)

    draw = ImageDraw.Draw(img)
    draw.ellipse((30, 30, 270, 270), fill = None, outline = colourForeground, width=5)

    now = datetime.fromisoformat(settings["wanted-time"])
    angles_h = now.hour * 30 + now.minute / 2

    draw.line(clockhand(angles_h, 120), fill=colourSpecial, width=10) # Hand.

    for x in np.arange(1, 361, 0.5):
        if((x % 30) == 0):
            draw.line(tick(x, 10), fill=colourForeground, width=5) # Hour Ticks
            draw.text(np.subtract(clockhand(x, 137)[1],(14,22)), str(int(x/30)), colourForeground, font=fontM)

        if((x % 7.5) == 0 and (x % 30) != 0):        
            draw.line(tick(x, 5), fill=colourForeground, width=3) # Ticks

        #if((x % 7.5) == 0):     
        #    draw.line(clockhand(x, 120), fill=colourSpecial, width=3) # Hand.   

    draw = ImageDraw.Draw(img)
    #draw.text((5, 300),"P:"+ str(now.hour) .zfill(2) +":" + str(now.minute).zfill(2), colourForeground, font=font)
    draw.text((25, 290),"e-PARK", colourForeground, font=fontL)
    draw.text((5, 380),"PATENT PENDING", colourForeground, font=fontS)

    img = img.transpose(Image.ROTATE_270)
    inky_display.set_image(img)
    inky_display.show()

    #img.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0])
    #img.save("image.png")

    deviceRef.update(
        { 
            "last-update-done": datetime.now().isoformat(),
            "last-set-time": now.isoformat()
        }
    )

def stream(message):
    if(message.path == "/dark-mode"):
        settings["dark-mode"] = message.data

    if(message.path == "/wanted-time"):
        settings["wanted-time"] = message.data

    setDisplayTimer(settings)

# Use the application default credentials
cred = credentials.Certificate("digital-parking-disc-firebase-adminsdk-z50m3-168434f695.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://digital-parking-disc-default-rtdb.europe-west1.firebasedatabase.app/'
})


serial = getserial()

adapters = ifaddr.get_adapters()
ips = []

for adapter in adapters:
    for ip in adapter.ips:
        ips.append({ "name": adapter.name, "ip:": ip.ip, "subnet": ip.network_prefix })

wanip = get('https://api.ipify.org').text

deviceRef = db.reference("devices").child(serial)

deviceRef.update(
        { 
            "last-boot": datetime.now().isoformat(),
            "network-adapters": ips,
            "public-ip": wanip
        }
    )

fontL = ImageFont.truetype(r'RobotoMono-VariableFont_wght.ttf', 70)
fontM = ImageFont.truetype(r'RobotoMono-VariableFont_wght.ttf', 30)
fontS = ImageFont.truetype(r'RobotoMono-VariableFont_wght.ttf', 10)

settingsRef = deviceRef.child("settings")
settings = settingsRef.get()
print(settings)

if(settings == None):
    settings = {}

inky_display = InkyWHAT('red')

if("wanted-time" not in settings):
    nowTmp = datetime.now().__add__(timedelta(hours=1))
    now = ceil_dt(nowTmp, timedelta(minutes=15))
    settings["wanted-time"] = now.isoformat()

#setDisplayTimer(settings)

print("Handing over to settings Stream")
settingsRef.listen(stream)
