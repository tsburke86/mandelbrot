from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
from collections import defaultdict
from math import floor, ceil



from math import log, log2

def mandelbrot(c,m):
    MAX_ITER = m
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
        print("Enter new Interation Value between 5-1000 (currently: "+str(oldValue)+"): ",end='')
        entry = input()
        if entry == '':continue
        try: eval(entry)
        except NameError:print("Invald input");continue
        entry = eval(entry)
        if 5 <= entry <= 1000:
            return entry
        

def printCommands():
    print()
    print("## COMMANDS ##")
    print("Command | Description |")
    print("--------|--------------")
    print("  +/-\t| zoom in or out by a factor of 2 on the initial image")
    print("  X\t| Toggles Cross Hairs")
    print("  dis\t| Toggles details printed on image")
    print("  iter\t| Sets the max iteration ")
    print("  res\t| Sets the resolution")
    print("  %N\t| Set the zoom for the initial image to N.")
    print("    \t|  -- Accepts:%0 %1, %16, %48, %128, %256, %512, %1024")
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
    print('Calculating...')
    
def setResolution(oldValue):
    res = {
        '1':(600,400),
        '2':(800,600),
        '3':(1200,800),
        '4':(1800,1200)
        }
    for key,value in res.items():print(key,value)
    
    while True:
        print("Enter the number for the new resolution (currently: "+\
              str(oldValue)+"x"+str(oldValue*.75)+"): ",end='')
        entry = str(input())
        if entry == '':continue
        
        if entry in res:
            WIDTH = res[entry][0]
            HEIGHT = res[entry][1]
            return WIDTH, HEIGHT
        else:print("Invalid input")
    
    
def naviLoop():
    #   Iterations
    MAX_ITER = 80
    #   Image size (pixels)
    WIDTH = 600
    HEIGHT = 400

    # Set initial coords
    #X:-0.7692813199999996 Y:0.1069251250000002
    x= -0.7692813199999996
    y= 0.1069251250000002

    #zStart = 4
    zStart = 2
    zTimes = 2
    
    #   Cross Hairs
    crossHairs = True
    #crossHairs = False

    #   Details on image
    display = True
    #display = False

    # The amount you can move
    big = 1/16
    bigD = big / 2
    small = big / 4
    smallD = small / 2
    xMoves = {
        # Big movements
        'E': bigD, 'e': smallD,
        'Z': -bigD, 'z': -smallD,
        'Q': -bigD, 'q': -smallD,
        'C': bigD, 'c': smallD,
        'D': big,'d':small,
        'A':-big, 'a':-small,

        # micro movements
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
        'Q': bigD, 'q': smallD,
        'E': bigD, 'e': smallD,
        'Z': -bigD, 'z': -smallD,
        'W': big, 'w':small,
        'S':-big, 's':small,
        'C': -bigD, 'c': -smallD,

        # micro movements
        '8': 0.0000001,
        '7': 0.0000000525,
        '9': 0.0000000525,
        '2': -0.0000001,
        '1': -0.0000000525,
        '3': -0.0000000525,
        '':0
        }
    
    '''
    x = -0.34515740000000006
    y = -0.6422024999999997
    '''
  
    #printHelp()
    print("Generating Images for:",x,y)
    print()
    # printZooms:

    printZooms(x, y, WIDTH, HEIGHT, MAX_ITER, zStart, zTimes, crossHairs, display,)

    
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
        if entry.upper() == "ITER":
            MAX_ITER = setMaxIter(MAX_ITER)
            print(" --Max Iterations set to: "+str(MAX_ITER))
            commandBool=True;continue

         # Set Resolution
        if entry.upper() == "RES":
            WIDTH, HEIGHT = setResolution(WIDTH)
            print(" --Resolution set to: "+str(WIDTH)+"x"+str(HEIGHT))
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
        if entry.upper() =='X':
            if crossHairs == False:
                crossHairs = True
                print(" --Enabling Cross Hairs")
                commandBool=True;continue
            else:
                crossHairs = False
                print(" --Disabling Cross Hairs")
                commandBool=True;continue
        # Toggle Display
        if entry.upper() =='DIS':
            if display == False:
                display = True
                print(" --Enabling Display")
                commandBool=True;continue
            else:
                display = False
                print(" --Disabling Display")
                commandBool=True;continue
        # Set zoom value
        if entry == "%0":
            zStart = 4
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%1":
            zStart = 1
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%16":
            zStart = 1/16
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%48":
            zStart = 1/48
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
        x += xChange * zStart
        y += yChange * zStart
        commandBool = False
        print("Generating Images for:",x,y)
        print()
        if xChange or yChange: print("Change in X: "+str(xChange)+\
                          "\nChange in Y: "+str(yChange))
        print()
        
        # Print it
        #         X, Y, WIDTH, HEIGHT, MAX_ITER, Zstart, Ztimes, crossHairs, display, mag = 4
        printZooms(x, y, WIDTH, HEIGHT, MAX_ITER, zStart, zTimes, crossHairs, display,)
        displayImage()
        print("######################## Done #########################")
        print("#######################################################")
        print()
        if xChange or yChange: print("Change in X: "+str(xChange)+\
                          "\nChange in Y: "+str(yChange))
        print()
