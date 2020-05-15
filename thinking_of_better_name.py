import pygame
import pika
import uuid
import json
from threading import Thread
import random
import os
import math

class Config(object):
    fullscreen = False
    width = 1100
    height = 600
    fps = 60

    ip = '34.254.177.17'
    port = 5672
    v_host = 'dar-tanks'
    user = 'dar-tanks'
    password = '5orPLExUYnyVYZg48caMpX'

    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    move_keys = {
        pygame.K_w: UP,
        pygame.K_a: LEFT,
        pygame.K_s: DOWN,
        pygame.K_d: RIGHT
    }

class Jukebox(object):
    """a class to hold all sounds & music"""
    sound = []

class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("forgot to override")

    def Update(self):
        print("forgot to override")

    def Render(self, screen):
        print("forgot to override")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class TankRPCClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = Config.ip, port = Config.port, virtual_host = Config.v_host,
                credentials = pika.PlainCredentials(
                    username = Config.user, password = Config.password
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '', auto_delete = True, exclusive = True)
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(exchange = 'X:routing.topic', queue = self.callback_queue)
        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack = True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message = {}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange = 'X:routing.topic',
            routing_key = key,
            properties = pika.BasicProperties(
                reply_to = self.callback_queue,
                correlation_id = self.corr_id,
            ),
            body = json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()

    def healthcheck(self):
        self.call('tank.request.healthcheck')

    def register(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']

    def quick_match(self):
        quick_number = 1
        while self.room_id == None:
            quick_number += 1
            if quick_number > 30:
                break
            quick_room_id = 'room-' + str(quick_number)
            self.register(quick_room_id)

    def tank_turn(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def tank_fire(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):
    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = Config.ip, port = Config.port, virtual_host = Config.v_host,
                credentials = pika.PlainCredentials(
                    username = Config.user, password = Config.password
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '', auto_delete = True, exclusive = True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange = 'X:routing.topic', queue = event_listener, routing_key = 'event.state.' + room_id)
        self.channel.basic_consume(
            queue = event_listener,
            on_message_callback = self.on_response,
            auto_ack = True,
            consumer_tag = 'stop_this_please'
        )
        
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()

class Text(pygame.sprite.Sprite):
    """ a helper class to write text on the screen """
    number = 0 
    book = {}
    def __init__(self, pos, msg, color = (255, 0, 0)):
        self.number = Text.number # get a unique number
        Text.number += 1 # prepare number for next Textsprite
        Text.book[self.number] = self # store myself into the book
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.msg = msg
        self.changemsg(msg, color)
 
    def update(self, seconds):        
        pass
 
    def changemsg(self, msg, color):
        self.msg = msg
        self.color = color
        self.image = write(self.msg, self.color)
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

class Food(pygame.sprite.Sprite):
    image = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [random.randint(15, Config.width-15), random.randint(15, Config.height-15)]
        image = Food.image[0]
        small_image = pygame.transform.scale(image, (25, 25))
        self.image = small_image
        self.rect = self.image.get_rect()
        self.update()

    def update(self, seconds = 0.0):
        self.rect.centerx = round(self.pos[0], 0) #x
        self.rect.centery = round(self.pos[1], 0) #y

class Bullet(pygame.sprite.Sprite):
    """ a big projectile fired by the tank's main cannon"""
    image = []
    vel = 3 # velocity
    maxlifetime = 7.5 # seconds
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.lifetime = 0.0
        self.calculate_heading() # !!!!!!!!!!!!!!!!!!!
        self.pos = self.boss.pos[:] # copy (!!!) of boss position 
        self.calculate_origin()
        self.update() # to avoid ghost sprite in upper left corner, 
                      # force position calculation.
 
    def calculate_heading(self):
        """ drawing the bullet and rotating it according to it's launcher"""
        self.angle += self.boss.tankAngle
        self.vel = Bullet.vel
        image = Bullet.image[0]
        small_image = pygame.transform.scale(image, (15, 15))
        self.image0 = small_image
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.dx = self.boss.dx * self.vel
        self.dy = self.boss.dy * self.vel
        if self.dx == 0 and self.dy == 0:
            self.dx = 300
 
    def calculate_origin(self):
        if self.angle == 0:
            self.pos[0] += 28
        elif self.angle == 90:
            self.pos[1] += -28
        elif self.angle == 180:
            self.pos[0] += -28
        elif self.angle == 270:
            self.pos[1] += 28
 
    def update(self, seconds=0.0):
        # ---- kill if too old ---
        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()
        # ------ calculate movement --------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        if self.pos[0] <= 0:
            self.pos[0] += Config.width 
        if self.pos[0]>= Config.width:
            self.pos[0] -= Config.width
        if self.pos[1] <= 0:
            self.pos[1] += Config.height 
        if self.pos[1] >= Config.height:
            self.pos[1] -= Config.height
        #------- move -------
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, ex_pos = None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0, 0]
        self.calculate_place(ex_pos)
        # -------- Creation -----------
        self.image = pygame.Surface((40, 40))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.update()

    def calculate_place(self, ex_pos):
        while self.pos[0] == 0:
            pos_x = random.randint (20, Config.width-20)
            if not (ex_pos[0] - 40) < pos_x < (ex_pos[0] + 40):
                self.pos[0] = pos_x
        while self.pos[1] == 0:
            pos_y = random.randint(20, Config.height)
            if not (ex_pos[1] - 40) < pos_y < (ex_pos[1] + 40):
                self.pos[1] = pos_y
    
    def update(self, seconds = 0.0):
        self.rect.centerx = round(self.pos[0], 0) #x
        self.rect.centery = round(self.pos[1], 0) #y

class Tank(pygame.sprite.Sprite):
    image = [] # list of all images
    movespeed = 100
    book = {} # a book of tanks to store all tanks
    number = 0 # each tank gets his own number
    def __init__(self, startpos = (150,150)):
        self.number = Tank.number # now i have a unique tank number
        Tank.number += 1 # prepare number for next tank
        Tank.book[self.number] = self # store myself into the tank book
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.pos = [startpos[0], startpos[1]] # x,y
        self.tankAngle = 0
        image = Tank.image[0]
        small_image = pygame.transform.scale(image, (40, 25))
        self.image = small_image
        self.image0 = self.image
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        self.movespeed = Tank.movespeed
        self.firestatus = 0.0
        #--------- Healthbar ---------
        self.hitpointsfull = 3
        self.hitpoints = 3
        Healthbar(self)
        #---------- Sounds -----------
        self.explosion = Jukebox.sound[4]
        self.cannonshot = Jukebox.sound[3]

    def death(self):
        self.explosion.play()
        Tank.book[self.number] = None # kill Tank in sprite dictionary
        pygame.sprite.Sprite.kill(self) # destroy the actual tank

    def update(self, seconds):
        # ------------ keyboard --------------
        pressedkeys = pygame.key.get_pressed()
        #-------- reloading, firestatus----------
        if self.firestatus > 0:
            self.firestatus -= seconds # cannon will soon be ready again
            if self.firestatus <0:
                self.firestatus = 0 #avoid negative numbers 
        # ---------- fire cannon -----------
        if self.firestatus == 0:
            if pressedkeys[pygame.K_SPACE]:
                self.firestatus = 1.0 # seconds until tank can fire again
                Bullet(self)
                self.cannonshot.play()
        # ---------- movement ------------
        if pressedkeys[pygame.K_RIGHT]:
            self.dx = self.movespeed
            self.dy = 0
            self.tankAngle = 0
        elif pressedkeys[pygame.K_UP]:
            self.dx = 0
            self.dy = -self.movespeed
            self.tankAngle = 90
        elif pressedkeys[pygame.K_LEFT]:
            self.dx = -self.movespeed
            self.dy = 0
            self.tankAngle = 180
        elif pressedkeys[pygame.K_DOWN]:
            self.dx = 0
            self.dy = self.movespeed
            self.tankAngle = 270
        # -------------- rotation ---------------
        oldcenter = self.rect.center
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image0, self.tankAngle) 
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter 
        # ------------- check border collision ---------------------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        if self.pos[0] <= 0:
            self.pos[0] += Config.width 
        if self.pos[0]>= Config.width:
            self.pos[0] -= Config.width
        if self.pos[1] <= 0:
            self.pos[1] += Config.height 
        if self.pos[1] >= Config.height:
            self.pos[1] -= Config.height
        # ---------- paint sprite at correct position ---------
        self.rect.centerx = round(self.pos[0], 0) #x
        self.rect.centery = round(self.pos[1], 0) #y    
        # ---------- check if still alive ----------
        if self.hitpoints <= 0:
            self.death() 

