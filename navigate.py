from PIL import Image, ImageDraw, ImageFont
from mandelbrot import mandelbrot, MAX_ITER
from collections import defaultdict
from math import floor, ceil

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t


# Image size (pixels)
WIDTH = 800
HEIGHT = 600

def naviLoop():
    while True:
        print("Enter X: ", end = '')
        x = eval(input())
        print("Enter Y: ", end = '')
        y = eval(input())
        navigate(x, y, True)

def navigate(x, y, crossHairs, times = 3):
    printZooms(x, y, 1, times, crossHairs, 4)
    print()
    print("#######################################################")
    print("######################## Done #########################")
    print("#######################################################")
    

# Set the x,y start end points based on the center pixel
def getPoints(x, y, xSpread):
    x1 = x - xSpread / 2
    x2 = x + xSpread / 2
    
    ySpread = xSpread * .75
    y1 = y - ySpread / 2
    y2 = y + ySpread / 2

    points = (x1,y1,x2,y2)
    return points, xSpread, ySpread



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
def printZooms(x, y, Zstart, Ztimes, crossHairs, mag = 2,):
    zoomList = getZooms(Zstart, Ztimes, mag)
    counter = 1
    for i in zoomList:
        printChart(x, y, i, crossHairs, counter)
        counter +=1
    
    
def printChart(X, Y, zoom, crossHairs, counter=1):
    crossHairs = crossHairs
    points, xSpread, ySpread = getPoints(X, Y, zoom)
    printZoom = str(int(1 / zoom))
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
            
    # stuff for printing        
    font1 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMono.ttf", 48)
    font2 = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono.ttf", 12)
    res = str(WIDTH)+"x"+str(HEIGHT)
    numbersCounted = str(WIDTH * HEIGHT)
    iterations = str(MAX_ITER)
    if xSpread < 1:
        precision = str(len(str(xSpread))-2)
    else: precision = str(1)
    name = 'navi-'+printZoom+'x-'+str(counter)+'.png'
    details = "File Name: "+name+\
              " | Resolution: "+res+\
              " | Zoom: "+printZoom+"x"+\
              " | Numbers tested: "+numbersCounted
    coordinates = "X: "+str(X)+"  Y: "+str(Y)+\
              "    Precision: "+precision
    spreads = "X Spread: "+str(xSpread)+"   Y Spread: "+str(ySpread)
    
    print("Name: "+name)
    print(details)
    print(coordinates)
    print("\n#######################################################")
    draw.rectangle((0, 0, WIDTH, 28), outline='black', fill='black')
    #Cross Hairs
    if crossHairs: draw.text((WIDTH/2, HEIGHT/2),"+",(0,0,255), font=font1)
    draw.text((4,0),details, (0,0,255), font=font2)
    draw.text((4,14),"Coordinates: "+coordinates, (0,0,255), font=font2 )
    
    im.convert('RGB').save(name, 'PNG')
  

# printZooms takes 6 args:
#         (x, y, initial zoom, images, crossHairBool, mag-optional)
#printZooms(-.749, .149, 1, 16, False, 4)

naviLoop()
#navigate(-1.1883, 0.242, 3)

#printChart(-1.1883, 0.242, .25, False)
'''
Cool Locations:

X: -1.1883  Y: 0.242
X: -0.749  Y: 0.149 


'''
