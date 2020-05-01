import pygame
import random
import os
import math
GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad

class Config(object):
    """ a class to hold all game constants that may be modded by the user"""
    fullscreen = False
    width = 640
    height = 480
    fps = 60

class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class Text(pygame.sprite.Sprite):
    """ a helper class to write text on the screen """
    number = 0 
    book = {}
    def __init__(self, pos, msg):
        self.number = Text.number # get a unique number
        Text.number += 1 # prepare number for next Textsprite
        Text.book[self.number] = self # store myself into the book
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.msg = msg
        self.changemsg(msg)
 
    def update(self, seconds):        
        pass
 
    def changemsg(self,msg):
        self.msg = msg
        self.image = write(self.msg)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

class Healthbar(pygame.sprite.Sprite):
    """shows a bar with the hitpoints of a Tank sprite"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.boss = boss
        self.image = pygame.Surface((self.boss.rect.width,7))
        self.image.set_colorkey((0,0,0)) # black transparent
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        self.bossnumber = self.boss.number # the unique number (name) of my boss
            
    def update(self, time):
        self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
            pygame.draw.rect(self.image, (0,255,0), (1,1,
                int(self.boss.rect.width * self.percent),5),0) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
        #check if boss is still alive
        if not Tank.book[self.bossnumber]:
            self.kill() # kill the hitbar
 
class Bullet(pygame.sprite.Sprite):
    """ a big projectile fired by the tank's main cannon"""
    side = 7 # small side of bullet rectangle
    vel = 180 # velocity
    mass = 50
    maxlifetime = 10.0 # seconds
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.lifetime = 0.0
        self.color = self.boss.color
        self.calculate_heading() # !!!!!!!!!!!!!!!!!!!
        self.dx += self.boss.dx
        self.dy += self.boss.dy # add boss movement
        self.pos = self.boss.pos[:] # copy (!!!) of boss position 
        self.calculate_origin()
        self.update() # to avoid ghost sprite in upper left corner, 
                      # force position calculation.
 
    def calculate_heading(self):
        """ drawing the bullet and rotating it according to it's launcher"""
        self.radius = Bullet.side # for collision detection
        self.angle += self.boss.turretAngle
        self.mass = Bullet.mass
        self.vel = Bullet.vel
        image = pygame.Surface((Bullet.side * 2, Bullet.side)) # rect 2 x 1
        image.fill((128,128,128)) # fill grey
        pygame.draw.rect(image, self.color, (0,0,int(Bullet.side * 1.5), Bullet.side)) # rectangle 1.5 length
        pygame.draw.circle(image, self.color, (int(self.side *1.5) ,self.side//2), self.side//2) #  circle
        image.set_colorkey((128,128,128)) # grey transparent
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.dx = math.cos(degrees_to_radians(self.boss.turretAngle)) * self.vel
        self.dy = math.sin(degrees_to_radians(-self.boss.turretAngle)) * self.vel
 
    def calculate_origin(self):
        # - spawn bullet at end of turret barrel instead tank center -
        # cannon is around Tank.side long, calculatet from Tank center
        # later subtracted 20 pixel from this distance
        # so that bullet spawns closer to tank muzzle
        self.pos[0] +=  math.cos(degrees_to_radians(self.boss.turretAngle)) * (Tank.side-20)
        self.pos[1] +=  math.sin(degrees_to_radians(-self.boss.turretAngle)) * (Tank.side-20)
 
    def update(self, seconds=0.0):
        # ---- kill if too old ---
        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()
        # ------ calculate movement --------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        # ----- kill if out of screen
        if self.pos[0] < 0:
            self.kill()
        elif self.pos[0] > Config.width:
            self.kill()
        if self.pos[1] < 0:
            self.kill()
        elif self.pos[1] > Config.height:
            self.kill()
        #------- move -------
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)
  
class Tank(pygame.sprite.Sprite):
    """ A Tank, controlled by the Player with Keyboard commands.
    This Tank draw it's own Turret (including the main gun) 
    and it's bow rectangle (slit for Tracer Machine Gun"""
    side = 100 # side of the quadratic tank sprite
    recoiltime = 0.75 # how many seconds  the cannon is busy after firing one time
    turretTurnSpeed = 25 # turret
    tankTurnSpeed = 8 # tank
    movespeed = 25
    maxrotate = 360 # maximum amount of degree the turret is allowed to rotate
    book = {} # a book of tanks to store all tanks
    number = 0 # each tank gets his own number
    # keys for tank control, expand if you need more tanks
    #          player1,        player2    etc
    firekey = (pygame.K_SPACE, pygame.K_SLASH)
    turretLeftkey = (pygame.K_q, pygame.K_COMMA)
    turretRightkey = (pygame.K_e, pygame.K_PERIOD)
    forwardkey = (pygame.K_w, pygame.K_UP)
    backwardkey = (pygame.K_s, pygame.K_DOWN)
    tankLeftkey = (pygame.K_a, pygame.K_LEFT)
    tankRightkey = (pygame.K_d, pygame.K_RIGHT)
    color = ((200,200,0), (0,0,200))
    msg = ["WASD QE LSHIFT", "ARROWS <> RSHIFT"]
 
    def __init__(self, startpos = (150,150), angle=0):
        self.number = Tank.number # now i have a unique tank number
        Tank.number += 1 # prepare number for next tank
        Tank.book[self.number] = self # store myself into the tank book
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.pos = [startpos[0], startpos[1]] # x,y
        self.dx = 0
        self.dy = 0
        self.hitpointsfull = 100
        self.hitpoints = 100
        self.ammo = 30 # main gun
        self.msg =  "player%i: ammo: %i keys: %s" % (self.number+1, self.ammo, Tank.msg[self.number])
        Text((Config.width/2, 30+20*self.number), self.msg) # create status line text sprite
        self.color = Tank.color[self.number]
        self.turretAngle = angle #turret facing
        self.tankAngle = angle # tank facing
        self.firekey = Tank.firekey[self.number] # main gun
        self.turretLeftkey = Tank.turretLeftkey[self.number] # turret
        self.turretRightkey = Tank.turretRightkey[self.number] # turret
        self.forwardkey = Tank.forwardkey[self.number] # move tank
        self.backwardkey = Tank.backwardkey[self.number] # reverse tank
        self.tankLeftkey = Tank.tankLeftkey[self.number] # rotate tank
        self.tankRightkey = Tank.tankRightkey[self.number] # rotat tank
        # painting facing north, have to rotate 90° later
        image = pygame.Surface((Tank.side,Tank.side)) # created on the fly
        image.fill((128,128,128)) # fill grey
        if self.side > 10:
             pygame.draw.rect(image, self.color, (5,5,self.side-10, self.side-10)) #tank body, margin 5
             pygame.draw.rect(image, (90,90,90), (0,0,self.side//6, self.side)) # track left
             pygame.draw.rect(image, (90,90,90), (self.side-self.side//6, 0, self.side,self.side)) # right track
             pygame.draw.rect(image, (255,0,0), (self.side//6+5 , 10, 10, 5)) # red bow rect left
             #pygame.draw.rect(image, (255,0,0), (self.side/2 - 5, 10, 10, 5)) # red bow rect middle
        pygame.draw.circle(image, (255,0,0), (self.side//2,self.side//2), self.side//3 , 2) # red circle for turret
        image = pygame.transform.rotate(image,-90) # rotate so to look east
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        #---------- turret ------------------
        self.firestatus = 0.0 # time left until cannon can fire again
        self.turndirection = 0    # for turret
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed
        Turret(self) # create a Turret for this tank
        #---------- Healthbar ------------
        Healthbar(self)
        #---------- Sounds -----------
        try:
            filepath = os.path.dirname(__file__)
            datapath = os.path.join(filepath, "data")
            cannonshot = pygame.mixer.Sound(os.path.join(datapath,'cannon.wav'))
            explosion = pygame.mixer.Sound(os.path.join(datapath,'explosion.wav'))
        except:
            pass
        self.explosion = explosion
        self.cannonshot = cannonshot
    
    def death(self):
        self.explosion.play()
        Tank.book[self.number] = None # kill Tank in sprite dictionary
        pygame.sprite.Sprite.kill(self) # destroy the actual tank

    def update(self, seconds):
        # no need for seconds but the other sprites need it
        #-------- reloading, firestatus----------
        if self.firestatus > 0:
            self.firestatus -= seconds # cannon will soon be ready again
            if self.firestatus <0:
                self.firestatus = 0 #avoid negative numbers 

        # ------------ keyboard --------------
        pressedkeys = pygame.key.get_pressed()

        # -------- turret manual rotate ----------
        self.turndirection = 0    #  left / right turret rotation
        if pressedkeys[self.turretLeftkey]:
            self.turndirection += 1
        if pressedkeys[self.turretRightkey]:
            self.turndirection -= 1

        #---------- tank rotation ---------
        self.tankturndirection = 0 # reset left/right rotation
        if pressedkeys[self.tankLeftkey]:
            self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]:
            self.tankturndirection -= 1
 
        # ---------------- rotate tank ---------------
        self.tankAngle += self.tankturndirection * self.tankTurnSpeed * seconds # time-based turning of tank
        # angle etc from Tank (boss)
        oldcenter = self.rect.center
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image0, self.tankAngle) 
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter 
        # if tank is rotating, turret is also rotating with tank !
        # -------- turret autorotate ----------
        self.turretAngle += self.tankturndirection * self.tankTurnSpeed * seconds  + self.turndirection * self.turretTurnSpeed * seconds # time-based turning
        # ---------- fire cannon -----------
        if (self.firestatus ==0) and (self.ammo > 0):
            if pressedkeys[self.firekey]:
                self.firestatus = Tank.recoiltime # seconds until tank can fire again
                Bullet(self)    
                self.cannonshot.play()
                self.ammo -= 1
                self.msg =  "player%i: ammo: %i keys: %s" % (self.number+1, self.ammo, Tank.msg[self.number])
                Text.book[self.number].changemsg(self.msg)
        # ---------- movement ------------
        self.dx = 0
        self.dy = 0
        self.forward = 0 # movement calculator
        if pressedkeys[self.forwardkey]:
            self.forward += 1
        if pressedkeys[self.backwardkey]:
            self.forward -= 1
        # if both are pressed togehter, self.forward becomes 0
        if self.forward == 1:
            self.dx =  math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy =  -math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        if self.forward == -1:
            self.dx =  -math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy =  math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        # ------------- check border collision ---------------------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        if self.pos[0] - self.side//2 <= 0:
            self.pos[0] += Config.width 
        if self.pos[0] + self.side//2 >= Config.width:
            self.pos[0] -= Config.width
        if self.pos[1] - self.side//2 <= 0:
            self.pos[1] += Config.height 
        if self.pos[1] + self.side//2 >= Config.height:
            self.pos[1] -= Config.height
        # ---------- paint sprite at correct position ---------
        self.rect.centerx = round(self.pos[0], 0) #x
        self.rect.centery = round(self.pos[1], 0) #y    
        # ---------- check if still alive ----------
        if self.hitpoints <= 0:
            self.death() 
 
class Turret(pygame.sprite.Sprite):
    """turret on top of tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.side = self.boss.side        
        self.bossnumber = self.boss.number
        self.images = {} # how much recoil after shooting, reverse order of apperance
        self.images[0] = self.draw_cannon(0)  # idle position
        self.images[1] = self.draw_cannon(1)
        self.images[2] = self.draw_cannon(2)
        self.images[3] = self.draw_cannon(3)
        self.images[4] = self.draw_cannon(4)
        self.images[5] = self.draw_cannon(5)
        self.images[6] = self.draw_cannon(6)
        self.images[7] = self.draw_cannon(7)
        self.images[8] = self.draw_cannon(8)  # position of max recoil
        self.images[9] = self.draw_cannon(4)
        self.images[10] = self.draw_cannon(0) # idle position
 
    def update(self, seconds):        
        # painting the correct image of cannon
        if self.boss.firestatus > 0:
            self.image = self.images[int(self.boss.firestatus // (Tank.recoiltime / 10.0))]
        else:
            self.image = self.images[0]
        # --------- rotating -------------
        # angle etc from Tank (boss)
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image, self.boss.turretAngle) 
        self.rect = self.image.get_rect()
        # ---------- move with boss ---------
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
        if not self.boss.book[self.bossnumber]:
            self.kill()
 
    def draw_cannon(self, offset):
         # painting facing right, offset is the recoil
         image = pygame.Surface((self.boss.side * 2,self.boss.side * 2)) # created on the fly
         image.fill((128,128,128)) # fill grey
         pygame.draw.circle(image, (255,0,0), (self.side,self.side), 22, 0) # red circle
         pygame.draw.circle(image, (0,255,0), (self.side,self.side), 18, 0) # green circle
         pygame.draw.rect(image, (255,0,0), (self.side-10, self.side + 10, 15,2)) # turret mg rectangle
         pygame.draw.rect(image, (0,255,0), (self.side-20 - offset,self.side - 5, self.side - offset,10)) # green cannon
         pygame.draw.rect(image, (255,0,0), (self.side-20 - offset,self.side - 5, self.side - offset,10),1) # red rect 
         image.set_colorkey((128,128,128))
         return image
# ---------------- End of classes --------------------
#------------ defs ------------------
def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0
 
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)
 
def write(msg="pygame is cool"):
    """helper function for the Text sprite"""
    myfont = pygame.font.SysFont("None", 28)
    mytext = myfont.render(msg, True, (255,0,0))
    mytext = mytext.convert_alpha()
    return mytext        
  
def play_game():
    """the game itself"""

def main(starting_scene):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    screen = pygame.display.set_mode((Config.width,Config.height))

    clock = pygame.time.Clock()    # create pygame clock object
    FPS = Config.fps               # desired max. framerate 

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        clock.tick(FPS)
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        
        # Event filtering 
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update(seconds)
        active_scene.Render(screen)
        
        active_scene = active_scene.next

        pygame.display.set_caption("FPS: %.2f, press ENTER to play" % ( clock.get_fps() ))
        pygame.display.flip()
    return 0

class MenuScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter 
                self.SwitchToScene(GameScene())
    
    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((110,110,110)) 
        background = background.convert()
        screen.blit(background, (0,0))

class GameScene(SceneBase):
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()    
    def __init__(self):
        SceneBase.__init__(self)
        self.tankgroup = GameScene.tankgroup
        self.bulletgroup = GameScene.bulletgroup
        self.allgroup = GameScene.allgroup

        Tank._layer = 4   # base layer
        Bullet._layer = 7 # to prove that Bullet is in top-layer
        Turret._layer = 6 # above Tank
        Text._layer = 3   # below Tank
        Healthbar._layer = 1 
    
        #assign default groups to each sprite class
        Healthbar.groups = self.allgroup
        Tank.groups = self.tankgroup, self.allgroup
        Turret.groups = self.allgroup
        Bullet.groups = self.bulletgroup, self.allgroup
        Text.groups = self.allgroup
        player1 = Tank((150,250), 90) # create  first tank, looking north
        player2 = Tank((450,250), -90) # create second tank, looking south
        status3 = Text((Config.width//2, 10), "Tank Demo. Press ESC to quit")
        try:
            filepath = os.path.dirname(__file__)
            datapath = os.path.join(filepath, "data")
            hit = pygame.mixer.Sound(os.path.join(datapath,'damage.wav'))
            self.hit = hit
        except:
            pass
    
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self, seconds):
        damagegroup = pygame.sprite.groupcollide(self.tankgroup, self.bulletgroup, False, True)
        for damaged in damagegroup:
                self.hit.play()
                damaged.hitpoints -= 25

        self.allgroup.update(seconds)
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((220,220,220)) # fill with color 
        background = background.convert()
        screen.blit(background, (0,0)) # delete all
        self.allgroup.clear(screen, background)
        self.allgroup.draw(screen)

if __name__ == '__main__':
    main(MenuScene() )