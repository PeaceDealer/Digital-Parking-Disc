from PIL import Image, ImageFont, ImageDraw
import math
import time

def clockhand(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 100

   radian_angle = math.pi * angle / 180.0
   x = offset + length * math.cos(radian_angle)
   y = offset + length * math.sin(radian_angle)
   return [(offset,offset),(x,y)]

def tick(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 100

   radian_angle = math.pi * angle / 180.0
   x = int(offset + 75 * math.cos(radian_angle))
   y = int(offset + 75 * math.sin(radian_angle))

   sX = int(x-length * math.cos(radian_angle))
   sY = int(y-length * math.sin(radian_angle))


   return [(sX,sY),(x,y)]

img = Image.new("RGB", (400, 300), (255, 255, 255))

draw = ImageDraw.Draw(img)
draw.ellipse((20, 20, 180, 180), fill = 'white', outline ='black', width=3)

baseLength = 80
#draw.line(clockhand(0, baseLength + 0), fill='red', width=3) # Minute hand.
draw.line(clockhand(90, baseLength + 0), fill='red', width=3) # Minute hand.

for x in range(360):
    if( (x % 30) == 0):
        print("drawing tick at " + str(x))
        draw.line(tick(x, 7), fill='black', width=3) # Hour Ticks

    if((x % 10) == 0 and (x % 30) != 0):
        print("drawing tick at " + str(x))
        draw.line(tick(x, 2), fill='black', width=1) # Hour Ticks
 

img.save("image.png", "PNG")