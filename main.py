import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500 #usually good practice to define concrete, constant values in all caps
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooty Blasty Ship Guys" ) #name of the game in the window's titlebar

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) #the black line in the middle of the screen
FPS = 60 #means it doesn't have a refresh rate of one billion and slow down old PCs
VEL = 5 #velocity of the spaceships when they move; 5px.
BULLET_VEL = 7 #speed of the bullets
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)

YELLOW_HIT = pygame.USEREVENT + 1 #making a custom user event. the 1 or 2 just means they're multiple custom events we're setting up and assigning
RED_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #sizing and rotating the space ship image. compare these numbers to the aspect ratio to understand the sizes.
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #stuff that happens in the lil box visually. drawing is top to bottom, it's possible to overlap stuff with other stuff.
    WIN.blit(SPACE, (0, 0)) #need this to actually put the text or images on the screen, including WHERE they go. top left is 0,0
    pygame.draw.rect(WIN, BLACK_COLOR,BORDER) #this is how you tell it to show the border we made
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE_COLOR) #the 1 is the anti-aliasing
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE_COLOR)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_COLOR, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_COLOR, bullet)
    pygame.display.update()  # i think you need to do this after everything so something actually changes. idk


#----YELLOW SHIP MOVEMENT---
def yellow_handle_movement (keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL  # if the a button is pressed, ship will move left at VELOCITY, but it will only work if the spaceship is more than 0 on the axis (which is the edge of the screen, so the player can't move any more)
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL  # note the x/y axes changing to +/-
    if keys_pressed[pygame.K_w] and yellow.y - VEL + yellow.height > BORDER.y + 50:  # UP
        yellow.y -= VEL #the 50 makes a little room for the titlebar.
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT:  # DOWN
        yellow.y += VEL #it's yellow.width because the images is ROTATED actually

# ---RED SHIP MOVEMENT---
def red_handle_movement (keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL  # if the a button is pressed, ship will move left at VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL  # note the x/y axes changing to +/-
    if keys_pressed[pygame.K_UP] and red.y - VEL + red.height > BORDER.y:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT:  # DOWN
        red.y += VEL

#---BULLET STUFF----
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets: #loop through this to check for these things:
        bullet.x += BULLET_VEL #if the bullet moved
        if red.colliderect(bullet): #if yellow's bullet hit red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) #delete the bullet after collision
        elif bullet.x > WIDTH: #if the bullet misses, delete it when it's off the screen
            yellow_bullets.remove(bullet)
    for bullet in red_bullets: #loop through this to check for these things:
        bullet.x -= BULLET_VEL #if the bullet moved
        if yellow.colliderect(bullet): #if red's bullet hit yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet) #delete the bullet after collision
        elif bullet.x < 0:
            red_bullets.remove(bullet) #if the bullet misses, delete it when it's off the screen

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE_COLOR)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main(): #the process of the game actually running!!
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run: #while the game is running, loop through all these different events to check if they're happening. If run is false, game ends.
        clock.tick(FPS)#means it doesn't have a refresh rate of one billion and slow down old PCs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(
                        yellow_bullets) < MAX_BULLETS:  # makes sure you still got bullets left
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10,
                                         5)  # where the bullet's coming from - edge of the image, directly from the middle of the ship, and 10/5 is the width/height of the rectangleitself.
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()
            if event.type ==YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()


        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS"

        if yellow_health <= 0:
            winner_text = "RED WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break




        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        print(red_bullets, yellow_bullets) #just prints it on the terminal when you press it. doesn't seem important
        keys_pressed = pygame.key.get_pressed()#checks what keys are being pressed down
        yellow_handle_movement(keys_pressed, yellow)#just running the function for how to move yellow spaceship
        red_handle_movement(keys_pressed, red)


        #red.x += 1 #this would move the piece at 60px per second (related to FPS, which is 60). just an example.
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) #tell it to show the stuff in da box

    main() #restarts the game at 'completion'. if you want the game to just quit, take this off


if __name__ == "__main__":
    main() #ensures the file is run if THIS file is run directly, not imported from elsewhere

