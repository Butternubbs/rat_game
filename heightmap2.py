from opensimplex import OpenSimplex
from pyglet.gl import *
from pyglet.window import key, mouse
import math
import random
import pyshaders


NOISE_FREQUENCY = 120
NUM_FILTERS = 3

SIZE = 100
HEIGHT_FACTOR = 40
TERRACE_HEIGHT = 0.01
SQUEEZE = 1

SPAWN_POINT = (30,30,30)
PLAYER_SPEED = 6
PLAYER_JUMP = 0.35
FRICTION = 0.2
BULLET_SPEED = 0.5

ENEMY_SPEED = 4
NUM_ENEMIES = 0

TREE_CHANCE = 0.03
airColor = [0.4, 0.4, 0.5, 1.0]
airColor = (GLfloat * len(airColor))(*airColor)
waterColor = [0, 0, 0.2, 1.0]
waterColor = (GLfloat * len(waterColor))(*waterColor)

vLists = []
batch = pyglet.graphics.Batch()
entityBatch = pyglet.graphics.Batch()
tBatch = pyglet.graphics.Batch() #transparent textures, must be drawn last
bullets = []
enemies = []
entities = []

grass = pyglet.graphics.TextureGroup(pyglet.image.load('flatgrass.png').get_mipmapped_texture())
grass2 = pyglet.graphics.TextureGroup(pyglet.image.load('flatgrass2.png').get_mipmapped_texture())
rock = pyglet.graphics.TextureGroup(pyglet.image.load('flatrock.png').get_mipmapped_texture())
rock2 = pyglet.graphics.TextureGroup(pyglet.image.load('flatrock2.png').get_mipmapped_texture())
sand = pyglet.graphics.TextureGroup(pyglet.image.load('flatsand.png').get_mipmapped_texture())
sand2 = pyglet.graphics.TextureGroup(pyglet.image.load('flatsand2.png').get_mipmapped_texture())
snow = pyglet.graphics.TextureGroup(pyglet.image.load('snow.png').get_mipmapped_texture())
stone = pyglet.graphics.TextureGroup(pyglet.image.load('flatstone.png').get_mipmapped_texture())
stone2 = pyglet.graphics.TextureGroup(pyglet.image.load('flatstone2.png').get_mipmapped_texture())

water = pyglet.graphics.TextureGroup(pyglet.image.load('water.png').get_mipmapped_texture())
enemy = pyglet.graphics.TextureGroup(pyglet.image.load('dirt3.png').get_mipmapped_texture())
bullet = pyglet.graphics.TextureGroup(pyglet.image.load('bullet.png').get_mipmapped_texture())

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Function to find equation of plane. 
def equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):  
    a1 = x2 - x1 
    b1 = y2 - y1 
    c1 = z2 - z1 
    a2 = x3 - x1 
    b2 = y3 - y1 
    c2 = z3 - z1 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x1 - b * y1 - c * z1) 
    return (a, b, c, d)
    #Equation of plane is ax + by + cz + d= 0.

hmap = []
for s in range(SIZE):
    hmap.append([])
    for d in range(SIZE):
        hmap[s].append(None)

tmp = OpenSimplex(random.randint(1, 100))
percent = 0
for i in range(SIZE):
    for j in range(SIZE):
        hmap[i][j] = tmp.noise2d(x=i/NOISE_FREQUENCY, y=j/NOISE_FREQUENCY)
        for f in range(NUM_FILTERS):
            fac = math.pow(2, f+1)
            hmap[i][j] += abs(tmp.noise2d(x=i/(NOISE_FREQUENCY/fac), y=j/(NOISE_FREQUENCY/fac))/fac)
        hmap[i][j] *= HEIGHT_FACTOR
        hmap[i][j] -= hmap[i][j]%TERRACE_HEIGHT #TERRACING, UNCOMMENT FOR COOL EFFECT
        if int((i*SIZE+j)/(SIZE*SIZE)*100) > percent:
            percent = int((i*SIZE+j)/(SIZE*SIZE)*100)
            print("Calculating... " + str(percent) + "%")
        

