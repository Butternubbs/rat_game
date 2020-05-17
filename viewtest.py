import math
import random

def check(thingy): #this checks if a block exists in the grid space
    if random.random() > 0.5:
        return True
    else:
        return False

grid = []
for i in range(10):
    for j in range(5):
        for k in range(10):
            grid.append((i,j,k))
#print(grid)
pos = (random.random(), random.random(), random.random())
ori = ((180 * random.random() - 90), (360 * random.random() - 180))
ori = (ori[0] - ori[0]%0.125, ori[1] - ori[1]%0.125)

print("Position: " + str(pos))
print("Orientation: " + str(ori))
DIST = 4
dy = DIST * math.sin(math.radians(ori[0]))
plane = DIST * math.cos(math.radians(ori[0]))
dx = plane * math.sin(math.radians(ori[1]))
dz = plane * math.cos(math.radians(ori[1]))

print("Endpoint: " + str(dx + pos[0]) + " " + str(dy + pos[1]) + " " + str(dz + pos[2]))

#There should be a better way to optimize the # of comparisons...
if dx < 0:
    itx = -1
else:
    itx = 1
gugx = int(pos[0] + itx)
xnext = (gugx, (((gugx-pos[0])/dx)*dy) + pos[1], (((gugx-pos[0])/dx)*dz) + pos[2])
print(xnext)
if dy < 0:
    ity = -1
else:
    ity = 1
gugy = int(pos[1] + ity)
ynext = ((((gugy-pos[1])/dy)*dx) + pos[0], gugy, (((gugy-pos[1])/dy)*dz) + pos[2])
print(ynext)
if dz < 0:
    itz = -1
else:
    itz = 1
gugz = int(pos[2] + itz)
znext = ((((gugz-pos[2])/dz)*dx) + pos[0], (((gugz-pos[0])/dz)*dy) + pos[1], gugz)
print(znext)

memex = (((gugx-pos[0])/dx)*DIST) #distance from origin to first x-cross
memey = (((gugy-pos[1])/dy)*DIST) #distance from origin to first y-cross
memez = (((gugz-pos[2])/dz)*DIST) #distance from origin to first z-cross

print(memex)
print(memey)
print(memez)
while abs(memex) <= 4 or abs(memey) <= 4 or abs(memez) <= 4: #change ands to ors when done
    if memex < memey and memex < memez:
        if not check(xnext):
            gugx += itx
            memex = (((gugx-pos[0])/dx)*DIST)
            xnext = (gugx, (((gugx-pos[0])/dx)*dy) + pos[1], (((gugx-pos[0])/dx)*dz) + pos[2])
        else:
            return xnext
    if memey < memex and memey < memez:
        if not check(ynext):
            gugy += ity
            memey = (((gugy-pos[1])/dy)*DIST)
            ynext = ((((gugy-pos[1])/dy)*dx) + pos[0], gugy, (((gugy-pos[1])/dy)*dz) + pos[2])
        else:
            return ynext
    if memez < memex and memez < memey:
        if not check(znext):
            gugz += itz
            memez = (((gugz-pos[2])/dz)*DIST)
            znext = ((((gugz-pos[2])/dz)*dx) + pos[0], (((gugz-pos[0])/dz)*dy) + pos[1], gugz)
        else:
            return znext