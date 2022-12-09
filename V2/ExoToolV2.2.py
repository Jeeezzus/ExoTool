import moderngl as mgl
import numpy as np

import pygame


init = pygame.init()
print(init)

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3); 
screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE | pygame.OPENGL)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font2 = pygame.font.SysFont("Arial", 64)
  
SIZE = WIDTH, HEIGHT = int(500), int(500)
COLOR_MODE = "RGBA"

ctx = mgl.create_context()
fbo = ctx.simple_framebuffer(SIZE, components=len(COLOR_MODE))
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

with open('shaders/Fragment.glsl', 'r') as file:
     FS = file.read()

with open('shaders/Vertex.glsl', 'r') as file:
     VS = file.read()

prog = ctx.program(vertex_shader=VS, fragment_shader=FS)
vao = ctx.vertex_array(prog, [(vbo, "3f 2f", "in_vert", "in_uv")], ibo)
vao.render(mode=mgl.TRIANGLES)

run = True
while run:
  screen.fill(150)
  text = font2.render("Hello World", 1, pygame.Color("orange"))
  screen.blit(text, (10,20))

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
  pygame.display.flip()
pygame.quit()