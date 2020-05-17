from opensimplex import OpenSimplex
import random
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400,400))

hmap = []
for s in range(200):
    hmap.append([])
    for d in range(200):
        hmap[s].append(None)

tmp = OpenSimplex(random.randint(1, 100))

for i in range(200):
    for j in range(200):
        hmap[i][j] = tmp.noise2d(x=i/15, y=j/15)
        rect = pygame.rect.Rect(i*2, j*2, 2, 2)
        pygame.draw.rect(screen, (max(0, int(hmap[i][j]*128+128)), 0, 0), rect)

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()