import pygame,sys,random


pygame.init()  # Initialize pygame

def draw_floor():
    screen.blit(floor, (floor_x, 450))
    screen.blit(floor, (floor_x + 2400, 450))

def dino_animation():
    new_dino = dino_frame[dino_index]
    new_dino_rect = new_dino.get_rect(center=(100, dino_rect.centery))
    return new_dino, new_dino_rect


def create_cactus():
    cactus_no=random.randint(0, 5)
    cactus=cactus_list[cactus_no]
    new_cactus=(cactus.get_rect(center=(600, 438))).inflate(-10, -10)
    return (new_cactus, cactus_no)

def move_cactus(cacti):
    for cactus in cacti:
        cactus[0].centerx-=2
    visible_cacti=[cactus for cactus in cacti if cactus[0].right>-50]
    return visible_cacti

def draw_cactus(cacti):
    for cactus in cacti:
        screen.blit(cactus_list[cactus[1]], cactus[0])

def set_random_cactus_timer():
    pygame.time.set_timer(SPAWNCACTUS, random.randint(700, 2000))

def check_collision(cacti):
    for cactus in cacti:
        if dino_rect.colliderect(cactus[0]):
            die_sound.play()
            return False
    return True

def reset_msg():
    game_font_1 = pygame.font.Font('PressStart2P-Regular.ttf', 14)  # Font
    restart_menu_surface = game_font_1.render('Press "Enter" to restart', True, (128,128,128))
    restart_menu_rect = restart_menu_surface.get_rect(center=(290, 423))
    screen.blit(restart_menu_surface, restart_menu_rect)

def score_display():
    if game_active:
        game_font = pygame.font.Font('PressStart2P-Regular.ttf', 13)  # Font
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(420, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(452, 73))
        screen.blit(high_score_surface, high_score_rect)

    else:
        game_font = pygame.font.Font('PressStart2P-Regular.ttf', 13)  # Font
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(420, 495))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(452, 518))
        screen.blit(high_score_surface, high_score_rect)


def high_score_break(score, high_score):
    if score > high_score:
        high_score = score
    return high_score



reset_m=False
RESET_MSG = pygame.USEREVENT+2
pygame.time.set_timer(RESET_MSG, 600)
RESET_MSG_1 = pygame.USEREVENT+3
pygame.time.set_timer(RESET_MSG_1, 615)





# Constants
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 800
CLOUD_COUNT = random.randint(3, 7)

#game variables
gravity=0.22
dino_movement=0
game_active=True
score=0
high_score=0
high_score_broken=False

# Function to create a new cloud off the right side of the screen
def create_cloud():
    x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
    y = random.randint(50, 180)
    return [x, y]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a screen
clock = pygame.time.Clock()  # Clock

pygame.display.flip()

#floor
floor=pygame.image.load('assets/track.png').convert_alpha()
floor_x=0

#dino
dino_1=pygame.image.load('assets/dino-run1.png').convert_alpha()
dino_1=pygame.transform.scale(dino_1,(55,55))
dino_2=pygame.image.load('assets/dino-run2.png').convert_alpha()
dino_2=pygame.transform.scale(dino_2,(55,55))
dino_frame=[dino_1, dino_2]
dino_index=0
dino=dino_frame[dino_index]
dino_rect=dino.get_rect(center=(100,432))
is_jumping=False

#cactus
cactus_1=pygame.image.load('assets/cactus1.png').convert_alpha()
cactus_1=pygame.transform.scale(cactus_1,(40,40))
cactus_2=pygame.image.load('assets/cactus2.png').convert_alpha()
cactus_2=pygame.transform.scale(cactus_2,(40,40))
cactus_3=pygame.image.load('assets/cactus3.png').convert_alpha()
cactus_3=pygame.transform.scale(cactus_3,(40,40))
cactus_4=pygame.image.load('assets/big-cactus1.png').convert_alpha()
cactus_4=pygame.transform.scale(cactus_4,(40,40))
cactus_5=pygame.image.load('assets/big-cactus2.png').convert_alpha()
cactus_5=pygame.transform.scale(cactus_5,(40,40))
cactus_6=pygame.image.load('assets/big-cactus3.png').convert_alpha()
cactus_6=pygame.transform.scale(cactus_6,(40,40))
cactus_list=[cactus_1, cactus_2, cactus_3, cactus_4, cactus_5, cactus_6]
cacti=[]

SPAWNCACTUS=pygame.USEREVENT+1
set_random_cactus_timer()


#cloud
# Load and scale the cloud image
cloud_image = pygame.image.load('assets/cloud.png').convert_alpha()
original_width, original_height = cloud_image.get_size()
desired_width = 100
scale_factor = desired_width / original_width
new_height = int(original_height * scale_factor)
cloud_image = pygame.transform.scale(cloud_image, (desired_width, new_height))

# Create initial clouds
clouds = [create_cloud() for _ in range(CLOUD_COUNT)]

# game over
game_over=pygame.image.load('assets/game-over.png').convert_alpha()
game_over=pygame.transform.scale(game_over,(360,160))
reset=pygame.image.load('assets/reset.png').convert_alpha()
reset=pygame.transform.scale(reset,(80,80))

dino_run = pygame.USEREVENT
pygame.time.set_timer(dino_run, 100)

#sound
die_sound = pygame.mixer.Sound('assets/Sound/die.wav')
jump_sound = pygame.mixer.Sound('assets/Sound/jump.wav')
score_sound = pygame.mixer.Sound('assets/Sound/point.wav')



while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # dino jump
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if dino_rect.centery>=432:
                    dino_movement=-8
                    is_jumping=True
                    jump_sound.play()

            if event.key==pygame.K_RETURN:
                if not game_active:
                    game_active=True
                    cacti.clear()
                    dino_rect.center=(100,432)
                    dino_movement=0
                    score=0
                    high_score_broken=False


        if event.type==dino_run:
            if dino_index==0:
                dino_index=1
            else:
                dino_index=0
            dino, dino_rect = dino_animation()

        if event.type==SPAWNCACTUS:
            cacti.append(create_cactus())
            set_random_cactus_timer()

        if event.type==RESET_MSG:
            reset_m=True

        if event.type==RESET_MSG_1:
            reset_m=False







    #white screen
    screen.fill((255, 255, 255))

    if game_active:
        # cactus
        cactus = move_cactus(cacti)
        draw_cactus(cacti)

        # dino jump
        if is_jumping:
            dino_movement += gravity
        dino_rect.centery += dino_movement
        if dino_rect.centery >= 432:
            dino_rect.centery = 432
            dino_movement = 0
            is_jumping = False
        screen.blit(dino, dino_rect)
        game_active = check_collision(cacti)
        score += 0.01
        if score > high_score and not high_score_broken:
            score_sound.play()
            high_score_broken = True
        high_score = high_score_break(score, high_score)
        score_display()

    else:

        screen.blit(game_over, (114, 150))
        screen.blit(reset, (248, 300))
        score_display()
        if reset_m:
            reset_msg()



    #floor
    floor_x-=1.3
    draw_floor()
    if floor_x<=-2400:
        floor_x=0


    # Update game state
    for cloud in clouds:
        cloud[0] -= 2  # Move cloud to the left
        if cloud[0] < -200:  # Reset cloud if it moves past the left edge
            clouds.remove(cloud)
            clouds.append(create_cloud())

    # Draw the scene
    for cloud in clouds:
        screen.blit(cloud_image, (cloud[0], cloud[1]))





    pygame.display.update()
    clock.tick(120)
