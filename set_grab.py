import pygame
from pygame import *

display = (800,800)

init()
screen = pygame.display.set_mode(display)
pygame.mouse.set_pos(375,375)

dino = pygame.sprite.Sprite()
dino.image = transform.scale(pygame.image.load("dino.png"), (50, 50))
dino.rect = dino.image.get_rect(topleft = (375,375))
pygame.event.set_grab(True)
while 1:
    pygame.mouse.set_pos(375,375)
    #pygame.event.poll()
    (x, y) = pygame.mouse.get_rel()
    dino.rect.left += x
    dino.rect.top += y
    screen.fill((255,255,255))
    screen.blit(dino.image, dino.rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.set_grab(False)
        if event.type == MOUSEMOTION:
            print(event)