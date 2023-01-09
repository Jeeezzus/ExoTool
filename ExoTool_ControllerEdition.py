#region Imports
from PIL import Image, ImageOps
from pyrr import Matrix44

import moderngl as mgl
import numpy as np

import pygame
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import serial
import serial.tools.list_ports
import time
import math 
from matplotlib.ticker import MaxNLocator
#endregion

#region PyGame Initialisation
start = time.time()

pygame.init()
screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font2 = pygame.font.SysFont("Arial", 64)
#endregion

#region variables
fpslist = []    #To store the fps count of the previous frames
fpsText = "0"   #Text object for the FSP counter
graphMax = 30   #number of seconds displayed on the fps graph
ser = "none"    #To store the recieved infos in a global way
run = True      #To store id the app is running
up = True       #
frame = 0       #Count frames since the start of the programm
alpha = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #angles of the fingers
errcpt = 0      #Count error to trigger a scan of devices (arduino disconected)
isLeftHand = True
handButtonText = "Right Hand"
#cam settings------------------
cameraAngle = 0 #Angle for the camera
camAuto = False #Is the camera in automod (turning around the model)
speed = 0.01    #Speed of the turn
camRadius = 4
#------------------------------
#endregion

#region Tools

def pilImageToSurface(pilImage): #transform ans image to a PyGame surface (used to display it)
  return pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

        
def show_fbo(fbo, size, color_mode): #Take the FrameBuffer of modernGL
    img = Image.frombytes(color_mode, size, fbo.read(components=len(color_mode))) #Translate the FrameBuffer to a PIL image
    img = img.transpose(Image.FLIP_TOP_BOTTOM ) #Flip it
    if (isLeftHand == False):
      img = img.transpose(Image.FLIP_LEFT_RIGHT)
    pygameSurface = pilImageToSurface(img) #Translate it to a PyGame surface
    screen.blit(pygameSurface, pygameSurface.get_rect(center = (1400, 490))) #Display it on the left of the screen

def update_fps(): #Get fps from Pygame and store it into an array and put it into a text format to be displayed
	fps = int(clock.get_fps())
	fpslist.append(fps)
	fpstring = str(fps)
	fps_text = font.render(fpstring, 1, pygame.Color("coral"))
	return fps_text

def portsDetection(): #To detect arduinos
     print("waiting for connection...")
     ports = list(serial.tools.list_ports.comports()) #Scan all active ports on the PC
     for p in ports:
          print(p.manufacturer)
          if "Arduino" in p.manufacturer:
               print("This is an Arduino!")
               return(serial.Serial(str(p.device), 115200, timeout=1)) #If the manufacturer of the board is "Arduino" return it
     raise Exception("No device Found") #Raise an exception if we didn't find any arduinos

def button(screen, position, text, fsize): #To draw and render buttons with pygame
	fontb = pygame.font.SysFont("Arial", fsize)
	text_render = fontb.render(text, 1, (255, 0, 0)) #create a text object for the button
	x, y, w , h = text_render.get_rect() #Get the dimentions of the text
	x, y = position
	pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
	pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
	pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
	pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
	pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h)) #Draw edges and rectangle around the text
	return screen.blit(text_render, (x, y))#Display the button

def alphas(): #Assign the anglo to each phallanges
  for i in range(5):
          alpha[i][1] = alpha[i][0] +  0.25 + alpha[i][0]
          alpha[i][2] = alpha[i][1] + alpha[i][0] - 1
          alpha[i][0] += 1.
#endregion

#region ModernGL context creation
   
SIZE = WIDTH, HEIGHT = int(1080), int(1080)
COLOR_MODE = "RGBA"
ctx = mgl.create_context(standalone=True)
fbo = ctx.simple_framebuffer(SIZE, components=len(COLOR_MODE))
fbo.use()

vbo = ctx.buffer(np.array([
    # x     y    z     u    v  
     1,     1,  0.0,   1.,  1.,
     1,    -1,  0.0,   1., -1.,
    -1,    -1,  0.0,  -1., -1.,
    -1,     1,  0.0,  -1.,  1.,
], dtype=np.float32))

ibo = ctx.buffer(np.array([
    0, 1, 3,
    1, 2, 3,
], dtype=np.int32))


with open('shaders/Fragment.glsl', 'r') as file:
     FS = file.read()

with open('shaders/Vertex.glsl', 'r') as file:
     VS = file.read()

prog = ctx.program(vertex_shader=VS, fragment_shader=FS)
vao = ctx.vertex_array(prog, [(vbo, "3f 2f", "in_vert", "in_uv")], ibo)
vao.render(mode=mgl.TRIANGLES)
#endregion

#region initialisation
#assign first position of phalanges
alphas()
prog["cameraRadius"] = camRadius

plt.style.use('dark_background')
start = time.time()
#endregion

