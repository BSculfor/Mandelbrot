from PIL import Image
from math import sqrt
from math import log as ln

def oneOverln(n):
    return 1/ln(n)

def lerp(x, a, b):    #interpolates x as a combination of a & b when a<=x<=b
    colour=[0,0,0]
    colour[0]=int((((x-a[0])/(b[0]-a[0]))*a[1][0])+(((b[0]-x)/(b[0]-a[0]))*b[1][0]))
    colour[1]=int((((x-a[0])/(b[0]-a[0]))*a[1][1])+(((b[0]-x)/(b[0]-a[0]))*b[1][1]))
    colour[2]=int((((x-a[0])/(b[0]-a[0]))*a[1][2])+(((b[0]-x)/(b[0]-a[0]))*b[1][2]))
    return (colour[0],colour[1], colour[2])

def f(z, c):  #f(z,c) = z^2+c, for z,c \in C. z = z[0]+z[1]i
    return [(z[0]*z[0])-(z[1]*z[1])+c[0], 2*z[0]*z[1]+c[1]]

"""From here down to the end ot the function 'classic(colour)' (line 80),
the functions are different ways of colouring the fractal"""

def ColourBlue(colour):
    #takes input as an int 0<=colour<=255
    if colour >= 127 and colour < 255:
        #changes from blue to white near the boundary
        return (colour, colour, 255)
    elif colour < 127 and colour > 0:
        #changes from black to blue far from the boundary
        return (0, 0, colour)
    else:
        #If the point hits the max number of iterations, it is marked black
        return (0,0,0)

def ColourGreen(colour):
    if colour >= 127 and colour < 255:
        return (colour, 255, colour)
    elif colour < 127 and colour > 0:
        return (0, colour, 0)
    else:
        return (0,0,0)

def ColourRed(colour):
    if colour >= 127 and colour < 255:
        return (255, colour, colour)
    elif colour < 127 and colour > 0:
        return (colour, 0, 0)
    else:
        return (0,0,0)

def ColourCyan(colour):
    if colour >= 127 and colour < 255:
        return (colour, 255, 255)
    elif colour < 127 and colour > 0:
        return (0, colour, colour)
    else:
        return (0,0,0)

def ColourMagenta(colour):
    if colour >= 127 and colour < 255:
        return (255, colour, 255)
    elif colour < 127 and colour > 0:
        return (colour, 0, colour)
    else:
        return (0,0,0)

def ColourYellow(colour):
    if colour >= 127 and colour < 255:
        return (255, 255, colour)
    elif colour < 127 and colour > 0:
        return (colour, colour, 0)
    else:
        return (0,0,0)

def Greyscale(colour):
    if 0 < colour < 255:
        return (colour, colour, colour)
    else:
        return (0,0,0)

def classic(colour):
    if 0 <= colour <= 41:
        return lerp(colour,[0,[0,7,100]],[41,[0,0,0]])
    elif 41 < colour <= 107:
        return lerp(colour,[42,[32,107,203]],[70,[0,7,100]])
    elif 107 < colour <= 164:
        return lerp(colour,[71,[237,255,255]],[130,[32,107,203]])
    elif 164 < colour <= 219:
        return lerp(colour,[131,[255,170,0]],[200,[237,255,255]])
    elif 219 < colour < 255:
        return lerp(colour,[201,[0,2,0]],[255,[255,170,0]])
    else:
        return (0, 0, 0)

def mod(z): #returns |z|
    return sqrt(z[0]*z[0]+z[1]*z[1])

def iterate(z, m, func, c, b):
    #counts how many iterations of f(f(...f(0,c)...)) it takes before
    #the modulus of a point exceeds 2. 
    if z==func(z,c):
        return 0
    n=0
    while True:
        z = func(z,c)
        if mod(z) > b:   #break if the point escapes
            break
        n=n+1
        if n >= m:   #if it doesn't get outside the radius after this many iterations,
            break    #it probably never will, and can be assumed convergent
    return n
        