def write(msg = "pygame is cool", color = (255, 0, 0)):
    """helper function for the Text sprite"""
    myfont = pygame.font.SysFont("None", 28)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext

def draw_tank(screen, id_1, id_2, x, y, width, height, direction):
    if id_1 == id_2:
        image = Tank.image[0]
    else:
        image = Tank.image[1]
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    if direction == 'RIGHT':
        tank_angle = 0
    elif direction == 'UP':
        tank_angle = 90
    elif direction == 'LEFT':
        tank_angle = 180
    elif direction == 'DOWN':
        tank_angle = 270
    image  = pygame.transform.rotate(image, tank_angle)
    nickname = write('{}'.format(id_1), (200,200,200))
    screen.blit(image, (x, y))
    screen.blit(nickname, (x-20, y-30))

def draw_bullet(screen, owner, id_2, x, y, width, height, direction):
    if owner == id_2:
        image = Bullet.image[0]
    else: 
        image = Bullet.image[1]
    image = image.convert_alpha()
    if direction == 'RIGHT':
        bullet_angle = 0
    elif direction == 'UP':
        bullet_angle = 90
    elif direction == 'LEFT':
        bullet_angle = 180
    elif direction == 'DOWN':
        bullet_angle = 270
    image = pygame.transform.rotate(image, bullet_angle)
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x, y))

