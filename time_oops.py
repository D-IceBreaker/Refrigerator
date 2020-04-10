import pygame 
import random

class PygView(object):

    def __init__(self, width = 640, height = 480, fps = 60):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.screenrect = self.screen.get_rect()
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255, 255, 255))
        self.background2 = self.background.copy()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
    
    def wildPainting(self):
        pygame.draw.circle(self.background, (random.randint(0,255),
                       random.randint(0,255), random.randint(0,255)),
                       (random.randint(0, self.screenrect.width),
                       random.randint(0, self.screenrect.height)),
                       random.randint(50, 500))

    def run(self):
        myball = Ball() 
        myball.blit(self.screen) 
        running = True
        paint_big_circles = False
        cleanup = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.fps += 10
                        if self.fps > 1000:
                            self.fps = 1000
                    elif event.key == pygame.K_DOWN:
                        self.fps -= 10
                        if self.fps < 5:
                            self.fps = 5
                    elif event.key == pygame.K_0:
                        self.fps = 60
                    elif event.key == pygame.K_x:
                        paint_big_circles =  not paint_big_circles
                    elif event.key == pygame.K_y:
                        cleanup = not cleanup
                    elif event.key == pygame.K_w:
                        self.background.blit(self.background2, (0,0))

            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds

            pygame.display.set_caption("x: paint ({}), y: cleanup ({}), w: white, arrow keys and 0: change FPS:{:.2f}".format(
                           paint_big_circles, cleanup, self.clock.get_fps()))

            if cleanup:
                self.screen.blit(self.background, (0, 0))
            if paint_big_circles:
                self.wildPainting()
            myball.move(self.screenrect, seconds)
            
            myball.blit(self.screen)
            pygame.display.flip()

        pygame.quit()

class Ball(object):
    def __init__(self, radius = 50, color = (0, 0, 255), x = 320, y = 240, dx = 240, dy = 200):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.surface = pygame.Surface((2*self.radius, 2*self.radius))
        self.surface.set_colorkey((0, 0, 0))    
        pygame.draw.circle(self.surface, color, (radius, radius), radius)
        self.surface = self.surface.convert_alpha()
        self.ballrect = self.surface.get_rect()

    def blit(self, background):
        background.blit(self.surface, (self.x, self.y))

    def move(self, screenrect, seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x < 0:
            self.x = 0
            self.dx *= -1 
        elif self.x + self.ballrect.width > screenrect.width:
            self.x = screenrect.width - self.ballrect.width
            self.dx *= -1
        if self.y < 0:
            self.y = 0
            self.dy *= -1
        elif self.y + self.ballrect.height > screenrect.height:
            self.y = screenrect.height - self.ballrect.height
            self.dy *= -1

if __name__ == '__main__':

    PygView().run()