def Genfractal(maxiterations, colourfunc=classic):
    #^^Automatically generates red Mandelbrot images with a specified number of iterations
    #initialises a black image of the specified dimensions
    Mandelbrot=Image.new('RGB', (1366,768), 'black') 
    pixels=Mandelbrot.load()    #defines pixel map
    for i in range(Mandelbrot.size[0]): #Image.size = [width, height]
        for j in range(Mandelbrot.size[1]): 
            n = iterate([((3.5*i)/Mandelbrot.size[0])-2.5, 1-(2*j/Mandelbrot.size[1])], maxiterations, c)
            #makes n an integer from 0 to 255 
            colour=int((255*n/maxiterations)//1)
            #pixels[i,j]=(0,0,n) legacy code used to generate "Mandelbrot3.png"
            if n >= 127 and n<255:
                #changes from coloured to white near the boundary
                pixels[i,j]=colourfunc(colour)
            elif n<127 and n>0:
                #changes from black to coloured far from the boundary
                pixels[i,j]=colourfunc(colour)
            else:
                #If the point hits the max number of iterations, it is marked black
                pixels[i,j]=(0,0,0)
    filename=input("Image created. What would you like to name the file? ")+".PNG"
    Mandelbrot.save(filename)

######################################################################################################

wid=int(input("what is the width of the image (in pixels)? "))
hgt=int(input("What is the height of the image (in pixels)? "))
Mandelbrot=Image.new('RGB', (wid,hgt), 'black')
pixelmap=Mandelbrot.load()
maxiterations = int(input("How many iterations do you want? "))
bailout=int(input("What should the bailout radius be (normally ==2)? "))
if hgt > wid:
    def x(i,j):
        return [(3.5*j)/hgt-2.5, 1-(2*i/wid)]
else:
    def x(i,j):
        return [(3.5*i)/wid-2.5, 1-(2*j/hgt)]
while True:
    cscheme=input("What colour would you like the fractal to be? [r,g,b,c,m,y,greyscale,classic] ")    
    if cscheme=='r' or cscheme=='R' or cscheme=='Red' or cscheme=='red':
        colourfunc=ColourRed
        break
    elif cscheme=='g' or cscheme=='G' or cscheme=='Green' or cscheme=='green':
        colourfunc=ColourGreen
        break
    elif cscheme=='b' or cscheme=='B' or cscheme=='Blue' or cscheme=='blue':
        colourfunc=ColourBlue
        break
    elif cscheme=='c' or cscheme=='C' or cscheme=='Cyan' or cscheme=='cyan':
        colourfunc=ColourCyan
        break
    elif cscheme=='m' or cscheme=='M' or cscheme=='Magenta' or cscheme=='magenta':
        colourfunc=ColourMagenta
        break
    elif cscheme=='y' or cscheme=='Y' or cscheme=='Yellow' or cscheme=='yellow':
        colourfunc=ColourYellow
        break
    elif cscheme=='greyscale' or cscheme=='Greyscale' or cscheme=='Grayscale' or cscheme=='grayscale':
        colourfunc=Greyscale
        break
    elif cscheme=='classic' or cscheme=='Classic':
        colourfunc=classic
        break
    else:
        print("Not a valid input. Please type one of the options given.")
while True:
    ans=input("Do you want to specify c? [y/n] ")
    if ans=='y' or ans=='Y' or ans=='yes' or ans=='Yes':
        c=[]
        c.append(float(input("Re(c) == ")))
        c.append(float(input("Im(c) == ")))
        break
    else:
        break
for i in range(Mandelbrot.size[0]):
    for j in range(Mandelbrot.size[1]):
        n=iterate(x(i,j), maxiterations, f, x(i,j), bailout)
        #makes n an integer from 0 to 255 
        n=int((255*n/maxiterations)//1)
        pixelmap[i,j]=colourfunc(n)
    if i%25==0:
        print("Done column", i)
    if 2*i==Mandelbrot.size[0] and hgt>wid:
        print("__________________Halfway there!________________________")
filename=input("Image created. What would you like to name the file? ")+".PNG"
Mandelbrot.save(filename)
input("Image saved. Press [Enter] to exit the programme.")

