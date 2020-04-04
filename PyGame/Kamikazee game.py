# Kamikazee! created Brandon Herbst
import pygame
import random
import os
import self as self
from pygame import mixer
from os import path
# setup of our game constants*

WIDTH = 800
HEIGHT = 600
FPS = 60

# define RGB (colours in pygame)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OLIVE = (128, 128, 0)

# setup assets folders!!
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, "images")
sounds_folder = os.path.join(game_folder, "sounds")
font_name = pygame.font.match_font('AtariClassicChunky')

# initializing pygame and creating a window
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kamikazee!')
pygame.display.set_icon(pygame.image.load("ICON.png"))

clock = pygame.time.Clock()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_enemies():
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

def draw_shield(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_width = 100
    bar_height = 30
    fill = (pct / 100) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, OLIVE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 3)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player (pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.6 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius )
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.x_speed = 0
        # create a player shield & lives!
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # check to see when its time to unhide the player!
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.x_speed = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = -5
        if keystate[pygame.K_RIGHT]:
            self.x_speed = 5

        self.rect.x += self.x_speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        missile = Missile(self.rect.centerx, self.rect.top)
        all_sprites.add(missile)
        missiles.add(missile)
        missile_sound.play()

    def hide(self):
        # temporarily hide the player between lives!
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.4 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, 100)
        self.speed_y = random.randrange(1, 10)
        self.speed_x = random.randrange(-1, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speed_y = random.randrange(4, 8)

class Missile (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # kill the bullet off the screen;
        if self.rect.bottom < 0:
            self.kill()

class Explosion (pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#create a game start screen!
def show_start_screen():
    window.blit(background, background_rect)
    draw_text(window, "KAMIKAZEE!", 72, WIDTH / 2, 50)
    draw_text(window, "Press Arrows to move!", 25, WIDTH / 2, 450)
    draw_text(window, "Press Spacebar to fire!", 25, WIDTH / 2, 500)
    draw_text(window, "Press any key to start!", 25, WIDTH / 2, 550)
    window.blit(start_screen_image, (WIDTH / 3, 180))
    pygame.display.flip()
    wait_for_key()
#create a game over screen
def game_over_screen():
    window.blit(background, background_rect)
    draw_text(window, "KAMIKAZEE!", 72, WIDTH / 2, 50)
    draw_text(window, "GAME OVER!" , 50, WIDTH / 2, 300)
    draw_text(window, "Press any key to play again!", 25, WIDTH / 2, 500)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# load all the games graphics & images
background = pygame.image.load (os.path.join (image_folder, "background.png"))
background_rect = background.get_rect()
player_image = pygame.image.load(os.path.join(image_folder, "P1.png"))
player_lives_img = pygame.transform.scale(player_image, (36, 36))
player_lives_img.set_colorkey(BLACK)
start_screen_image = pygame.image.load(os.path.join(image_folder, "start_image.png"))
missile_image = pygame.image.load(os.path.join(image_folder, "missile.png")).convert()
enemy_missile = pygame.image.load(os.path.join(image_folder, "enemy_missile.png")).convert()
enemy_images = []
enemy_list = ['E1.png', 'E2.png', 'E3.png']
for images in enemy_list:
    enemy_images.append(pygame.image.load(os.path.join(image_folder, images)))

# create an explosion!
explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
for i in range(10):
    filename = 'EX{}.png'.format(i)
    images = pygame.image.load(os.path.join(image_folder, filename))
    images.set_colorkey(BLACK)
    img_large = pygame.transform.scale(images, (72, 72))
    explosion_animation['lg'].append(img_large)
    img_small = pygame.transform.scale(images, (50, 50))
    explosion_animation['sm'].append(img_small)

# load all the game sounds:
missile_sound = pygame.mixer.Sound(os.path.join(sounds_folder, 'Missile.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join(sounds_folder, 'explosion.wav'))
# load background music!
pygame.mixer.music.load(os.path.join(sounds_folder, 'background-3.wav'))
# adjust the volume of the music
pygame.mixer.music.set_volume(0.6)

# play the background music
pygame.mixer.music.play(loops=-1)

# Game loop!
start_game = True
game_over = True
run = True
while run:
    if start_game:
        show_start_screen()
        start_game = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        missiles = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(12):
            new_enemies()

        score = 0

    else:
        if player.lives == 0 and not exp.alive():
            game_over = True
            game_over_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            missiles = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(12):
                new_enemies()

            score = 0

    # keep the game running at the correct frames per second
    # We will do this at 60 FPS

    clock.tick(FPS)

    # process input(events)

    for event in pygame.event.get():
        # close the window enabled
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #
    all_sprites.update()
    # check to see a collision between the missiles and the enemy
    impact = pygame.sprite.groupcollide(enemies, missiles, True, True)
    for hit in impact:
        score += 10
        explosion_sound.play()
        exp = Explosion(hit.rect.center, 'lg')
        all_sprites.add(exp)
        new_enemies()

    # check to see any hits from the Kamikazee pilots (use the circle around the sprite!)
    impact = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in impact:
        player.shield -= hit.radius * 3
        explosion_sound.play()
        exp = Explosion(hit.rect.center, 'sm')
        all_sprites.add(exp)
        new_enemies()
        if player.shield < 0:
            exp = Explosion(hit.rect.center, 'lg')
            all_sprites.add(exp)
            player.hide()
            player.lives -= 1
            player.shield = 100

        clock.tick (FPS)

        # process input(events)

        for event in pygame.event.get():
            # close the window enabled
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        #
        all_sprites.update()
        # check to see a collision between the missiles and the enemy
        impact = pygame.sprite.groupcollide(enemies, missiles, True, True)
        for hit in impact:
            score += 10
            explosion_sound.play()
            exp = Explosion(hit.rect.center, 'lg')
            all_sprites.add(exp)
            new_enemies()

        # check to see any hits from the Kamikazee pilots (use the circle around the sprite!)
        impact = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        for hit in impact:
            player.shield -= hit.radius * 1.2
            explosion_sound.play()
            exp = Explosion(hit.rect.center, 'sm')
            all_sprites.add(exp)
            new_enemies()
            if player.shield < 0:
                exp = Explosion(hit.rect.center, 'lg')
                all_sprites.add(exp)
                player.hide()
                player.lives -= 1
                player.shield = 100

    # draw / render on the game window!

    window.fill(BLACK)
    window.blit(background, background_rect)
    all_sprites.draw(window)
    draw_text(window, ("SCORE: " + str(score)), 20, 130, 10)
    draw_shield(window, 650, 8, player.shield)
    draw_lives(window, WIDTH - 450, 10, player.lives, player_lives_img)

    # always do this last, flip the display after draw!!
    pygame.display.flip()

pygame.quit()
quit()