#region MainLoop
while run: #Looping while the app is running
  #region FrameInit
  frame += 1 #Add one frame to the counter
  screen.fill(0) #clearing the screen
  camModified = False #reseting the camera state
  calculated = False #reseting the angle calcultion state
  if camAuto == True and frame % 2 == 0: #If the camera turns by itself, adjusting the cam angle by the speed
    cameraAngle += speed
    camModified = True
    if(cameraAngle >= (2*math.pi)) or cameraAngle <= -(2*math.pi):
      print("reduced")
      cameraAngle = 0
    prog["camAngle"] = cameraAngle

  clock.tick(60) #Tick Pygame with a limitation of 60 fps (is we have more than 60, Pygame will wait before continuing)
  text = font2.render("ExoTool Viewer V1.4", 1, pygame.Color("orange")) #create the text object for the title
  
  #endregion
  
  #region fps Graph
  end = time.time()
  fig = None
  if (end-start >= 1):
    start = time.time()
    fpsText = update_fps()
    fig = plt.figure(figsize=(8.4, 2.0), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    if graphMax != -1:
        ax.plot(range(len(fpslist))[-graphMax:-1],fpslist[-graphMax:-1])
    else:
        ax.plot(range(len(fpslist)),fpslist)
    try:
        ax.set_ylim(ymin=0, ymax=(max(fpslist[-graphMax:-1])+5))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    except:
        pass

    fig.canvas.draw()
    pil = Image.frombytes('RGB',fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    surf = pilImageToSurface(pil)
    matplotlib.pyplot.close()
    #Just for debugging
    #print(len(fpslist))
  try:
        screen.blit(surf, surf.get_rect(center = (430, 900)))
  except Exception:
    pass
  #endregion

  #region Data Reception
  try:
    if (ser.inWaiting() > 0): #If there is a new data
      strval = ser.readline().decode().strip() #Strip the new data
      ser.flushInput()
      if "A" in strval: #Check if there is a grat chance that it's the good data
        alpha[0][0] =  (( int(strval.split("A")[1].split("B")[0])*1.6)/1024) - (0.85)#Assign the finger value to the first value alphas
        alpha[1][0] =  (( int(strval.split("B")[1].split("C")[0])*1.6)/1024) - (0.85)
        alpha[2][0] =  (( int(strval.split("C")[1].split("D")[0])*1.6)/1024) - (0.85)
        alpha[3][0] =  (( int(strval.split("D")[1].split("E")[0])*1.6)/1024) - (0.85)
        alpha[4][0] =  (( int(strval.split("E")[1].split("F")[0])*1.6)/1024) - (0.85)
        alphas() #Apply the change to all the phalanges
        for fing in range(5):
          for phal in range(1,4):
               prog["alpha" + str(fing) + ""+ str(phal)] = alpha[fing][phal-1] #Send the changes to the Fragment shader for each phalange of each finger
        
    errcpt = 0 #Reset the error counter
    calculated = True #Tell the program that new values have been calculated
  except Exception: #If there is an error while slicing the datas
          errcpt += 1 #add one to the error counter
          if (errcpt >= 10): #If there is 10 error in a row, we trigger the scan of new devices
               print("Connection error, please check cables")
               text = font2.render("waiting for connection...", 1, pygame.Color("red"))
               found = False
               while found == False: #Try to scan for new devices, loop while not found
                    clock.tick(5)#Reduce frame rate 
                    screen.blit(text, (10, 60))
                    pygame.display.update() #Display an error message
                    try:
                         ser = portsDetection()
                         found = True
                    except Exception:
                         found = False

                    
                        
          pass
  #endregion
  
  #region event handling
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if b1.collidepoint(pygame.mouse.get_pos()):
          camAuto = True
        if b2.collidepoint(pygame.mouse.get_pos()):
          camAuto = False
          cameraAngle += 0.2
          camModified = True
          prog["camAngle"] = cameraAngle
        if b3.collidepoint(pygame.mouse.get_pos()):
          camAuto = False
          cameraAngle -= 0.2
          camModified = True
          prog["camAngle"] = cameraAngle
        if b4.collidepoint(pygame.mouse.get_pos()):
          graphMax = 30
        if b5.collidepoint(pygame.mouse.get_pos()):
          graphMax = 60
        if b6.collidepoint(pygame.mouse.get_pos()):
          graphMax = 300
        if b7.collidepoint(pygame.mouse.get_pos()):
          graphMax = -1
        if b9.collidepoint(pygame.mouse.get_pos()):
          if(camRadius <= 8):
            camRadius += 0.25
          prog["cameraRadius"] = camRadius
        if b8.collidepoint(pygame.mouse.get_pos()):
          if(camRadius >= 1.5):
            camRadius -= 0.25
          prog["cameraRadius"] = camRadius
        if b10.collidepoint(pygame.mouse.get_pos()):
          if(isLeftHand == True):
            handButtonText = "Left Hand"
            isLeftHand = False
          else:
            handButtonText = "Right Hand"
            isLeftHand = True


  #endregion
  
  #region Rendering
  if camModified == True or calculated == True:
    vao.render(mode=mgl.TRIANGLES) #Render the shader
  screen.blit(text, (10,20)) #Display the title
  try: #Security to prevent errors of there is a problem with the graph
    screen.blit(fpsText, (810,800)) #Display the fps count
  except Exception:
    pass
  show_fbo(fbo, SIZE, COLOR_MODE) #Display function for the 3D visu
  #buttons for the camera
  b1 = button(screen, (200, 500), "Auto", 60)
  b2 = button(screen, (350, 500), "+", 60)
  b3 = button(screen, (120, 500), " - ", 60)
  b8 = button(screen, (160, 400), "Zoom +", 60)
  b9 = button(screen, (160, 600), "Zoom -", 60)

  b4 = button(screen, (50, 800), "30 sec", 20)
  b5 = button(screen, (125, 800), "1 min", 20)
  b6 = button(screen, (190, 800), "5 min", 20)
  b7 = button(screen, (255, 800), "All", 20)

  b10 = button(screen, (880, 20), handButtonText, 20)
  pygame.display.flip()
  #endregion
  
#endregion
pygame.quit()