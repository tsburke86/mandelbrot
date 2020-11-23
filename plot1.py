from PIL import Image, ImageDraw
from mandelbrot import mandelbrot, MAX_ITER
from collections import defaultdict
from math import floor, ceil

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t
'''
def getPoints(x1,x2,y1):
    xd = abs( abs(x1) - abs(x2))
    if xd == 0 and x1 != x2: 
        yd = .75
    else: yd = xd * .75

    y2 = y1 + yd
    points = (x1,y1,x2,y2)
    return points
'''
def getPoints(x, y, xSpread):
    x1 = x - xSpread / 2
    x2 = x + xSpread / 2
    
    ySpread = xSpread * .75
    y1 = y - ySpread / 2
    y2 = y + ySpread / 2

    points = (x1,y1,x2,y2)
    return points

# Image size (pixels)
WIDTH = 1200
HEIGHT = 800
'''
# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1
'''

def getZooms(start, times):
    zoomList = [start]
    for i in range(times -1 ):
        start = start / 2
        zoomList.append(start)
    return zoomList
        
'''
# set points 
points = getPoints(-.749, .149, .25)

start = (points[0], points[1] )
end =   (points[2], points[3] )
RE_START = start[0]
IM_START = start[1]
RE_END = end[0]
IM_END = end[1]

# print Actions
print("Creating file")
print("Width: "+str(WIDTH)+" Height: "+str(HEIGHT))
print(points)
'''
def printZooms(x, y, Zstart, Ztimes):
    zoomList = getZooms(Zstart, Ztimes)
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

    
printZooms(-.749, .149, 1, 16)
print()
print("######################## Done #########################")
print("######################## Done #########################")
print("######################## Done #########################")
print("######################## Done #########################")
print("######################## Done #########################")
print("######################## Done #########################")
