from __future__ import annotations

from PIL import Image
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

start = time.time()

pygame.init()

screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font2 = pygame.font.SysFont("Arial", 64)

fpslist = []

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

        
def show_fbo(fbo: mgl.Framebuffer, size: tuple[int], color_mode: str) -> None:
    print("bite")
    img = Image.frombytes(color_mode, size, fbo.read(components=len(color_mode)))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    pygameSurface = pilImageToSurface(img)
    screen.blit(pygameSurface, pygameSurface.get_rect(center = (1400, 490)))

def update_fps():
	fps = int(clock.get_fps())
	fpslist.append(fps)
	fpstring = str(fps)
	fps_text = font.render(fpstring, 1, pygame.Color("coral"))
	return fps_text

def portsDetection():
     print("waiting for connection...")
     ports = list(serial.tools.list_ports.comports())
     for p in ports:
          print(p.manufacturer)
          if "Arduino" in p.manufacturer:
               print("This is an Arduino!")
               return(serial.Serial(str(p.device), 115200, timeout=10))
     raise Exception("No device Found")

def button(screen, position, text):
	font = pygame.font.SysFont("Arial", 50)
	text_render = font.render(text, 1, (255, 0, 0))
	x, y, w , h = text_render.get_rect()
	x, y = position
	pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
	pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
	pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
	pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
	pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
	return screen.blit(text_render, (x, y))


ser = "none"    
SIZE = WIDTH, HEIGHT = int(500), int(500)
COLOR_MODE = "RGBA"
ctx = mgl.create_context()
fbo = ctx.simple_framebuffer(SIZE, components=len(COLOR_MODE))
fbo.use()

vbo = ctx.buffer(np.array([
    # x     y    z     u    v  
     1,  1, 0.0,  1., 1.,
     1, -1, 0.0,  1., -1.,
    -1, -1, 0.0,  -1., -1.,
    -1,  1, 0.0,  -1., 1.,
], dtype=np.float32))

ibo = ctx.buffer(np.array([
    0, 1, 3,
    1, 2, 3,
], dtype=np.int32))

b1 = button(screen, (200, 700), "Auto")
b2 = button(screen, (350, 700), "+")
b3 = button(screen, (110, 700), " - ")

L11 = 1.
L12 = 0.84
L13 = 0.92

L21 = 1.08
L22 = 1.04
L23 = 1.

L31 = 0.9
L32 = 0.9
L33 = 1.

L41 = 0.64
L42 = 0.6
L43 = 0.84

with open('shaders/Fragment.glsl', 'r') as file:
     FS = file.read()

with open('shaders/Vertex.glsl', 'r') as file:
     VS = file.read()
run = True
up = True
frame = 0
cameraAngle = 0
camAuto = False
speed = 0.01

alpha = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
P = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
def alphas():
  for i in range(4):
          alpha[i][1] = alpha[i][0] +  0.25 + alpha[i][0]
          alpha[i][2] = alpha[i][1] + alpha[i][0] - 1
          alpha[i][0] += 1.
          for j in range(3):
            P[i][j] = "vec3(" + str(L11*np.cos(alpha[i][j])) + "," + str(L11*np.sin(alpha[i][j])) + ",0.)"


errcpt = 0
alphas()


prog = ctx.program(vertex_shader=VS, fragment_shader=FS)
vao = ctx.vertex_array(prog, [(vbo, "3f 2f", "in_vert", "in_uv")], ibo)
vao.render(mode=mgl.TRIANGLES)
camModified = False

FPSText = update_fps()

while run:
  #show_fbo(fbo, SIZE, COLOR_MODE)
  camModified = False
  calculated = False
  if camAuto == True:
    cameraAngle += speed
    camModified = True
  frame += 1
  clock.tick(40)
  text = font2.render("ExoTool Viewer V1.2", 1, pygame.Color("orange"))
  screen.blit(text, (10,20))
  try:
    if (ser.inWaiting() > 0):
      strval = ser.readline().decode().strip()
      if "A" in strval:
        alpha[0][0] = ((int(strval.split("A")[1].split("B")[0])*1.6)/1024)-0.85
        alpha[1][0] = ((int(strval.split("B")[1].split("C")[0])*1.6)/1024)-0.85
        alpha[2][0] = ((int(strval.split("C")[1].split("D")[0])*1.6)/1024)-0.85
        alpha[3][0] = ((int(strval.split("D")[1])*1.6)/1024)-0.85
        alphas()
        prog["alpha01"] = alpha[3][0]
        prog["alpha02"] = alpha[3][1]
        prog["alpha03"] = alpha[3][2]
        for fing in range(1,5):
          for phal in range(1,4):
               #print("alpha" + str(fing) + ""+ str(phal))
               prog["alpha" + str(fing) + ""+ str(phal)] = alpha[fing-1][phal-1]
        
    errcpt = 0
    calculated = True
  except Exception:
          errcpt += 1
          if (errcpt >= 5):
               print("Connection error, please check cables")
               text = font2.render("waiting for connection...", 1, pygame.Color("red"))
               screen.blit(text, (1200, 10))
               pygame.display.update()
               found = False
               while found == False:
                    time.sleep(1)
                    try:
                         ser = portsDetection()
                         found = True
                    except Exception:
                         found = False
          pass
  try:
     prog["camAngle"] = cameraAngle
     vao.render(mode=mgl.TRIANGLES)
  except Exception:
    print("error while rendering image")
  

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if b1.collidepoint(pygame.mouse.get_pos()):
          camAuto = True
        if b2.collidepoint(pygame.mouse.get_pos()):
          camAuto = False
          cameraAngle += 0.2
        if b3.collidepoint(pygame.mouse.get_pos()):
          camAuto = False
          cameraAngle -= 0.2

  
  if frame>30 and frame%30 == 0:
    fig = plt.figure(figsize=(8.4, 2.0), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    end = time.time()
    ax.plot(range(len(fpslist))[-600:-1],fpslist[-600:-1])
    fig.canvas.draw()
    pil = Image.frombytes('RGB',fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    surf = pilImageToSurface(pil)
    matplotlib.pyplot.close()
    FPSText = update_fps()
    
  try:
    screen.blit(surf, surf.get_rect(center = (430, 900)))
    screen.blit(FPSText, (810,800))
  except Exception:
    pass
  pygame.display.update()
  
pygame.quit()