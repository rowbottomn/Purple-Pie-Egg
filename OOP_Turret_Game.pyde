    
add_library('minim')

#Global declarations
global WIDTH, HEIGHT
global MAX_ENEMIES
global base_scl, tur_scl, bul_scl, pla_scl, bom_scl
global bg, base, turret, bullet, turret_fire, turret_charging
global target, tar_pos, tar_vel
global images, alive
global center 


#Constants
WIDTH = 1172
HEIGHT = 1024#int(WIDTH*4/5)

MAX_ENEMIES = 20
g = 0.1

#Classes

#enemies
class Enemy:
    #class globals 
    global images, sounds
    global center
    global alive
    global turret_charging, tur_pos
    global bul_pos
    global drawImage
    #class variables
    
    
    #class constructor
    def __init__(self):
        #set the images
        # for i in range (0,4):
        #    img.append(images[20+i])
        self.state = 1 #0 = exists but not added in yet, 1 = alive and moving, 2 = attacking, 3 = dying, 4 = dead but still in play
        self.speed = 0.6

        self.delay = 40.
        self.intel = 200  #0 homes in, 360 is a random walk but it can still home in
        self.pos = PVector()
        self.vel = PVector()
        self.img_ctr = 1
        self.snd_ctr = 3
        self.img = images[1]
        self.scl = 1.0    
        alive.append(self)
        self.onSpawn()
        #set the sounds
            
        #load AI
        
        
    #class methods
    def onSpawn(self):
        global speed

        #get a random location
        #while (PVector.dist(center, self.pos) < WIDTH):
        self.pos = PVector.random2D()

        self.pos.mult(float(WIDTH/2.))
        self.pos.add(center)        
 #       text(str(self.pos), 500,100)

        return True
        
    def onHit(self):
        return True
    
    def onEnd(self):
        alive.remove(self)
        return True
    
    def attacking(self):
        return True
    
    def dying(self):
        return True
    
    def onUpdate(self):
        global images
        step = 0
        if (self.state == 1):
            if float(frameCount)%self.delay ==0:
                self.vel = center.copy()
                self.vel.sub(self.pos)
                self.vel.normalize()
                self.vel.mult(self.speed)
                step = (float(random(self.intel)-self.intel/2.)*(1.05*PVector.dist(center, self.pos)/float(WIDTH)))
                self.vel.rotate(PI*(step/180.))#moves a random amount from pointing directly at the player
                
                self.img_ctr += 1;
                if self.img_ctr > 3:
                    self.img_ctr = 0
                self.img = images[self.img_ctr+1]
            self.pos.add(self.vel)
            if detectHit(tur_pos, 40,self.pos, 20):
                self.state = 2
            elif detectHit(bul_pos, 40,self.pos, 20):
                self.state = 2            
        if (self.state ==2): 
            self.onEnd()
        return True
        
    def onDraw(self):
        drawImage(self.img, self.pos, self.vel.heading()+PI/2., self.scl)
        return True
    
#Program header

#Pseudocode

#enemies

#arrays
alive = []
ball_pos = []
ball_vel = []
targets = []
images = []
sounds = []

