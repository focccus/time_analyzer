

from datetime import date

# date range
start_date = date(2022,6,6)
end_date = date(2023,1,1)

weeks = (end_date - start_date).days // 7

# vertical pixels per day
dayHeight = 128
# hour range which get less pixels
reducedHours = (2,7)
reducedHourCount = reducedHours[1] - reducedHours[0]
# horizontal pixels per normal hour
pixelsPerHour = 60 // 3
# horizontal pixels per reduced hour
pixelsPerReducedHour = 60 // 10

# total pixels per day
pixelsPerDay = (24 - reducedHourCount) * pixelsPerHour + reducedHourCount * pixelsPerReducedHour
sizeX = pixelsPerDay * 7
sizeY = dayHeight * (weeks + 1)

# mapping tag, project or client to a hex color code
colormap = {
    'Lecture': '1ab7ff',
    'Homework': '005780',
    'Social': '356013',
    '__default': '606060' # used if no other match is found
}