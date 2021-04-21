from PIL import Image, ImageDraw, __version__

print(__version__)

image = Image.new("P", (300, 300), 0)

draw = ImageDraw.Draw(image)

draw.ellipse((20, 20, 280, 280), fill=None, outline=1, width=5)

image.putpalette([255, 255, 255, 0, 0, 0])

image = image.resize((600, 600), Image.NEAREST)

image.save("test.png")