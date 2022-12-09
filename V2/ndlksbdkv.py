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

pygame.init()

screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font2 = pygame.font.SysFont("Arial", 64)

run = True 
while run:
	screen.fill(0)
	text = font2.render("ExoTool Viewer V1.2", 1, pygame.Color("orange"))
	screen.blit(text, (10,20))
	pygame.display.flip()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
pygame.quit()