def key_sort(e):
    return e['Score']

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
                try:
                    active_scene.client.connection.close()
                    active_scene.event_client.channel.basic_cancel(consumer_tag = 'stop_this_please')
                except:
                    pass
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update(seconds)
        active_scene.Render(screen)
        
        active_scene = active_scene.next

        pygame.display.set_caption("FPS: %.2f" % ( clock.get_fps() ))
        pygame.display.flip()
    return 0

class LoadingScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, seconds):
        try:
            filepath = os.path.dirname(__file__)
            datapath = os.path.join(filepath, "data")
            Jukebox.sound.append(pygame.mixer.Sound(os.path.join(datapath,'damage.wav')))
            Jukebox.sound.append(pygame.mixer.Sound(os.path.join(datapath,'click.wav')))
            Jukebox.sound.append(pygame.mixer.Sound(os.path.join(datapath,'crunch.wav')))
            Jukebox.sound.append(pygame.mixer.Sound(os.path.join(datapath,'cannon.wav')))
            Jukebox.sound.append(pygame.mixer.Sound(os.path.join(datapath,'explosion.wav')))
            Tank.image.append(pygame.image.load(os.path.join(datapath,"tank.png")))
            Tank.image.append(pygame.image.load(os.path.join(datapath,"tank_red.png")))
            Food.image.append(pygame.image.load(os.path.join(datapath,"combat_rations.png")))
            Bullet.image.append(pygame.image.load(os.path.join(datapath,"bullet.png")))
            Bullet.image.append(pygame.image.load(os.path.join(datapath,"bullet_blue.png")))
        except:
            pass
        self.SwitchToScene( MainMenuScene() )

    def Render(self, screen):
        pass

