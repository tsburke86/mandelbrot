from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
from math import floor, ceil

# Iterations
MAX_ITER = 80
# Image size (pixels)
WIDTH = 600
HEIGHT = 400

from math import log, log2

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t

def setMaxIter(oldValue):
    while True:
        print("Enter new Interation Value between 80-500 (currently: "+str(oldValue)+"): ",end='')
        entry = eval(input())
        if 80 <= entry <= 500:
            return entry


def printCommands():
    print()
    print("## COMMANDS ##")
    print("Command | Description |")
    print("--------|--------------")
    print("  X\t| Toggles Cross Hairs")
    print("  +/-\t| zoom in or out by a factor of 2 on the initial image")
    print("  $\t| Sets the max iteration ")
    print("  %N\t| Set the zoom for the initial image to N.")
    print("    \t|  -- Accepts: %1, %128, %256, %512, %1024")
    print()

def printMoves():
    print()
    print("## MOVES ##")
    print()
    print("    W   ",end='\t'); print("\t   8   ")
    print("  Q   E ",end='\t'); print("\t 7   9 ")
    print(" A     D",end='\t'); print("\t4     6")
    print("  Z   C ",end='\t'); print("\t 1   3 ")
    print("    S   ",end='\t'); print("\t   2   ")
    print()
    
def printHelp():
    print()
    print("######################################################")
    print("################ Mandelbort Navigator ################")
    print("######################################################")
    print()
    print("                      HELP MENU")
    print()
    print("##################### MOVEMENTS ######################")
    print()
    print("  Movements can be combined into one string AAAAASSS.\n")
    print("Leaving it blank will print images with any new commands queued. Capital letters move more than lowercase. (D = 0.05, d = 0.0025) The Key pad moves very little. (6 = 0.0001)")
    print()
    printMoves()
    print()
    print(" # Use the Cross Hairs to narrow in with the X command")
    print()
    print("#################### COMMANDS #######################")
    print()
    print("  Commands cannot be combined with movements or other commands.\n")
    print("After issuing a command, you will be prompted to move. You can press Enter to print current position, issue a move and print, or enter another command and repeat.")
    print()
    printCommands()
    print()
    print("Press Enter to Continue")
    one=input()
    one = ''
    print("#######################################################")
    print()
    print()


def printDetails(name, X, Y, xSpread, res, printZoom,
                 iterations, precision, numbersCounted):
    p = '.'+precision+'f'
    fov = str(format(X - xSpread/2,p))+" to "+ str(format(X + xSpread/2,p))
    print("#######################################################")
    print()
    print("File Name: "+name+\
              "\n  Resolution: "+res+\
              "\n  Zoom: "+printZoom+"x"+\
              "\n  Iterations: "+iterations)
    print()
    print("Center Coordinates: X:"+str(X)+" Y:"+str(Y))
    print("X Spread: "+str(xSpread)+" | FOV = "+fov)
    print()
    print("#######################################################")
    
    
def naviLoop():
    
    xMoves = {
        # Big movements
        'E': 0.025, 'e': 0.000125,
        'Z': -0.025, 'z': -0.000125,
        'Q': -0.025, 'q': -0.000125,
        'C': 0.025, 'c': 0.000125,
        'D': 0.05,'d':0.00025,
        'A':-0.05, 'a':-0.00025,

        # Small movements
        '3': 0.0000000525,
        '7': -0.0000000525,
        '9': 0.0000000525,
        '4': -0.0000001,
        '1': -0.0000000525,
        '6': 0.0000001,
        '':0
        }
    yMoves = {
        # Big movements
        'Q': 0.025, 'q': 0.000125,
        'E': 0.025, 'e': 0.000125,
        'Z': -0.025, 'z': -0.000125,
        'W': 0.05, 'w':0.00025,
        'S':-0.05, 's':-0.00025,
        'C': -0.025, 'c': -0.000125,

        # Small movements
        '8': 0.0000001,
        '7': 0.0000000525,
        '9': 0.0000000525,
        '2': -0.0000001,
        '1': -0.0000000525,
        '3': -0.0000000525,
        '':0
        }
    # Set initial coords
    
    x = -0.34515740000000006
    y = -0.6422024999999997

    #zStart = 1
    zStart = .25
    crossHairs = True
    #printHelp()
    print("Generating Images for:",x,y)
    print()
    printZooms(x, y, zStart, 2, crossHairs)
    print("######################## Done #########################")
    print("#######################################################")
    print()
    # Main loop
    commandBool = False
    while True:
        if not commandBool:
            #printMoves()
            printCommands()
            print("#######################################################")
            print()
            print("Enter movement or command (help): ", end = '')
        else:
            print("Commands queued, enter movement or press enter to print: ",end='')
        entry = input()
