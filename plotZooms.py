from PIL import Image, ImageDraw
from mandelbrot import mandelbrot, MAX_ITER
from collections import defaultdict
from math import floor, ceil

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t


# Image size (pixels)
WIDTH = 1200
HEIGHT = 800

# Set the x,y start end points based on the center pixel
def getPoints(x, y, xSpread):
    x1 = x - xSpread / 2
    x2 = x + xSpread / 2
    
    ySpread = xSpread * .75
    y1 = y - ySpread / 2
    y2 = y + ySpread / 2

    points = (x1,y1,x2,y2)
    return points



# Set the amount of images and their zoom ratio
# default zoom increase is mag=2

def getZooms(start, times, mag):
    zoomList = [start]
    for i in range(times -1 ):
        start = start / mag
        zoomList.append(start)
    return zoomList

# Print as many images as Ztimes.
# mag is the amount (times) to magnify each time.
#      - So mag = 2 means is gets twice as big each time
def printZooms(x, y, Zstart, Ztimes, mag = 2):
    zoomList = getZooms(Zstart, Ztimes, mag)
    counter = 1
    for i in zoomList:
        printChart(x, y, i, counter)
        counter +=1
    
    
def printChart(x, y, zoom, counter=1):
    points = getPoints(x, y, zoom)
    start = (points[0], points[1] )
    end =   (points[2], points[3] )
    RE_START = start[0]
    IM_START = start[1]
    RE_END = end[0]
    IM_END = end[1]
    
    histogram = defaultdict(lambda: 0)
    values = {}
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            # Compute the number of iterations
            m = mandelbrot(c)
            
            values[(x, y)] = m
            if m < MAX_ITER: # Test
            #if m < MAX_ITER - (MAX_ITER * .1): # Test
                histogram[floor(m)] += 1

    total = sum(histogram.values())
    hues = []
    h = 0
    for i in range(MAX_ITER):
        h += histogram[i] / total
        hues.append(h)
    hues.append(h)
     
    im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            m = values[(x, y)]
            # The color depends on the number of iterations    
            hue = 255 - int(255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1))
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))
            
    name = 'output-'+str(counter)+'-'+str(zoom)+'x.png'
    im.convert('RGB').save(name, 'PNG')
    print("\nsaved file: "+name)

# printZooms takes 5 args:
#         (x, y, initial zoom, images, mag-optional)
printZooms(-.749, .149, 1, 16, 4)
print()
print("#######################################################")
print("######################## Done #########################")
print("#######################################################")
