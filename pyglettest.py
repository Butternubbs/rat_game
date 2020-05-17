from pyglet.gl import *
from pyglet.window import key, mouse
import math

models = []
for i in range(16):
    for k in range(16):
        for j in range(255):
            models.append((i,j,k))
        for j in range(1):
            models.append((i,j+255,k))
texs = []
for i in range(16):
    for k in range(16):
        for j in range(255):
            texs.append("dirt")
        for j in range(1):
            texs.append("grass")

batch = pyglet.graphics.Batch()
vLists = []

allTextures = ['grass_top.png', 'grass_side.png', 'dirt.png', 'cobblestone.png']
textures = []
for t in allTextures:
    textures.append(pyglet.graphics.TextureGroup(pyglet.image.load('grass_top.png').get_texture()))
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
grasstop = pyglet.graphics.TextureGroup(pyglet.image.load('grass_top.png').get_texture())
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
grassside = pyglet.graphics.TextureGroup(pyglet.image.load('grass_side.png').get_texture())
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
dirt = pyglet.graphics.TextureGroup(pyglet.image.load('dirt.png').get_texture())
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
cobble = pyglet.graphics.TextureGroup(pyglet.image.load('cobblestone.png').get_texture())
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, pos, block):
        if block == "dirt":
            self.top = dirt
            self.side = dirt
            self.bottom = dirt
        if block == "grass":
            self.top = grasstop
            self.side = grassside
            self.bottom = dirt
        if block == "cobblestone":
            self.top = cobble
            self.side = cobble
            self.bottom = cobble

        #self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        
        x,y,z = pos
        X,Y,Z = x+1,y+1,z+1
        vLists.append(batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z)),tex_coords))
        vLists.append(batch.add(4,GL_QUADS,self.side,('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z)),tex_coords))
        vLists.append(batch.add(4,GL_QUADS,self.bottom,('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z)),tex_coords))
        vLists.append(batch.add(4,GL_QUADS,self.top,('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z)),tex_coords))
        vLists.append(batch.add(4,GL_QUADS,self.side,('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z)),tex_coords))
        vLists.append(batch.add(4,GL_QUADS,self.side,('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z)),tex_coords))


    #def draw(self):
        #self.batch.draw()

class Player:
    def __init__(self,pos=(5,12,5),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.xvel = 0
        self.yvel = 0
        self.zvel = 0
        self.speed = 0
        self.hitbox = (self.pos[0]+0.3, self.pos[0]-0.3, self.pos[1]+0.25, self.pos[1]-1.625, self.pos[2]+0.3, self.pos[2]-0.3)
        self.onGround = False
        #self.ch = Crosshair((5, 5, 5))

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90

    def update(self,dt,keys):
        premove = list(self.hitbox)
        s = dt*5 #speed factor
        self.yvel -= 0.000 #gravity
        rotY = -self.rot[1]/180*math.pi
        self.xvel *= 0.80
        self.zvel *= 0.80

        self.dx,self.dz = s*math.sin(rotY),s*math.cos(rotY)
        self.speed = math.sqrt((self.xvel*self.xvel) + (self.zvel * self.zvel))
        if self.speed < 0.06:
            if keys[key.W]: self.xvel+=self.dx; self.zvel-=self.dz
            if keys[key.S]: self.xvel-=self.dx; self.zvel+=self.dz
            if keys[key.A]: self.xvel-=self.dz; self.zvel-=self.dx
            if keys[key.D]: self.xvel+=self.dz; self.zvel+=self.dx
        
        if keys[key.P]: print(self.pos)
        if keys[key.R]: print(self.rot)
         # and self.pos[1] == 12: self.yvel += 0.2
        if keys[key.LSHIFT]: 
            self.yvel = -0.25
        else:
            self.yvel = 0
        #if self.onGround:
        if keys[key.SPACE]:
            self.yvel = 0.15 #jump power
            self.onGround = False
        elif not keys[key.LSHIFT]:
            self.yvel = 0
        #if not keys[key.SPACE] and not keys[key.LSHIFT]:
            #self.yvel = 0
        self.pos[0]+=self.xvel
        self.pos[1]+=self.yvel
        self.pos[2]+=self.zvel
        self.updateHitbox()
        precollide = self.pos # to test if a collision has forced the player's position to change
        self.collision(premove, 2)
    def updateHitbox(self):
        self.hitbox = (self.pos[0]+0.3, self.pos[0]-0.3, self.pos[1]+0.25, self.pos[1]-1.625, self.pos[2]+0.3, self.pos[2]-0.3)
    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.
        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.75
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in models:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.yvel = 0
                    break
        return p

    def collision(self, prevpos, height):
        if normalizeHitbox(prevpos) != normalizeHitbox(self.hitbox): #if the player has moved...
            if self.xvel < 0: #if left:
                block = check((int(self.hitbox[1]), int(self.pos[1]), int(self.pos[2])))
                block2 = check((int(self.hitbox[1]), int(self.pos[1])-1, int(self.pos[2])))
                #print(block)
                if block != False: #if the player would have entered a block
                    self.xvel = 0
                    self.pos[0] = models[block][0] + 1.3
                    self.updateHitbox()
                    #print("blockhit!")
                if block2 != False: #if the player would have entered a block
                    self.xvel = 0
                    self.pos[0] = models[block2][0] +1.3
                    self.updateHitbox()
                    #print("blockhit!")
            if self.xvel > 0: #if right:
                block = check((int(self.hitbox[0]), int(self.pos[1]), int(self.pos[2])))
                block2 = check((int(self.hitbox[0]), int(self.pos[1])-1, int(self.pos[2])))
                #print(block)
                if block != False: #if the player would have entered a block
                    self.xvel = 0
                    self.pos[0] = models[block][0] - 0.3
                    self.updateHitbox()
                    #print("blockhit!")
                if block2 != False: #if the player would have entered a block
                    self.xvel = 0
                    self.pos[0] = models[block2][0] -0.3
                    self.updateHitbox()
                    #print("blockhit!")
            if self.zvel < 0: #if left:
                block = check((int(self.pos[0]), int(self.pos[1]), int(self.hitbox[5])))
                block2 = check((int(self.pos[0]), int(self.pos[1])-1, int(self.hitbox[5])))
                #print(block)
                if block != False: #if the player would have entered a block
                    self.zvel = 0
                    self.pos[2] = models[block][2] + 1.3
                    self.updateHitbox()
                    #print("blockhit!")
                if block2 != False: #if the player would have entered a block
                    self.zvel = 0
                    self.pos[2] = models[block2][2] +1.3
                    self.updateHitbox()
                    #print("blockhit!")
            if self.zvel > 0: #if right:
                block = check((int(self.pos[0]), int(self.pos[1]), int(self.hitbox[4])))
                block2 = check((int(self.pos[0]), int(self.pos[1])-1, int(self.hitbox[4])))
                #print(block)
                if block != False: #if the player would have entered a block
                    self.zvel = 0
                    self.pos[2] = models[block][2] - 0.3
                    self.updateHitbox()
                    #print("blockhit!")
                if block2 != False: #if the player would have entered a block
                    self.zvel = 0
                    self.pos[2] = models[block2][2] -0.3
                    self.updateHitbox()
                    #print("blockhit!")
            if self.yvel < 0: #if falling:
                blocks = []
                blocks.append(check((int(self.hitbox[0]), int(self.hitbox[3]), int(self.hitbox[4]))))
                blocks.append(check((int(self.hitbox[1]), int(self.hitbox[3]), int(self.hitbox[4]))))
                blocks.append(check((int(self.hitbox[0]), int(self.hitbox[3]), int(self.hitbox[5]))))
                blocks.append(check((int(self.hitbox[1]), int(self.hitbox[3]), int(self.hitbox[5]))))
                print(blocks)
                self.onGround = False
                for block in blocks:
                    if block != False: #if the player would have entered a block
                        self.yvel = 0
                        self.pos[1] = models[block][1] + 2.625
                        self.updateHitbox()
                        self.onGround = True
                        #print("blockhit!")
            if self.yvel > 0: #if rising:
                block = check((int(self.pos[0]), int(self.hitbox[2]), int(self.pos[2])))
                #print(block)
                if block != False: #if the player would have entered a block
                    self.yvel = 0
                    self.pos[1] = models[block][1] - 0.375
                    self.updateHitbox()
                    #print("blockhit!")

class Window(pyglet.window.Window):

    def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2],)
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
        for i in range(models.__len__()):
            Model(models[i], texs[i])
        
        self.player = Player((5, 15, 5),(-30,0))

        self.reticle = None

        self.availableBlocks = ["cobblestone", "grass", "dirt"]
        self.currBlock = 0

        # The label that is displayed in the top left of the canvas.
        #self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            #x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            #color=(0, 0, 0, 255))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock
        elif KEY == key.B:
            if self.currBlock != self.availableBlocks.__len__() - 1:
                self.currBlock += 1
            else:
                self.currBlock = 0

        
    
    def on_mouse_press(self, x, y, BUTTON, MOD):
        vector = self.get_sight_vector()
        block, previous = self.hit_test(self.player.pos, vector)
        print(block)
        if (BUTTON == mouse.RIGHT) or \
                ((BUTTON == mouse.LEFT) and (MOD & key.MOD_CTRL)):
            # ON OSX, control + left click = right click.
            if previous:
                models.append(previous)
                texs.append(self.availableBlocks[self.currBlock])
                Model(previous, self.availableBlocks[self.currBlock])

        elif BUTTON == mouse.LEFT:
            print(block)
            ind = models.index(block)
            models.pop(ind)
            print(ind)
            for i in range(6):
                vLists[ind*6].delete()
                vLists.pop(ind*6)


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

    def update(self,dt):
        self.player.update(dt,self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        glColor3d(1, 1, 1)
        self.push(self.player.pos,self.player.rot)
        self.clear()
        
        batch.draw()
        self.set2d()
        self.draw_reticle()
        glPopMatrix()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)
    
    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.draw()

    def hit_test(self, position, vector, max_distance=4):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 4
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and check(key) != False:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x = self.player.rot[1]*-1
        y = self.player.rot[0]
        print(self.player.rot)
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

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.
    Parameters
    ----------
    position : tuple of len 3
    Returns
    -------
    block_position : tuple of ints of len 3
    """
    x, y, z = position
    x, y, z = (int(x), int(y), int(z))
    return (x, y, z)

def normalizeHitbox(dimensions):
    return((dimensions[0], dimensions[1], dimensions[2], dimensions[3], dimensions[4], dimensions[5]))

def check(coords):
    coordsfix = (coords[0], coords[1], coords[2])
    if coordsfix in models:
        return models.index(coordsfix)
    else:
        return False


if __name__ == '__main__':
    window = Window(width=854,height=480,caption='Minecraft',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    pyglet.app.run()