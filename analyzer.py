# %%

import math
from turtle import color
import polars as pl#
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime,date,time
import matplotlib.pyplot as plt
from config import *

# %%

# Read the data from data.csv
df = pl.read_csv('data.csv', parse_dates=True).select([
        pl.col("Client").alias("client"),
        pl.col("Project").alias("project"),
        pl.col("Description").alias("desc"),
        pl.col("Start date").alias("start_date"),
        pl.col("Start time").alias("start_time"),
        pl.col("End date").alias("end_date"),
        pl.col("End time").alias("end_time"),
        pl.col("Duration").cast(pl.Duration).alias("duration"),
        pl.col("Tags").str.split(",").alias("tags"),
    ]
)

print(df)

# %%
df = df.filter(
    (pl.col("start_date") >= start_date) & (pl.col("end_date") <= end_date),
).sort(["start_date","start_time"])

def getPixelForTime(time):
    minute = time.hour*60 + time.minute + time.second / 60
    return round(
        minute * pixelsPerHour / 60 -
        (min(reducedHours[1],max(time.hour,reducedHours[0])) - reducedHours[0]) 
        * (pixelsPerHour - pixelsPerReducedHour)
    )

def findColor(row):
    return colormap.get(row.project) or (colormap.get(row.tags[0]) if row.tags and row.tags[0] in colormap else None) or colormap.get(row.client) or colormap['__default'] 

# %%
if __name__ == '__main__':
    img = Image.new("RGB", (sizeX,sizeY), (255,255,255))
    draw = ImageDraw.Draw(img)

    for row in df.iterrows(named=True):

        dayIndex = (row.start_date - start_date).days
        y = (dayIndex // 7 ) * dayHeight
        xDay = (dayIndex % 7) * pixelsPerDay
        
        minX = xDay + getPixelForTime(row.start_time)
        maxX = xDay + getPixelForTime( row.end_time if row.end_date == row.start_date else time(23,59,00)  )
        
        
        red, green, blue = bytes.fromhex(findColor(row))

        draw.rectangle((minX,y, maxX+1, y + dayHeight - 1),  fill=(red,green,blue))

        if row.end_date != row.start_date and row.end_date <= end_date:
            dayIndex += 1
            y = (dayIndex // 7 ) * dayHeight
            xDay = (dayIndex % 7) * pixelsPerDay
            minX = xDay
            maxX = xDay + getPixelForTime(row.end_time)
            draw.rectangle((minX,y, maxX+1, y + dayHeight - 1),  fill=(red,green,blue))


    im = plt.imshow(img)
    with open("out/out.bmp", "wb") as f:
        img.save(f)
    plt.show()
# %%

