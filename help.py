import pygame
from numpy import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0, 1, 0),
    (0, 1, 0),
    (1, 0, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0),
    (0.2, 0.2, 0)
)
def Cube():
    glBegin(GL_QUADS)
    it = 0
    for face in faces:
        it += 1
        for vertex in face:
            glColor3fv(colors[it])
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_LINES)
    glColor3fv(colors[0])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.mouse.set_pos((400,400))
    pygame.event.poll()
    pitch = 0.0
    yaw = 0.0
    gluPerspective(45, (display[0]/display[1]), 0.1, 50)
    glTranslatef(0,0,-10)
    glRotatef(0,0,0,0)
    while 1:
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    glTranslate(-1, 0, 0)
                if event.key == K_RIGHT:
                    glTranslate(1, 0, 0)
                if event.key == K_UP:
                    glTranslate(0, 1, 0)
                if event.key == K_DOWN:
                    glTranslate(0, -1, 0)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslate(0,0,1)
                if event.button == 5:
                    glTranslate(0,0,-1)
            if event.type == MOUSEMOTION:
                (dx, dy) = pygame.mouse.get_rel()
                (x, y) = pygame.mouse.get_pos()
                print((dx, dy))
                yaw += dx
                pitch -= dy
                if pitch > 90:
                    glRotatef(abs(dy), 0, -dy, 0)
                    pitch = 90
                    pygame.mouse.set_pos((x - dx, 90))
                if pitch < -90:
                    glRotatef(abs(dy), 0, -dy, 0)
                    pitch = -90
                    pygame.mouse.set_pos((x - dx, 270))
                glRotatef(sqrt((dx*dx + dy*dy)), dx, dy, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()