# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption('Winged Whimsical Run')

score = 0
coin_collected = False
score_increment = 100

pygame.font.init()

# Initialize the font for the score
font = pygame.font.Font(None, 36)


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(
            "C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\main_sprite-removebg-preview.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


def display_score(score1):
    """Display the current score on the screen."""
    score_text = font.render(f'Score: {score1}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def check_coin_collision(player1, coins1):
    """Check if the player has collected the coin and update score."""
    global score
    coin = pygame.sprite.spritecollideany(player1, coins1, pygame.sprite.collide_mask)
    if coin:
        if pygame.sprite.collide_mask(player1, coin):
            score += score_increment
            coin.kill()


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\pixil-frame-0.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 17)
        self.mask = pygame.mask.from_surface(self.surf)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super(Coins, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\coinscopy.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 50, SCREEN_WIDTH + 130),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        self.mask = pygame.mask.from_surface(self.surf)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 310)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDCOIN = pygame.USEREVENT + 3
pygame.time.set_timer(ADDCOIN, millis=900)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("C:\\Users\\gaura\\PycharmProjects\\pythonProject\\venv\\Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDCOIN:
            new_coin = Coins()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()
    coins.update()

    check_coin_collision(player, coins)

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    display_score(score)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Stop the loop
        running = False


    # def check_coin_collision():
    #     """Check if the player has collected the coin."""
    #     global coin_collected, score
    #     if pygame.sprite.spritecollideany(player, coins):
    #         coin_collected = True
    #         score += score_increment

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()