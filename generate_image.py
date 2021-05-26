from PIL import Image, ImageFont, ImageDraw, ImageOps
import math 
from math import sin, cos, radians
import numpy as np
import scipy


def clockhand(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 150

   radian_angle = math.pi * angle / 180.0
   x = offset + length * math.cos(radian_angle)
   y = offset + length * math.sin(radian_angle)

   print([(offset+30,offset),(offset-30,offset),(x,y)])
   return [(offset+30,offset),(offset-30,offset),(x,y)]

def rotate_point(points, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point s.o that center_point becomes the origin
    result = []
    for point in points:
        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                    new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
        # Reverse the shifting we have done
        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
        result.append(new_point)
    return result

def tick(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 150
   offset2 = 149

   radian_angle = math.pi * angle / 180.0
   x = int(offset + offset2 * math.cos(radian_angle))
   y = int(offset + offset2 * math.sin(radian_angle))

   sX = int(x-length * math.cos(radian_angle))
   sY = int(y-length * math.sin(radian_angle))


   return [(sX,sY),(x,y)]

def number(angle):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 140
   offset2 = 15

   radian_angle = math.pi * angle / 180.0
   x = int(offset + 120 * math.cos(radian_angle))
   y = int(offset + 120 * math.sin(radian_angle))

   sX = int(x-offset2 * math.cos(radian_angle))
   sY = int(y-offset2 * math.sin(radian_angle))


   return (sX,sY)

def hourFromAngle(angle):
    angle += 180
    result = 3 - (1/30) * (angle % 360)

    if(result < 0):
        result += 12

    if(result == 0):
        result = 12

    if(result < 10):
        return " " + str(int(result))

    return str(int(result))


colourBackground = 'white'
colourForeground = 'black'
colourSpecial = 'red'

font = ImageFont.truetype(r'RobotoMono-VariableFont_wght.ttf', 40)
numberFont = ImageFont.truetype(r'RobotoMono-Bold.ttf', 17)

img = Image.new("RGB", (300, 400), colourBackground)

draw = ImageDraw.Draw(img)
draw.ellipse((1, 1, 298, 298), fill = None, outline = colourForeground, width=2)
draw.ellipse((30, 30, 270, 270), fill = None, outline = colourForeground, width=2)

triangle = [(120, 150), (140, 120), (160, 120), (180, 150), (150, 285)]

draw.polygon(rotate_point(triangle, 90, (150,150)), fill = colourSpecial)

for x in np.arange(1, 361, 0.5):
    if( (x % 30) == 0):
        draw.line(tick(x, 30), fill=colourForeground, width=5) # Hour Ticks
        draw.text(number(x), hourFromAngle(x), colourForeground, font=numberFont)

    if((x % 7.5) == 0 and (x % 30) != 0):        
        draw.line(tick(x, 30), fill=colourForeground, width=2) # Ticks

draw = ImageDraw.Draw(img)

img = img.transpose(Image.ROTATE_90)

img.save("image.png")