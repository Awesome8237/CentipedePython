import pygame
import random

def checkPlayerMushroomCollision(x,y, mushrooms, direction):

    for mushroom in mushrooms:
        if mushroom['exists'] and mushroom['x'] < x + 32 and mushroom['x'] + 32 > x and mushroom['y'] + 32 > y and mushroom['y'] < y + 32:
            if direction == 'up' and y > mushroom['y']:
                return True
            elif direction == 'down' and y < mushroom['y']:
                return True
            elif direction == 'right' and x < mushroom['x']:
                return True
            elif direction == 'left' and x > mushroom['x']:
                return True

def checkBulletMushroomCollision(bullets,mushrooms):

    for bullet in bullets:
        for mushroom in mushrooms:
            if mushroom['exists']:
                if bullet['x'] < mushroom['x'] + 32 and bullet['x'] + 20 > mushroom['x'] and bullet['y'] < mushroom['y'] + 32 and mushroom['y'] < bullet['y'] + 32:
                    mushroom['exists'] = False
                    bullets.remove(bullet)

def checkCentipedeCollsion(centipede,mushrooms):

    for segment in centipede:
        if segment['x'] < 0 or segment['x']+32 > 960:
            if centipede[centipede.index(segment) - 1]['exists'] and abs(centipede[centipede.index(segment) - 1]['x'] - segment['x']) >= 32:
                segment['movingDown'] = True

                segment['movingLeft'] = not segment['movingLeft']
        else:
            for mushroom in mushrooms:
                if mushroom['exists'] and segment['x'] < mushroom['x'] + 32 and segment['x'] + 32 > mushroom['x'] and segment['y'] + 32 > mushroom['y'] and segment['y'] < mushroom['y'] + 32:
                    segment['movingDown'] = True
                    segment['movingLeft'] = not segment['movingLeft']


pygame.init()

screen = pygame.display.set_mode((960,960),pygame.SCALED | pygame.FULLSCREEN)

#screen = pygame.display.set_mode((960,960),RESIZABLE)

clock = pygame.time.Clock()

player_x = 960/2
player_y = 960/2

bullets = []

mushrooms = []

centipede = []

head = {'exists': True, 'x': 10*32, 'y': 0, 'head': True, 'movingLeft': True, 'movingDown': False}

centipede.append(head)

for i in range(11):
    segment = {'exists': True, 'x': (10+i+1)*32, 'y': 0, 'head': False, 'movingLeft': True, 'movingDown': False}
    centipede.append(segment)



for row in range(30):
    for column in range(30):
        mushroom = {'exists': False, 'x': column*32, 'y': row*32}
        mushrooms.append(mushroom)

# mushroom_num = random.randint(20,30)
#
# placed = False
#
# for item in range(mushroom_num):
#     placed = False
#     while not placed:
#         position = random.randint(0, len(mushrooms))
#         if not mushrooms[position]['exists'] and position > 30:
#             mushrooms[position]['exists'] = True
#             placed = True




bg_surface = pygame.image.load('Textures/background.png')

player_surface = pygame.image.load('Textures/player.png')

bullet_surface = pygame.image.load('Textures/bullet.png')

mushrooms_sprite_sheet = pygame.image.load('Textures/mushroom.png')

mushroom_surface = pygame.Surface((32,32)).convert_alpha()

mushroom_surface.blit(mushrooms_sprite_sheet,(0,0),(0,0,32,32))

mushroom_surface.set_colorkey((0,0,0))

head_image = pygame.image.load('Textures/c_head_left_walk.png')

head_surface = pygame.Surface((32,32)).convert_alpha()

head_surface.blit(head_image,(0,0), (0,0,32,32))

head_surface.set_colorkey((0,0,0))

body_image = pygame.image.load('Textures/c_body_left_walk.png')

body_surface = pygame.Surface((32,32)).convert_alpha()

body_surface.blit(body_image,(0,0), (0,0,32,32))

body_surface.set_colorkey((0,0,0))

player_speed = 5

#----------------------------------GAME LOOP---------------------------------#

while True:

    bullet = {"x": player_x, "y": player_y}


#----------------------------EVENT HANDLER---------------------------------#

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0 and not checkPlayerMushroomCollision(player_x,player_y,mushrooms,"left"):
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + 32 < 960 and not checkPlayerMushroomCollision(player_x,player_y,mushrooms,"right"):
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0 and not checkPlayerMushroomCollision(player_x,player_y,mushrooms,"up"):
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + 32 < 960 and not checkPlayerMushroomCollision(player_x,player_y,mushrooms,"down"):
        player_y += player_speed

#----------------------Bullet movement-------------------------#
    for bullet in bullets:
        if bullet["y"] < 0:
            bullets.remove(bullet)
        else:
            bullet["y"] -= 10

    checkBulletMushroomCollision(bullets, mushrooms)
    checkCentipedeCollsion(centipede, mushrooms)

    for segment in centipede:
        if segment["exists"]:
            if segment["movingDown"]:
                segment['y'] += 32



                segment["movingDown"] = False
            elif segment["movingLeft"]:
                segment['x'] -= 3
            else:
                segment['x'] += 3


#------------------------------- DRAWING --------------------------------#

    screen.blit(bg_surface,(0,0))

    for mushroom in mushrooms:
        if mushroom['exists']:
            screen.blit(mushroom_surface, (mushroom["x"], mushroom["y"]))

    for segment in centipede:
        if segment['head'] and segment['exists']:
            if segment['movingLeft']:
                screen.blit(head_surface, (segment["x"], segment["y"]))
            else:
                flipped_head = pygame.transform.flip(head_surface,True, False)
                flipped_head.set_colorkey((0,0,0))
                screen.blit(flipped_head,(segment["x"], segment["y"]))
        elif not segment['head']:
            if segment['movingLeft']:
                screen.blit(body_surface, (segment["x"], segment["y"]))
            else:
                flipped_body = pygame.transform.flip(body_surface,True, False)
                flipped_body.set_colorkey((0,0,0))
                screen.blit(flipped_body,(segment["x"], segment["y"]))


    for bullet in bullets:
        screen.blit(bullet_surface,(bullet["x"],bullet["y"]))

    screen.blit(player_surface, (player_x, player_y))

    pygame.display.update()
    clock.tick(60)