#Vectors
#space_base 
base_pos = PVector(WIDTH//2, HEIGHT//2)
base_scl = 0.15

#turret
#tur_offset = PVector(0,-30)
tur_pos = PVector(WIDTH//2-3, HEIGHT//2-2)
#tur_pos.add(tur_offset)
tur_dir = PVector(5, -5)

#bullet
bul_pos = PVector(10000,10000)
bul_vel = PVector(0)
bul_offset = PVector(40, 0);

#plane
pla_pos = PVector(WIDTH//2, HEIGHT)
pla_vel = PVector(5, -5)

#bomb
bom_pos = PVector(WIDTH//2, HEIGHT)
bom_vel = PVector(5, -5)

#target 
tar_pos = PVector(-10000, -10000)
tar_vel = PVector()

#other
acc = PVector(0, g)
center = PVector(WIDTH//2, HEIGHT//2)

#Variables

tur_scl = 0.5
bul_scl = 0.1
bom_scl = 1.0
pla_scl = 1.0

ball_num = 1000
#num_enemies

can_fire = True


#Setup
def setup():
    global WIDTH, HEIGHT
    global minim, music
    global turret_fire, images
    minim = Minim(this)
    size(WIDTH, HEIGHT)
    fill(250)
    stroke(255)
    background(0)
    imageMode(CENTER)
    rectMode(CENTER)
    cursor(CROSS) 
    #loading images and sounds
    loadAssets(minim)
    music.play()
    music.loop()
    test = Enemy()


def loadAssets(_minim):
    global bg, base, turret, turret_charging, bullet, turret_fire, music, images

#def loadAssets():
 #   global bg, base, turret, turret_charging, bullet, turret_fire, images, minim
#Images and Sounds
    #0-09  Titles and backgrounds
    #10-19 Player
    #20-49 Enemies
    #50-69 Buttons
    
    
    #images.append(loadImage ("space_bg.jpg"))
    images.append(loadImage("http://www.jpl.nasa.gov/spaceimages/images/largesize/PIA02408_hires.jpg"))
    images.append(loadImage("invader0.png"))
    images.append(loadImage("invader1.png"))
    images.append(loadImage("invader2.png"))
    images.append(loadImage("invader3.png"))
    base = loadImage("space_base.png")
    turret = loadImage("turret_green.png")
    turret_charging = loadImage("turret_charging2.png")#also used as explosion
    bullet = loadImage("fire_blast1.png")
    turret_fire = _minim.loadFile("turret_blast.mp3")
    music = _minim.loadFile("music.mp3")
    
#Methods   
def drawImage(_img, _pos, _dir, _size):
    pushMatrix()
    translate(_pos.x, _pos.y)
    rotate(_dir)
    scale(_size)
    image(_img, 0, 0)
    popMatrix()     
   
def detectHit(_vec1, _s1, _vec2, _s2):
    if PVector.dist(_vec1, _vec2) <= (_s1+_s2)/2:
        return True
    return False

#def spawnEnemy(num):
#    if num < 

def drawCharging(_img, _vec, _radius):
    global bul_pos, bul_vel, tur_dir, charging_pos,tur_pos, turret_charging
    for i in range (1,10):
        temp = PVector.random2D()
        temp.mult(_radius+i)
        temp.add(_vec)
        drawImage(_img, temp, 0, (2+1.5*i)/100.)
    _radius -= 0.3
    #if abs(_radius - 15.5) < 0.3:
       # fire_turret()
    text("start sound" + str(_radius), 100,100)
    if _radius  < 1: 
        bul_pos =_vec.copy() 
        bul_vel = tur_dir.copy()
    return _radius

def fire_turret():
    global turret_fire  
    if turret_fire.isPlaying() != True:
        turret_fire.rewind()
        turret_fire.play()
        
def keyPressed():
    test = 2
    
def keyReleased():
    test = 2



charging_radius = 26.
#Draw
def draw():
    global tur_pos, tur_dir
    background(images[0])
    global charging_radius, charging_pos
    mouse = PVector(mouseX, mouseY)
    mouse.sub(tur_pos)
    tur_dir = mouse.copy()
    bul_pos.add(bul_vel)
    text(str(len(alive))+str(int(120*(MAX_ENEMIES -1)//frameCount)), 400, 100)
    if (len(alive) + int(60*(MAX_ENEMIES -1)//frameCount)<MAX_ENEMIES ):
        alive.append(Enemy())
        #alive[-1].onSpawn()
       # background(255,0,0)
    for x in alive:
        x.onUpdate()
        x.onDraw()
        
    drawImage(base, base_pos, PI/10, base_scl)
    if mousePressed:
        if can_fire:
            if turret_fire.isPlaying() != True and charging_radius < 1:
                if charging_radius < 1:
                    charging_radius = 15.
        else:
            charging_pos = tur_pos.copy()
            tur_dir.normalize()
            tur_dir.mult(turret.height*0.21)
            charging_pos.add(tur_dir)
            charging_radius = drawCharging(turret_charging, charging_pos, charging_radius)
    drawImage(bullet, bul_pos, bul_vel.heading()+PI/2., bul_scl)
    drawImage(turret, tur_pos, tur_dir.heading() + PI/2., tur_scl)
    
 
        