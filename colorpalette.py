import matplotlib.pyplot as plt
from config import *
from PIL import Image, ImageDraw, ImageFont

# exporting the colormap as image

items = list(colormap.items())
height = 10
spacing = 1.2
palette = Image.new("RGB", (height * 20, round(len(items) * height * spacing)), (255,255,255))
drawPalette = ImageDraw.Draw(palette)
for i in range(0,len(items)):
    red, green, blue = bytes.fromhex(items[i][1])
    
    y = round(height * i * spacing)

    drawPalette.rectangle(
        (0,y,height,y + height),
        (red,green,blue)
    )

    drawPalette.text((height * 2,y),items[i][0],fill=(0,0,0))

plt.imshow(palette)
plt.savefig("out/palette.png")