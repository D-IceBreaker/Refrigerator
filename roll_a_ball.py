import pygame
import random

pygame.init()

screen = pygame.display.set_mode((640, 480))
screenrect = screen.get_rect()

background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))

background = background.convert()

screen.blit(background, (0, 0))

ballsurface = pygame.Surface((50, 50))
ballsurface.set_colorkey((0, 0, 0))
pygame.draw.circle(ballsurface, (255, 0, 0), (25 , 25), 25)
ballsurface = ballsurface.convert_alpha()
ballrect = ballsurface.get_rect()

ballx, bally = 320, 240
dx = 0
dy = 0
speed = 200 #That's for time-based movement

screen.blit(ballsurface, (ballx, bally))

mainloop = True
FPS = 60
playtime = 0.0
clock = pygame.time.Clock()

while mainloop:
    milliseconds = clock.tick(FPS) 
    seconds = milliseconds / 1000.0
    playtime += seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_LEFT: #This is for the second part of the Task 1
                ballx -= 20
            elif event.key == pygame.K_RIGHT: #It moves the ball by 20 pixels in the direction of pressed key
                ballx += 20
            elif event.key == pygame.K_UP: #You can call it "short-range teleport"
                bally -= 20
            elif event.key == pygame.K_DOWN:
                bally += 20

    screen.blit(background, (0, 0))

    pressedkeys = pygame.key.get_pressed() #And this is for normal time-based movement
    dx, dy  = 0, 0
    if pressedkeys[pygame.K_a]:
        dx -= speed
    if pressedkeys[pygame.K_d]:
        dx += speed
    if pressedkeys[pygame.K_w]:
        dy -= speed
    if pressedkeys[pygame.K_s]:
        dy += speed
    ballx += dx * seconds 
    bally += dy * seconds

    if ballx < 0: #Now it won't leave the screen
        ballx = 0
    elif ballx + ballrect.width > screenrect.width:
        ballx = screenrect.width - ballrect.width
    if bally < 0:
        bally = 0
    elif bally + ballrect.height > screenrect.height:
        bally = screenrect.height - ballrect.height
    screen.blit(ballsurface, (round(ballx, 0), round(bally, 0)))

    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    pygame.display.flip()

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))