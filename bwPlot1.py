MAX_ITER = 100

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n

if __name__ == "__main__":
    for a in range(-10, 10, 5):
        for b in range(-10, 10, 5):
            c = complex(a / 10, b / 10)
            print(c, mandelbrot(c))
from PIL import Image, ImageDraw

def getPoints(x1,x2,y1):
    xd = abs( abs(x1) - abs(x2))
    if xd == 0 and x1 != x2: 
        yd = .75
    else: yd = xd * .75

    y2 = y1 + yd
    points = (x1,y1,x2,y2)
    return points
    
# Image size (pixels)
WIDTH = 1200
HEIGHT = 800

'''
# Plot window ORIGINAL
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1
'''
#points = getPoints(-.7, -.4, -.725) #output2.png
#points = getPoints(-2, -.5, -.5) # output1.png
#points = getPoints(-1, -.5, -.5)  #output3.png
#points = getPoints(-.795, -.74, .12) #output4.png
points = getPoints(-.82, -.78, .158) #output5.png
points = getPoints(-.81, -.80, .158)

# print Actions
print("Creating file")
print("Width: "+str(WIDTH)+" Height: "+str(HEIGHT))
print(points)

start = (points[0], points[1] )
end =   (points[2], points[3] )
RE_START = start[0]
IM_START = start[1]
RE_END = end[0]
IM_END = end[1]

palette = []

# Color Version
'''
im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = mandelbrot(c)
        # The color depends on the number of iterations
        hue = int(255 * m / MAX_ITER)
        saturation = 255
        value = 255 if m < MAX_ITER else 0
        # Plot the point
        draw.point([x, y], (hue, saturation, value))

im.convert('RGB').save('output.png', 'PNG')
'''
#Black and White

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)
for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = mandelbrot(c)
        # The color depends on the number of iterations
        color = 255 - int(m * 255 / MAX_ITER)
        # Plot the point
        draw.point([x, y], (color, color, color))

im.save('output.png', 'PNG')



print("#################### DONE #######################")
print("#################### DONE #######################")
print("#################### DONE #######################")



