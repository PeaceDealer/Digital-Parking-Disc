from PIL import Image
from inky.inky_uc8159 import Inky
from datetime import datetime, timedelta
import numpy as np
import ifaddr
from requests import get
from generate_image import generateImage

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import RPi.GPIO as GPIO

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

    now = datetime.fromisoformat(settings["wanted-time"])
    angles_h = now.hour * 30 + now.minute / 2

    print(angles_h)
    img = generateImage(angles_h, [colourForeground, colourBackground, colourSpecial])

    #img = img.transpose(Image.ROTATE_90)
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

settingsRef = deviceRef.child("settings")
settings = settingsRef.get()
print(settings)

if(settings == None):
    settings = {}

inky_display = Inky()

if("wanted-time" not in settings):
    nowTmp = datetime.now().__add__(timedelta(hours=1))
    now = ceil_dt(nowTmp, timedelta(minutes=15))
    settings["wanted-time"] = now.isoformat()
    settingsRef.update(settings)

#setDisplayTimer(settings)

BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'C', 'D']
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def process_button(label):
    if(label == 'A'):
        print("setting time to now")
        print(settings)
        nowTmp = datetime.now().__add__(timedelta(hours=1))
        now = ceil_dt(nowTmp, timedelta(minutes=15))
        settings["wanted-time"] = now.isoformat()
        print(settings)

    if(label == 'B'):
        print("adding 15 minutes to timer")
        print(settings)
        now = datetime.fromisoformat(settings["wanted-time"])
        now = now + timedelta(minutes=15)
        settings["wanted-time"] = now.isoformat()
        print(settings)

    if(label == 'C'):
        print("adding 1 hour to timer")
        print(settings)
        now = datetime.fromisoformat(settings["wanted-time"])
        print(now)
        now = now + timedelta(hours=1)
        print(now)
        settings["wanted-time"] = now.isoformat()
        print(settings)

    if(label == 'D'):
        print("Push Time Update")
        print(inky_display.busy_pin)
        print(settings)
        #if not connected
        setDisplayTimer(settings)
        #else
        #settingsRef.update(settings)

def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    process_button(label)

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)


print("Handing over to settings Stream")
settingsRef.listen(stream)
