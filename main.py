from PIL import Image, ImageFont, ImageDraw, ImageOps
from inky import InkyWHAT
from datetime import datetime, timedelta
import math


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
   x = int(offset + 120 * math.cos(radian_angle))
   y = int(offset + 120 * math.sin(radian_angle))

   sX = int(x-length * math.cos(radian_angle))
   sY = int(y-length * math.sin(radian_angle))


   return [(sX,sY),(x,y)]

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

inky_display = InkyWHAT('red')

colourBackground = inky_display.WHITE
colourForeground = inky_display.BLACK
colourSpecial = inky_display.RED

inky_display.set_border(colourBackground)

img = Image.new("P", (300, 400), colourBackground)

draw = ImageDraw.Draw(img)
draw.ellipse((20, 20, 280, 280), fill = None, outline = colourForeground, width=5)

now = ceil_dt(datetime.now(), timedelta(minutes=15))

angles_h = now.hour * 30 + now.minute / 2

print(now)
print(angles_h)

draw.line(clockhand(angles_h, 130), fill=colourSpecial, width=10) # Hand.

for x in range(360):
    if( (x % 30) == 0):
        draw.line(tick(x, 10), fill=colourForeground, width=5) # Hour Ticks

    if((x % 10) == 0 and (x % 30) != 0):
        
        draw.line(tick(x, 5), fill=colourForeground, width=3) # Ticks

font = ImageFont.truetype(r'RobotoMono-VariableFont_wght.ttf', 40)

draw = ImageDraw.Draw(img)
draw.text((41, 300),"P "+ str(now.hour) +":" + str(now.minute).zfill(2), colourForeground, font=font)

img = img.transpose(Image.ROTATE_270)
inky_display.set_image(img)
inky_display.show()

img.putpalette([255, 255, 255, 0, 0, 0, 255, 0, 0])
img.save("image.png")
