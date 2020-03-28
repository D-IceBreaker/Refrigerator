import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
background = background.convert()
clock = pygame.time.Clock()

ballsurface = pygame.Surface((50,50))
pygame.draw.circle(ballsurface, (0,0,255), (25,25),25)
ballsurface = ballsurface.convert()

pygame.draw.circle(background, (255,192,203), (320,240), 200)
pygame.draw.polygon(background, (0,180,0), ((300, 85),(265,110),(280,70),(250,50),(285,50),(300,5),(315,50),(350,50),(320,70),(335,110)))
pygame.draw.arc(background, (255,150,0),(0,0,1400,1024), 0, 3.14)
for point in range(0,641,64): # range(start, stop, step)
   pygame.draw.line(background, (128,255-25*(point/64),25*(point/64)), (0,0), (480, point), 1)
   pygame.draw.line(background, (255-25*(point/64),25*(point/64), 128), (640,0), (160, point), 1)
   pygame.draw.line(background, (255-25*(point/64),128,25*(point/64)), (0,480), (480, 480-point), 1)
   pygame.draw.line(background, (255-25*(point/64),255-25*(point/64),25*(point/64)), (640,480), (160, 480-point), 1)

mainloop = True
FPS = 30
playtime = 0.0

screen.blit(background, (0, 0))
screen.blit(ballsurface, (320, 240)) #this line should be outcommented if you want to remove both the blue ball and black square
while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    pygame.display.flip()

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))