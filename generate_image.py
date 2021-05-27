from PIL import Image, ImageFont, ImageDraw, ImageOps
import math 
from math import sin, cos, radians
import numpy as np

def clockhand(angle, length):
   """
   Calculate the end point for the given vector.
   Angle 0 is 12 o'clock, 90 is 3 o'clock.
   Based around (32,32) as origin, (0,0) in top left.
   """
   offset = 224

   radian_angle = math.pi * angle / 180.0
   x = offset + length * math.cos(radian_angle)
   y = offset + length * math.sin(radian_angle)

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
   offset = 224
   offset2 = 220

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
   offset = 204
   offset2 = 170
   offset3 = 0

   radian_angle = math.pi * angle / 180.0
   x = int(offset + offset2 * math.cos(radian_angle))
   y = int(offset + offset2 * math.sin(radian_angle))

   sX = int(x-offset3 * math.cos(radian_angle))
   sY = int(y-offset3 * math.sin(radian_angle))


   return (sX,sY)

def hourFromAngle(angle):
    angle *= -1
    result = 3 - (1/30) * (angle % 360)
    
    if(result < 0):
        result += 12

    if(result == 0):
        result = 12

    if(result < 10):
        return " " + str(int(result))


    return str(int(result))


def generateImage(angle, colors, type="P"):
    colourForeground = colors[0]
    colourBackground = colors[1]
    colourSpecial = colors[2]

    numberFont = ImageFont.truetype(r'RobotoMono-Bold.ttf', 30)

    img = Image.new(type, (600, 448), colourBackground)

    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, 446, 446), fill = None, outline = colourForeground, width=2)
    draw.ellipse((30, 30, 418, 418), fill = None, outline = colourForeground, width=2)

    triangle = [(224, 184), (284, 204),(284, 264), (224, 284), (10,224)]

    draw.polygon(rotate_point(triangle, angle+90, (224,224)), fill = colourSpecial)

    for x in np.arange(1, 361, 0.5):
        if( (x % 30) == 0):
            draw.line(tick(x, 26), fill=colourForeground, width=5) # Hour Ticks
            draw.text(number(x), hourFromAngle(x), colourForeground, font=numberFont)

        if((x % 7.5) == 0 and (x % 30) != 0):        
            draw.line(tick(x, 26), fill=colourForeground, width=2) # Ticks

    return img

if __name__ == "__main__":
    image = generateImage(0, ["WHITE","BLACK","RED"], "RGB")
    image.save("image.png")