class MainMenuScene(SceneBase):
    textgroup = pygame.sprite.LayeredUpdates()
    def __init__(self):
        SceneBase.__init__(self)
        self.textgroup = MainMenuScene.textgroup
        Text._layer = 2
        Text.groups = self.textgroup
        very_cool_name = Text( (Config.width//2, 100), "NOT SO DEMO TANKS THIS TIME", (250, 250, 250))
        option1 = Text( (Config.width//2, 160), "Single Player", (255, 255, 255))
        option2 = Text( (Config.width//2, 200), "Multiplayer", (255, 255, 255))
        option3 = Text( (Config.width//2, 240), "Multiplayer Auto", (255, 255, 255))
        option4 = Text( (Config.width//2, 280), "Quit", (255, 255, 255))
        how_to_choose = Text( (Config.width//2, 360), "Use arrows and ENTER to select a mode", (80, 80, 80))
        point_at = 0
        self.point_at = point_at
        options = (140, 180, 220, 260)
        self.options = options

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.point_at -= 1
                elif event.key == pygame.K_DOWN:
                    self.point_at += 1
                elif event.key == pygame.K_RETURN:
                    # Move to the next scene when the user pressed Enter 
                    if self.point_at == 0:
                        self.SwitchToScene( SinglePlayerScene() )
                    elif self.point_at == 1:
                        self.SwitchToScene( MultiPlayerScene() )
                    elif self.point_at == 2:
                        self.SwitchToScene( MultiBotsScene() )
                    elif self.point_at == 3:
                        self.Terminate()
    
    def Update(self, seconds):
        self.textgroup.update(seconds)
        if self.point_at > 3:
            self.point_at = 0
        elif self.point_at < 0:
            self.point_at = 3
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((50,50,50)) 
        background = background.convert()
        screen.blit(background, (0,0))
        choicesurface = pygame.Surface((250, 40))
        choicesurface.set_colorkey((0, 0, 0))
        pygame.draw.rect(choicesurface, (250, 250, 250), (0, 0, 240, 38), 2)
        choicesurface = choicesurface.convert_alpha()
        screen.blit(choicesurface, ((Config.width//2)-120, self.options[self.point_at]))
        self.textgroup.clear(screen, background)
        self.textgroup.draw(screen)

class SinglePlayerScene(SceneBase):
    spawn_food = pygame.USEREVENT + 1
    power_down = pygame.USEREVENT + 2
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    wallgroup = pygame.sprite.Group()
    consumables = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
    def __init__(self):
        SceneBase.__init__(self)
        self.spawn_food = SinglePlayerScene.spawn_food
        self.power_down = SinglePlayerScene.power_down

        self.tankgroup = SinglePlayerScene.tankgroup
        self.bulletgroup = SinglePlayerScene.bulletgroup
        self.wallgroup = SinglePlayerScene.wallgroup
        self.consumables = SinglePlayerScene.consumables
        self.allgroup = SinglePlayerScene.allgroup

        Wall._layer = 3
        Tank._layer = 4
        Food._layer = 5
        Bullet._layer = 6
        Healthbar._layer = 7

        Healthbar.groups = self.allgroup
        Tank.groups = self.tankgroup, self.allgroup
        Bullet.groups = self.bulletgroup, self.allgroup
        Wall.groups = self.wallgroup, self.allgroup
        Food.groups = self.consumables, self.allgroup

        player_single = Tank((random.randint(0,Config.width), random.randint(0,Config.height)))
        for i in range(8):
            Wall(player_single.pos)
        pygame.time.set_timer(self.spawn_food, random.randint(5000,30000))
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == self.spawn_food:
                Food()
                Jukebox.sound[1].play()
            elif event.type == self.power_down:
                for powered_up in self.tankgroup:
                    if powered_up.movespeed > 100:
                        powered_up.movespeed = 100
                        powered_up.dx *= 0.5
                        powered_up.dy *= 0.5
                pygame.time.set_timer(self.power_down, 0)
        
    def Update(self, seconds):
        super_power = pygame.sprite.groupcollide(self.tankgroup, self.consumables, False, True)
        for powered_up in super_power:
            Jukebox.sound[2].play()
            powered_up.movespeed *= 2
            powered_up.dx *= 2
            powered_up.dy *= 2
            pygame.time.set_timer(self.power_down, 5000)
        wallcrash_1 = pygame.sprite.groupcollide(self.bulletgroup, self.wallgroup, True, True)
        for crashed in wallcrash_1:
            Jukebox.sound[0].play()
        wallcrash_2 = pygame.sprite.groupcollide(self.tankgroup, self.wallgroup, False, True)
        for crashed in wallcrash_2:
            Jukebox.sound[0].play()
            crashed.hitpoints -= 1
        damagegroup = pygame.sprite.groupcollide(self.tankgroup, self.bulletgroup, False, False)
        for damaged in damagegroup:
            for hits in damagegroup[damaged]:
                if hits.boss != damaged:
                    hits.kill()
                    Jukebox.sound[0].play()
                    damaged.hitpoints -= 1
        self.allgroup.update(seconds)
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((110, 110, 110)) 
        background = background.convert()
        screen.blit(background, (0, 0))
        self.allgroup.clear(screen, background)
        self.allgroup.draw(screen)

class MultiPlayerScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.client = TankRPCClient()
        self.client.healthcheck()
        self.client.quick_match()
        if self.client.room_id != None:
            self.event_client = TankConsumerClient(self.client.room_id)
            self.event_client.start()
        elif self.client.room_id == None:
            self.Terminate()
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in Config.move_keys:
                    self.client.tank_turn(self.client.token, Config.move_keys[event.key])
                if event.key == pygame.K_SPACE:
                    self.client.tank_fire(self.client.token)
                    Jukebox.sound[3].play()
        
    def Update(self, seconds):
        winners = self.event_client.response['winners']
        losers = self.event_client.response['losers']
        kicked = self.event_client.response['kicked']
        for winner in winners:
            if self.client.tank_id == winner['tankId']:
                self.SwitchToScene( GameOverScreen(winner['score'], 1) )
                self.client.connection.close()
                self.event_client.channel.basic_cancel(consumer_tag = 'stop_this_please')
        for loser in losers:
            if self.client.tank_id == loser['tankId']:
                self.SwitchToScene( GameOverScreen(loser['score'], 2) )
                self.client.connection.close()
                self.event_client.channel.basic_cancel(consumer_tag = 'stop_this_please')
        for afk in kicked:
            if self.client.tank_id == afk['tankId']:
                self.SwitchToScene( GameOverScreen(afk['score'], 3) )
                self.client.connection.close()
                self.event_client.channel.basic_cancel(consumer_tag = 'stop_this_please')

    def Render(self, screen):
        background = pygame.Surface((830, 600))
        background.fill((110, 110, 110)) 
        background = background.convert()
        screen.blit(background, (0, 0))
        leaderboard = []
        try:
            tanks = self.event_client.response['gameField']['tanks']
            bullets = self.event_client.response['gameField']['bullets']
            self.remaining_time = self.event_client.response['remainingTime']
            for tank in tanks:
                tank_id = tank['id']
                if tank_id == self.client.tank_id:
                    self.health_points = tank['health']
                    self.score = tank['score']
                else:
                    enemy_dict = {'ID': '{}'.format(tank_id), 'HP': tank['health'], 'Score': tank['score']}
                    # leaderboard.append(write('{}: {}/{}'.format(tank_id, tank['health'], tank['score'])))
                    leaderboard.append(enemy_dict)
                    leaderboard.sort(key=key_sort)
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                draw_tank(screen, tank_id, self.client.tank_id, tank_x, tank_y, tank_width, tank_height, tank_direction)
            for bullet in bullets:
                bullet_id = bullet['owner']
                bullet_x = bullet['x']
                bullet_y = bullet['y']
                bullet_width = bullet['width']
                bullet_height = bullet['height']
                bullet_direction = bullet['direction']
                draw_bullet(screen, bullet_id, self.client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
        except:
            pass
        info_HUD = pygame.Surface((270, 600))
        info_HUD.fill((55,55,55))
        info_HUD = info_HUD.convert()
        info_border = pygame.draw.rect(info_HUD, (192,192,192), (0,0,270,600), 2)
        info_1 = write('Health Points: {}'.format(self.health_points), (200,200,200))
        score_1 = write('Your Score: {}'.format(self.score), (200,200,200))
        try:
            server_timer = write('Remaining Time: {}'.format(self.remaining_time), (200,200,200))
            info_HUD.blit(server_timer, (10, 570))
            for enemy in leaderboard:
                score_enemy = write('{}: {}/{}'.format(enemy['ID'], enemy['HP'], enemy['Score']))
                info_HUD.blit(score_enemy, (10, 80 + (20 * leaderboard.index(enemy))))
        except:
            pass
        info_HUD.blit(info_1, (10, 10))
        info_HUD.blit(score_1, (10, 30))
        screen.blit(info_HUD, (830, 0))

class MultiBotsScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((0, 0, 255)) 
        background = background.convert()
        screen.blit(background, (0, 0))

class GameOverScreen(SceneBase):
    def __init__(self, final_score, reason):
        SceneBase.__init__(self)
        self.final_score = final_score
        # reason = 1 if winner, 2 if loser, 3 if kicked
        self.reason = reason
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.SwitchToScene( MultiPlayerScene() )
        
    def Update(self, seconds):
        pass
    
    def Render(self, screen):
        background = pygame.Surface((screen.get_size()))
        background.fill((0, 0, 0)) 
        background = background.convert()
        if self.reason == 1:
            victory = write('VICTORY', (175,238,238))
            victory_quote = write('As victories mount, so too will resistance', (255,255,255))
            background.blit(victory, ((Config.width//2)-120, 180))
            background.blit(victory_quote, ((Config.width//2)-120, 210))
        elif self.reason == 2:
            defeat = write('DEFEAT', (220,20,60))
            defeat_quote = write('Where there is no peril in the task, there can be no glory in its accomplishment', (255,255,255))
            background.blit(defeat, ((Config.width//2)-220, 180))
            background.blit(defeat_quote, ((Config.width//2)-120, 210))
        elif self.reason == 3:
            kicked = write('KICKED', (250, 250, 250))
            kicked_quote = write('You were kicked from the game', (255,255,255))
            background.blit(kicked, ((Config.width//2)-120, 180))
            background.blit(kicked_quote, ((Config.width//2)-120, 210))
        your_score = write('YOUR FINAL SCORE IS: {}'.format(self.final_score), (255,255,255))
        r_to_restart = write('Press R to Restart', (255,255,255))
        esc_to_exit = write('Press ESC to Exit', (255,255,255))
        background.blit(your_score, ((Config.width//2)-120, 250))
        background.blit(r_to_restart, ((Config.width//2)-120, (Config.height)-60))
        background.blit(esc_to_exit, ((Config.width//2)-120, (Config.height)-30))
        screen.blit(background, (0, 0))

if __name__ == '__main__':
    main( LoadingScene() )