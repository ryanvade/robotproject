__author__ = 'ryanvade'
import pygame

title = "Hello!"
width = 640
height = 400
pygame.init()
screen = pygame.display.set_mode((width, height))
running = True
pygame.display.set_caption(title)

while True:
    key = pygame.key.get_pressed()
    if key[pygame.K_q]:
        break
    elif key[pygame.K_s]:
        print ("s")
    elif key[pygame.K_UP]:
        if key[pygame.K_RIGHT]:
            print ("up+right")
        elif key[pygame.K_LEFT]:
            print ("Up+left")
        print ("up")
    elif key[pygame.K_DOWN]:
        print ("down")
    elif key[pygame.K_LEFT]:
        print ("left")
    elif key[pygame.K_RIGHT]:
        print ("right")
    elif key[pygame.K_a]:
        print ("a")
    elif key[pygame.K_z]:
        print ("z")