# Commands
        if entry.upper() == "HELP":
            printHelp();continue

        # Set Iterations
        if entry == "$":
            global MAX_ITER
            MAX_ITER = setMaxIter(MAX_ITER)
            print(" --Max Iterations set to: "+str(MAX_ITER))
            commandBool=True;continue
        # Increase Zoom
        
        if entry == "+":
            zStart /= 2
            print(" --Zoom Start Value changed to: "+str(1 / zStart))
            commandBool=True;continue
        if entry == "-":
            if zStart < 1:
                zStart *= 2
                print(" --Zoom Start Value changed to: "+str(1 / zStart))
                commandBool=True;continue
            else: print(" --Zoom already at 1");continue
        # Toggle Cross Hairs
        if entry == "x" or entry =='X':
            if crossHairs == False:
                crossHairs = True
                print(" --Enabling Cross Hairs")
                commandBool=True;continue
            else:
                crossHairs = False
                print(" --Disabling Cross Hairs")
                commandBool=True;continue
        # Set zoom value
        if entry == "%1":
            zStart = 1
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%128":
            zStart = 1/128
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%256":
            zStart = 1/256
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%512":
            zStart = 1/512
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%1024":
            zStart = 1/1024
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        
            
        xChange = 0
        yChange = 0
        
        for i in entry:
            if i in xMoves:
                xChange += xMoves[i]
            if i in yMoves:
                yChange -= yMoves[i]
        x += xChange
        y += yChange
        commandBool = False
        print("Generating Images for:",x,y)
        print()
        if xChange or yChange: print("Change in X: "+str(xChange)+\
                          "\nChange in Y: "+str(yChange))
        print()
        printZooms(x, y, zStart, 2, crossHairs)
        print("######################## Done #########################")
        print("#######################################################")
        print()
        if xChange or yChange: print("Change in X: "+str(xChange)+\
                          "\nChange in Y: "+str(yChange))
        print()

        

def navigate(x, y, crossHairs, zStart, times = 3):
    printZooms(x, y, zStart, times, crossHairs, 8)
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
def printZooms(x, y, Zstart, Ztimes, crossHairs, mag = 2):    # Change default mag interval
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

     # stuff for printing        
    font1 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMono.ttf", 48)
    font2 = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono.ttf", 12)
    res = str(WIDTH)+"x"+str(HEIGHT)
    numbersCounted = str(WIDTH * HEIGHT)
    iterations = str(MAX_ITER)
    if xSpread < 1:
        precision = str(len(str(xSpread))-2)
    else: precision = str(1)
    #name = 'navi-'+printZoom+'x-'+str(counter)+'.png'
    name = 'navi-'+str(counter)+'.png'
    printDetails(name, X, Y, xSpread, res, printZoom,
                 iterations, precision, numbersCounted)
    # Print Data on Image
    details = "File Name: "+name+\
              " | Resolution: "+res+\
              " | Zoom: "+printZoom+"x"+\
              " | Iterations: "+iterations
    coordinates = "X: "+str(X)+"  Y: "+str(Y)+\
              "    Precision: "+precision
    spreads = "X Spread: "+str(xSpread)+"   Y Spread: "+str(ySpread)
    
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
            
   

    
    #Cross Hairs
    if crossHairs:
        mag1 = .25
        X1 = (WIDTH/2-WIDTH*mag1)
        X2 = (WIDTH/2+WIDTH*mag1)
        Ycenter = HEIGHT/2
        Y1 = HEIGHT/2-HEIGHT *mag1
        Y2 = HEIGHT/2+HEIGHT*mag1
        Xcenter = WIDTH /2
        draw.line((X1, Ycenter, X2, Ycenter), fill=(0,0,255), width = 1)
        draw.rectangle((X1, Y1, X2, Y2), outline = (0,0,255))
        draw.line((Xcenter, Y1, Xcenter, Y2), fill=(0,0,255), width = 1)
        
    # Add Text
    draw.rectangle((0, 0, WIDTH, 28), outline='black', fill='black')
    draw.text((4,0),details, (0,0,255))
    draw.text((4,14),"Coordinates: "+coordinates, (0,0,255))
    
    im.convert('RGB').save(name, 'PNG')
  

# printZooms takes 6 args:
#         (x, y, initial zoom, images, crossHairBool, mag-optional)
#printZooms(-0.3449474, -0.6425525, 1, 16, False, 2)

naviLoop()
#navigate(-1.1883, 0.242, 3)

#printChart(-1.1883, 0.242, .25, False)
#printZooms(-0.3449474, -0.6425525, 1/4, 3, False, 2)


'''
Cool Locations:

X: -1.1883  Y: 0.242
X: -0.749  Y: 0.149 
X:-0.34515734750000004 Y:-0.6422024474999997
X:-0.11640740000000008 Y:-0.6497024999999994

'''
