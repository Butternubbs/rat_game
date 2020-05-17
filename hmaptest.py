from PIL import Image
import pygame
import sys
import random

im = Image.open('noise.png', 'r')
width, height = im.size
pixel_values = list(im.getdata())

#def toprow(left):
#    return max(left + random.randint(-10, 10), 0)
#def leftcol(top):
#    return max(top + random.randint(-10, 10), 0)
#def majority(left, top):
#    return max(int((left+top)/2) + random.randint(-10, 10), 0)
#
pygame.init()

screen = pygame.display.set_mode((400,400))
#
#hmap2 = []
#for s in range(40):
#    hmap2.append([])
#    for d in range(40):
#        hmap2[s].append(None)
#
#hmap2[0][0] = random.randint(0,100) #topleft point
#for x in range(1, 40): #top row
#    hmap2[0][x] = toprow(hmap2[0][x-1])
#for y in range(1, 40): #left column
#    hmap2[y][0] = leftcol(hmap2[y-1][0])
#
#for p in range(1, 40): #the rest
#    for q in range(1, 40):
#        if q == 39:
#            hmap2[p][q] = majority(hmap2[p][q-1], hmap2[p-1][q])
#        else:
#            hmap2[p][q] = majority(hmap2[p][q-1], hmap2[p-1][q])
#
#hmap = []
#for s in range(400):
#    hmap.append([])
#    for d in range(400):
#        hmap[s].append(None)
#
#hmap[0][0] = random.randint(0,100) #topleft point
#for x in range(1, 400): #top row
#    hmap[0][x] = toprow(hmap[0][x-1])
#for y in range(1, 400): #left column
#    hmap[y][0] = leftcol(hmap[y-1][0])
#
#for p in range(1, 400): #the rest
#    for q in range(1, 400):
#        if q == 399:
#            hmap[p][q] = majority(hmap[p][q-1], hmap[p-1][q])
#            hmap[p][q] = int((hmap[p][q] + hmap2[int(p/10)][int(q/10)])/2)
#        else:
#            hmap[p][q] = majority(hmap[p][q-1], hmap[p-1][q])
#            hmap[p][q] = int((hmap[p][q] + hmap2[int(p/10)][int(q/10)])/2)
#
#
for i in range(100):
    for j in range(100):
        rect = pygame.rect.Rect(i*1, j*1, 1, 1)
        #print(hmap[i][j])
        pygame.draw.rect(screen, (pixel_values[i*100+j][0], 0, 0), rect)

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE:
    
                