def displayImage():
    window = Tk()
    window.title("Mandelbrot Navigator v4.20")
    # Left Side
    frame1 = Frame(window)
    frame1.pack(side = LEFT)



    # Right Side
    frame2 = Frame(window)
    frame2.pack(side = RIGHT)
    # Image 1
    canvas1 = Canvas(frame2, width = 600, height = 400)  
    canvas1.pack()  
    img1 = ImageTk.PhotoImage(Image.open("navi-1.png"))  
    canvas1.create_image(10, 10, anchor=NW, image=img1)
    # Image 2
    canvas2 = Canvas(frame2, width = 600, height = 400)  
    canvas2.pack(side = BOTTOM)  
    img2 = ImageTk.PhotoImage(Image.open("navi-2.png"))  
    canvas2.create_image(10, 10, anchor=NW, image=img2)

    window.mainloop()





        
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

def getIters(start, times, interval):
    iterList = [start]
    for i in range(times -1 ):
        start += interval
        iterList.append(start)
    return iterList

def printIters(X, Y, zoom, WIDTH, HEIGHT, Istart, Itimes, Iinterval, crossHairs, display):    # Change default mag interval
    iterList = getIters(Istart, Itimes, Iinterval)
    counter = 1
    for i in iterList:
        printChart(X, Y, zoom, WIDTH, HEIGHT, i, crossHairs, display, counter)
        counter +=1

# Print as many images as Ztimes.
# mag is the amount (times) to magnify each time.
#      - So mag = 2 means is gets twice as big each time
def printZooms(X, Y, WIDTH, HEIGHT, MAX_ITER, Zstart, Ztimes, crossHairs, display, mag = 4):    # Change default mag interval
    zoomList = getZooms(Zstart, Ztimes, mag)
    counter = 1
    for zoom in zoomList:
        printChart(X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, counter)
        counter +=1

def printTime(t):
    minutes = 0
    seconds = t
    if t > 60:
        minutes = t // 60
    seconds = format(t % 60, '.4f')
    return str(minutes)+' minutes and '+seconds+' seconds.'
#              1  2  3        4     5       6          7         8          9
def printChart(X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display,  counter=1):
    import time as t
    tStart = t.time() 
    points, xSpread, ySpread = getPoints(X, Y, zoom)
    printZoom = str(1 / zoom)
    start = (points[0], points[1] )
    end =   (points[2], points[3] )
    RE_START = start[0]
    IM_START = start[1]
    RE_END = end[0]
    IM_END = end[1]

    # stuff for printing        
    #font1 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMono.ttf", 48)
    #font2 = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono.ttf", 12)
    res = str(WIDTH)+"x"+str(HEIGHT)
    numbersCounted = str(WIDTH * HEIGHT)
    iterations = str(MAX_ITER)
    if xSpread < 1:
        precision = str(len(str(xSpread))-2)
    else: precision = str(1)

    # Naming
    
    #name = 'zoom-'+printZoom+'x-'+str(counter)+'.png'
    ##name = 'iter-'+printZoom+'x-'+str(counter)+'.png'
    
    name = 'navi-'+str(counter)+'.png'
    #name = 'main-'+printZoom+'x'+res+'.png'
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
            m = mandelbrot(c, MAX_ITER)
            
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
        mag1 = .125
        X1 = (WIDTH/2-WIDTH*mag1)
        X2 = (WIDTH/2+WIDTH*mag1)
        Ycenter = HEIGHT/2
        Y1 = HEIGHT/2-HEIGHT *mag1
        Y2 = HEIGHT/2+HEIGHT*mag1
        Xcenter = WIDTH /2
        draw.line((X1, Ycenter, X2, Ycenter), fill=(0,0,255), width = 1)
        draw.rectangle((X1, Y1, X2, Y2), outline = (0,0,255))
        draw.line((Xcenter, Y1, Xcenter, Y2), fill=(0,0,255), width = 1)
      
    # Add Details
    if display:
        draw.rectangle((0, 0, WIDTH, 28), outline='black', fill='black')
        draw.text((4,0),details, (0,0,255))
        draw.text((4,14),"Coordinates: "+coordinates, (0,0,255))
    
    # save file
    im.convert('RGB').save(name, 'PNG')

    # print Time
    tEnd = t.time()
    tDif = tEnd - tStart
    print()
    print("Elapsed Time: "+printTime(tDif))
    print()
    print("#######################################################")
  

# printZooms takes 6 args:
#         (x, y, initial zoom, images, crossHairBool, mag-optional)
#printZooms(-0.3449474, -0.6425525, 1, 16, False, 2)

naviLoop()
'''
printIters(-0.7692813199999996, # X,
           0.1069251250000002,  # Y
           1/128,                 # zoom,
           4800,                  # WIDTH,               
           3600,                  # HEIGHT,
           200,                   # Istart,
           10,                   # Itimes,
           20,                    # Iinterval,
           crossHairs = False,
           display = False)

print('done')

'''

'''
Cool Locations:
X:-0.7806635625 Y:-0.14670003249999977
X: -1.1883  Y: 0.242
X: -0.749  Y: 0.149 
X:-0.34515734750000004 Y:-0.6422024474999997
X:-0.11640740000000008 Y:-0.6497024999999994

 Resolution: 600x400
  Zoom: 128.0x
  Iterations: 240

Center Coordinates: X:-0.7692813199999996 Y:0.1069251250000002


'''