class Player:
    def __init__(self,pos=(5,12,5),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.xvel = 0
        self.yvel = 0
        self.zvel = 0
        self.speed = 0
        #self.ch = Crosshair((5, 5, 5))
        self.onGround = False
        self.underwater = False
        self.points = 0
        self.hitbox = [self.pos[0] - 0.5, self.pos[0] + 0.5,
                       self.pos[1] - 0.5, self.pos[1] + 0.5,
                       self.pos[2] - 0.5, self.pos[2] + 0.5]

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90

    def update(self,dt,keys):
        s = dt*5 #speed factor
        rotY = -self.rot[1]/180*math.pi
        self.xvel *= (1 - FRICTION)
        self.zvel *= (1 - FRICTION)

        self.dx,self.dz = s*math.sin(rotY),s*math.cos(rotY)
        self.speed = math.sqrt((self.xvel*self.xvel) + (self.zvel * self.zvel))
        if not self.underwater:
            if self.speed < 0.01 * PLAYER_SPEED:
                if keys[key.W]: self.xvel+=self.dx; self.zvel-=self.dz
                if keys[key.S]: self.xvel-=self.dx; self.zvel+=self.dz
                if keys[key.A]: self.xvel-=self.dz; self.zvel-=self.dx
                if keys[key.D]: self.xvel+=self.dz; self.zvel+=self.dx
        else:
            if self.speed < 0.005 * PLAYER_SPEED:
                if keys[key.W]: self.xvel+=self.dx; self.zvel-=self.dz
                if keys[key.S]: self.xvel-=self.dx; self.zvel+=self.dz
                if keys[key.A]: self.xvel-=self.dz; self.zvel-=self.dx
                if keys[key.D]: self.xvel+=self.dz; self.zvel+=self.dx
        
        if keys[key.P]: print(self.pos)
        if keys[key.R]: print(self.rot)
        if keys[key.LSHIFT]: 
            self.yvel = -0.25
        #interpolation/ground collision
        grid_corners = [hmap[int(self.pos[0]*SQUEEZE)][int(self.pos[2]*SQUEEZE)],
                        hmap[int(self.pos[0]*SQUEEZE)+1][int(self.pos[2]*SQUEEZE)],
                        hmap[int(self.pos[0]*SQUEEZE)][int(self.pos[2]*SQUEEZE)+1],
                        hmap[int(self.pos[0]*SQUEEZE)+1][int(self.pos[2]*SQUEEZE)+1]]
        x_in_grid = self.pos[0] % 1/SQUEEZE
        z_in_grid = self.pos[2] % 1/SQUEEZE
        if x_in_grid + z_in_grid < 1/SQUEEZE:
            tri = 0
        else:
            tri = 1
        
        if tri == 0:
            plane = equation_plane(int(self.pos[0]*SQUEEZE), grid_corners[0], int(self.pos[2]*SQUEEZE),
                                   int(self.pos[0]*SQUEEZE)+1, grid_corners[1], int(self.pos[2]*SQUEEZE),
                                   int(self.pos[0]*SQUEEZE), grid_corners[2], int(self.pos[2]*SQUEEZE)+1)
        else:
            plane = equation_plane(int(self.pos[0]*SQUEEZE)+1, grid_corners[1], int(self.pos[2]*SQUEEZE),
                                  int(self.pos[0]*SQUEEZE), grid_corners[2], int(self.pos[2]*SQUEEZE)+1,
                                  int(self.pos[0]*SQUEEZE)+1, grid_corners[3], int(self.pos[2]*SQUEEZE)+1)
        groundheight = -(plane[0]*self.pos[0]*SQUEEZE + plane[2]*self.pos[2]*SQUEEZE + plane[3])/(plane[1]*SQUEEZE)
        #print(groundheight)
        if self.pos[1] <= groundheight + 2:
            self.onGround = True
            self.pos[1] = groundheight + 2
        else:
            if not self.underwater:
                self.onGround = False
                if self.yvel > -0.8:
                    self.yvel -= 0.02
            else:
                if self.yvel > -0.12:
                    self.yvel -= 0.01
                else:
                    self.yvel = -0.12
        
        if tri == 0:
            norm_vector = (plane[0], plane[1], plane[2])
        else:
            norm_vector = (-plane[0], -plane[1], -plane[2])
        xz = math.sqrt(norm_vector[0]*norm_vector[0]+norm_vector[2]*norm_vector[2])
        if self.onGround:
            if not self.underwater:
                if abs(xz) > 1:
                    self.xvel -= norm_vector[0] * 0.02
                    self.yvel -= norm_vector[1] * 0.02
                    self.zvel -= norm_vector[2] * 0.02
                else:
                    self.yvel = 0 #full upward normal force, fully negates gravity
        
        if keys[key.SPACE]:
            if not self.underwater:
                if self.onGround:
                    self.yvel = PLAYER_JUMP #jump power
                    self.onGround = False
            else:
                if self.onGround:
                    self.yvel = 0.1 #jump power
                    self.onGround = False
                else:
                    if self.yvel < 0.2:
                        self.yvel += 0.02
        
        self.hitbox = [self.pos[0] - 0.5, self.pos[0] + 0.5,
                       self.pos[1] - 0.5, self.pos[1] + 0.5,
                       self.pos[2] - 0.5, self.pos[2] + 0.5]
        for enemy in enemies:
            if collide(self.hitbox, enemy.hitbox):
                self.pos = list(SPAWN_POINT)
                self.points = 0
        if self.pos[1] < 2:
            self.underwater = True
        else:
            self.underwater = False
        if self.pos[1] < 0:
            glFogfv (GL_FOG_COLOR, waterColor)
            glFogf (GL_FOG_DENSITY, min(-self.pos[1]*0.03, 0.3))
        else:
            glFogfv (GL_FOG_COLOR, airColor)
            glFogf (GL_FOG_DENSITY, 0.01)

        self.pos[0]+=self.xvel
        self.pos[2]+=self.zvel
        self.pos[1]+=self.yvel

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x = self.rot[1]*-1
        y = self.rot[0]
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

class Entity:
    def __init__(self, position, verts, fas, draw, texture, batcher):
        entities.append(self)
        self.pos = list(position)
        self.vertexLists = []
        self.vertices = verts
        self.faces = fas
        tex_coords = ('t2f',(0,0, 1,0, 0,1))
        for face in self.faces:
            verts = (self.vertices[face[0]][0]+self.pos[0], self.vertices[face[0]][1]+self.pos[1], self.vertices[face[0]][2]+self.pos[2],
                     self.vertices[face[1]][0]+self.pos[0], self.vertices[face[1]][1]+self.pos[1], self.vertices[face[1]][2]+self.pos[2],
                     self.vertices[face[2]][0]+self.pos[0], self.vertices[face[2]][1]+self.pos[1], self.vertices[face[2]][2]+self.pos[2])
            vLists.append(batcher.add(3, GL_TRIANGLES, texture, ('v3f/' + draw, verts), tex_coords))
            self.vertexLists.append(vLists[-1]) #0.25 protrusion from the position point in all directions

class Bullet(Entity):
    def __init__(self, position, vector):
        bullets.append(self)
        self.vec = list(vector)
        verts = [(0, 0.5, 0),
                 (0.5, 0, 0),
                 (0, 0, 0.5),
                 (-0.5, 0, 0),
                 (0, 0, -0.5),
                 (0, -0.5, 0)]
        faces = [(0, 1, 2),
                 (0, 2, 3),
                 (0, 3, 4),
                 (0, 4, 1),
                 (5, 1, 2),
                 (5, 2, 3),
                 (5, 3, 4),
                 (5, 4, 1)]
        super().__init__(position, verts, faces, 'stream', bullet, entityBatch)
        for vlist in self.vertexLists:
            for i in range(3):
                for j in range(3):
                    vlist.vertices[i*3+j] += self.vec[j]
        self.hitbox = [self.pos[0] - 0.25, self.pos[0] + 0.25,
                       self.pos[1] - 0.25, self.pos[1] + 0.25,
                       self.pos[2] - 0.25, self.pos[2] + 0.25]
        
    def update(self, player):
        self.hitbox = [self.pos[0] - 0.25, self.pos[0] + 0.25,
                       self.pos[1] - 0.25, self.pos[1] + 0.25,
                       self.pos[2] - 0.25, self.pos[2] + 0.25]
        for i in range(3):
            self.pos[i] += self.vec[i]*BULLET_SPEED
        for vlist in self.vertexLists:
            for i in range(3):
                for j in range(3):
                    vlist.vertices[i*3+j] += self.vec[j]*BULLET_SPEED
        if abs(self.pos[0]) > 1000 or abs(self.pos[1]) > 1000 or abs(self.pos[2]) > 1000:
            self.delete()
        return 0
    def delete(self):
        for vlist in self.vertexLists:
            vLists.remove(vlist)
            vlist.delete()
        entities.remove(self)
        bullets.remove(self)

class Enemy(Entity):
    def __init__(self, position):
        enemies.append(self)
        verts = [(0, 1, 0),
                 (1, 0, 0),
                 (0, 0, 1),
                 (-1, 0, 0),
                 (0, 0, -1),
                 (0, -1, 0)]
        faces = [(0, 1, 2),
                 (0, 2, 3),
                 (0, 3, 4),
                 (0, 4, 1),
                 (5, 1, 2),
                 (5, 2, 3),
                 (5, 3, 4),
                 (5, 4, 1)]
        super().__init__(position, verts, faces, 'dynamic', enemy, entityBatch)
        self.hitbox = [self.pos[0] - 0.5, self.pos[0] + 0.5,
                       self.pos[1] - 0.5, self.pos[1] + 0.5,
                       self.pos[2] - 0.5, self.pos[2] + 0.5] #0.25 protrusion from the position point in all directions
    def update(self, player):
        self.hitbox = [self.pos[0] - 0.5, self.pos[0] + 0.5,
                       self.pos[1] - 0.5, self.pos[1] + 0.5,
                       self.pos[2] - 0.5, self.pos[2] + 0.5]
        for bullet in bullets[:]:
            if collide(self.hitbox, bullet.hitbox):
                bullet.delete()
                self.delete()
                return 10
        return 0
    def delete(self):
        for vlist in self.vertexLists:
            vLists.remove(vlist)
            vlist.delete()
        entities.remove(self)
        enemies.remove(self)

class Mobile(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.xvel = 0
        self.yvel = 0
        self.zvel = 0
        self.onGround = False
        self.wait = 0
    def update(self, player):
        self.xvel *= (1 - FRICTION)
        self.zvel *= (1 - FRICTION)
        vecc = vector(self.pos, player.pos)
        if math.sqrt((vecc[0]*vecc[0]) + (vecc[1] * vecc[1]) + (vecc[2] * vecc[2])) <= 15:
            self.speed = math.sqrt((self.xvel*self.xvel) + (self.zvel * self.zvel))
            if self.speed < 0.01 * ENEMY_SPEED:
                self.xvel -= vecc[0] * 0.01; self.zvel -= vecc[2] * 0.01
        
        #interpolation/ground collision
        grid_corners = [hmap[int(self.pos[0]*SQUEEZE)][int(self.pos[2]*SQUEEZE)],
                        hmap[int(self.pos[0]*SQUEEZE)+1][int(self.pos[2]*SQUEEZE)],
                        hmap[int(self.pos[0]*SQUEEZE)][int(self.pos[2]*SQUEEZE)+1],
                        hmap[int(self.pos[0]*SQUEEZE)+1][int(self.pos[2]*SQUEEZE)+1]]
        x_in_grid = self.pos[0] % 1/SQUEEZE
        z_in_grid = self.pos[2] % 1/SQUEEZE
        if x_in_grid + z_in_grid < 1/SQUEEZE:
            tri = 0
        else:
            tri = 1
        
        if tri == 0:
            plane = equation_plane(int(self.pos[0]*SQUEEZE), grid_corners[0]/SQUEEZE, int(self.pos[2]*SQUEEZE),
                                   int(self.pos[0]*SQUEEZE)+1, grid_corners[1]/SQUEEZE, int(self.pos[2]*SQUEEZE),
                                   int(self.pos[0]*SQUEEZE), grid_corners[2]/SQUEEZE, int(self.pos[2]*SQUEEZE)+1)
        else:
            plane = equation_plane(int(self.pos[0]*SQUEEZE)+1, grid_corners[1]/SQUEEZE, int(self.pos[2]*SQUEEZE),
                                  int(self.pos[0]*SQUEEZE), grid_corners[2]/SQUEEZE, int(self.pos[2]*SQUEEZE)+1,
                                  int(self.pos[0]*SQUEEZE)+1, grid_corners[3]/SQUEEZE, int(self.pos[2]*SQUEEZE)+1)
        groundheight = -(plane[0]*self.pos[0]*SQUEEZE + plane[2]*self.pos[2]*SQUEEZE + plane[3])/(plane[1])
        dif = 0
        if self.pos[1] <= groundheight + 1:
            self.onGround = True
            premove = self.pos[1]
            self.pos[1] = groundheight + 1
            dif = premove - self.pos[1]
            self.yvel = 0
        else:
            self.onGround = False
            self.yvel -= 0.02
        
        if tri == 0:
            norm_vector = (plane[0], plane[1], plane[2])
        else:
            norm_vector = (-plane[0], -plane[1], -plane[2])
        xz = math.sqrt(norm_vector[0]*norm_vector[0]+norm_vector[2]*norm_vector[2])
        if self.onGround:
            if abs(xz) > 1:
                self.xvel -= norm_vector[0] * 0.02
                self.yvel -= norm_vector[1] * 0.02
                self.zvel -= norm_vector[2] * 0.02
            self.yvel = 0 #full upward normal force, fully negates gravity
        
        if math.sqrt((vecc[0]*vecc[0]) + (vecc[1] * vecc[1]) + (vecc[2] * vecc[2])) <= 15:
            if self.onGround:
                self.yvel = 0.2 #jump power
                self.onGround = False
                self.wait = 10
        self.wait -= 1
        self.pos[0]+=self.xvel
        self.pos[2]+=self.zvel
        self.pos[1]+=self.yvel

        for vlist in self.vertexLists:
            for i in range(3):
                vlist.vertices[i*3] += self.xvel
                vlist.vertices[i*3+1] += self.yvel - dif
                vlist.vertices[i*3+2] += self.zvel
        
        return super().update(player)

class Tree(Entity):
    def __init__(self, position, color, width):
        verts = [(0, width*4, 0),
                 (width, 0, 0),
                 (-width, 0, 0),
                 (0, 0, width),
                 (0, 0, -width)]
        faces = [(0, 1, 2),
                 (0, 3, 4)]
        super().__init__(position, verts, faces, 'static', color, entityBatch)
    def update(self, player):
        return 0

class Window(pyglet.window.Window):

    def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2])
    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    def set2d(self): self.Projection(); gluOrtho2D(0,self.width,0,self.height); self.Model()
    def set3d(self): self.Projection(); gluPerspective(70,self.width/self.height,0.1,100); self.Model()

    def setLock(self,state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; mouse_lock = property(lambda self:self.lock,setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.player = Player(SPAWN_POINT,(-30,0))
        self.reticle = None

    def update(self,dt):
        self.player.update(dt,self.keys)
        for entity in entities[:]:
            pts = entity.update(self.player)
            if pts > 0:
                self.player.points += pts
                print(self.player.points)
        if enemies.__len__() < NUM_ENEMIES:
            x = random.randint(25,75)
            y = random.randint(25,75)
            Mobile((x, hmap[x][y] + 25, y))

    def on_draw(self):
        glLightfv(GL_LIGHT0,GL_SPOT_CUTOFF,GLfloat(180))
        self.clear()
        self.set3d()
        glColor3d(1, 1, 1)
        self.push(self.player.pos, self.player.rot)
        self.clear()
        glPolygonMode(GL_FRONT, GL_FILL)
        entityBatch.draw()
        batch.draw()
        tBatch.draw()
        glPopMatrix()
        fps_display.draw()
        self.set2d()
        self.draw_reticle()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)
    
    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_mouse_press(self, x, y, BUTTON, MOD):
        vector = self.player.get_sight_vector()
        if BUTTON == mouse.LEFT:
            Bullet(self.player.pos, vector)
    
    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock
    
    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        #self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

def collide(boxa, boxb):
    xcoll = boxa[1] >= boxb[0] and boxb[1] >= boxa[0]
    ycoll = boxa[3] >= boxb[2] and boxb[3] >= boxa[2]
    zcoll = boxa[5] >= boxb[4] and boxb[5] >= boxa[4]
    return xcoll and ycoll and zcoll

def vector(start, end):
    return (start[0] - end[0], start[1] - end[1], start[2] - end[2])




vert = '''
#version 120

varying vec4 diffuse_term;
varying vec3 ecViewdir;
varying vec3 normal;

void main()
{
    ecViewdir = (gl_ModelViewMatrix * gl_Vertex).xyz;
    gl_Position = ftransform();
    normal = gl_NormalMatrix * gl_Normal;  
    diffuse_term = gl_FrontMaterial.diffuse * gl_LightSource[0].diffuse;
    vec4 constant_term = gl_FrontMaterial.emission + gl_FrontMaterial.ambient
    * gl_LightSource[0].ambient;  
    gl_FrontColor.rgb = constant_term.rgb; gl_FrontColor.a = 1.0;
    gl_BackColor.rgb = constant_term.rgb; gl_BackColor.a = 0.0;

}
'''

frag = '''
varying vec4 diffuse_term;
varying vec3 ecViewdir;
varying vec3 normal;

void main()
{
    vec3 n;
    float NdotL, NdotHV;
    vec4 color = gl_Color;
    vec3 lightDir = gl_LightSource[0].position.xyz;
    vec3 halfVector = normalize(normalize(-lightDir) + normalize(ecViewdir));
    vec4 texel;
    vec4 fragColor;
    vec4 specular = vec4(0.0);
    n = normalize(normal);
    NdotL = dot(n, lightDir);
    if (NdotL > 0.0)
    {
    color += diffuse_term * NdotL;
    NdotHV = max(dot(n, halfVector), 0.0);
    if (gl_FrontMaterial.shininess > 0.0)
         {
          specular.rgb = (gl_FrontMaterial.specular.rgb
         * gl_LightSource[0].specular.rgb
         * pow(NdotHV, gl_FrontMaterial.shininess));
        }
    }
    color.a = diffuse_term.a;
    color = clamp(color, 0.0, 1.0);
    fragColor = color + specular;
    gl_FragColor = fragColor;
}
'''


try:
    program = pyshaders.from_string(vert, frag)
except pyshaders.ShaderCompilationError as e:
    print(e.logs)
print(program.uniforms)

tex_coordsone = ('t2f',(0,0, 1,0, 0,1))
tex_coordstwo = ('t2f',(1,0, 0,1, 1,1))
percent = 0
for i in range(SIZE - 1):
    for j in range(SIZE - 1):
        vertsOne = (i/SQUEEZE,hmap[i][j]/SQUEEZE,j/SQUEEZE, (i+1)/SQUEEZE,hmap[i+1][j]/SQUEEZE,j/SQUEEZE, i/SQUEEZE,hmap[i][j+1]/SQUEEZE,(j+1)/SQUEEZE)
        vertsTwo = ((i+1)/SQUEEZE,hmap[i+1][j]/SQUEEZE,j/SQUEEZE, i/SQUEEZE,hmap[i][j+1]/SQUEEZE,(j+1)/SQUEEZE, (i+1)/SQUEEZE,hmap[i+1][j+1]/SQUEEZE,(j+1)/SQUEEZE)

        #Deciding which texture to use
        avgheight = (vertsOne[4]+vertsOne[7])/2
        plane = equation_plane(*vertsOne)
        xz = math.sqrt(plane[0]*plane[0]+plane[2]*plane[2]) #xz component of normal vector to plane
        if abs(xz) > 1/(SQUEEZE*SQUEEZE) and avgheight > 10:
            tex = stone
        elif abs(xz) > 1/(SQUEEZE*SQUEEZE) and avgheight <= 10:
            tex = rock
        elif avgheight <= 1:
            tex = sand
        elif avgheight >= 10:
            tex = snow
        else:
            tex = grass
            if random.random() < TREE_CHANCE:
                Tree((i, avgheight, j), grass, max(random.random()*3, 0.5))
        vLists.append(batch.add(3,GL_TRIANGLES,tex,('v3f', vertsOne),tex_coordsone))
        
        avgheight = (vertsTwo[1]+vertsTwo[4])/2
        plane = equation_plane(*vertsTwo)
        xz = math.sqrt(plane[0]*plane[0]+plane[2]*plane[2])
        if abs(xz) > 1/(SQUEEZE*SQUEEZE) and avgheight > 10:
            tex = stone2
        elif abs(xz) > 1/(SQUEEZE*SQUEEZE) and avgheight <= 10:
            tex = rock2
        elif avgheight <= 1:
            tex = sand2
        elif avgheight >= 10:
            tex = snow
        else:
            tex = grass2
        vLists.append(batch.add(3,GL_TRIANGLES,tex,('v3f', vertsTwo),tex_coordstwo))
        if int((i*SIZE+j)/(SIZE*SIZE)*100) > percent:
            percent = int((i*SIZE+j)/(SIZE*SIZE)*100)
            print("Rendering... " + str(percent) + "%")

waterverts = (0, 0, 0, SIZE/SQUEEZE, 0, 0, 0, 0, SIZE/SQUEEZE, SIZE/SQUEEZE, 0, SIZE/SQUEEZE)
vLists.append(tBatch.add(3,GL_TRIANGLES,water,('v3f', waterverts[0:9]),tex_coordsone))
vLists.append(tBatch.add(3,GL_TRIANGLES,water,('v3f', waterverts[3:12]),tex_coordstwo))


if __name__ == '__main__':
    config = pyglet.gl.Config(sample_buffers=1, samples=4, major_version=4, minor_version=4)
    window = Window(width=854,height=480,caption='Height Map',resizable=True)
    fps_display = pyglet.window.FPSDisplay(window)
    glEnable(GL_DEPTH_TEST)
    

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    lightSource = [100, 0, 100]
 
    glEnable(GL_FOG)
 
    global fogMode
    fogMode = GL_EXP
    glFogi (GL_FOG_MODE, fogMode)
    glFogfv (GL_FOG_COLOR, airColor)
    glFogf (GL_FOG_DENSITY, 0.01)
    glHint (GL_FOG_HINT, GL_DONT_CARE)
    glFogf (GL_FOG_START, 1.0)
    glFogf (GL_FOG_END, 5.0)
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glShadeModel(GL_SMOOTH) 
    
    #glEnable(GL_CULL_FACE)
    #Mobile((50, hmap[50][50], 50))
    
    print(glGetError(program.use()))
    glDisable(GL_CULL_FACE)

    pyglet.app.run()