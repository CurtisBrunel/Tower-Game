

import pygame
import sys
import random


#Initilise pygame
pygame.init()

#Screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tower Game')

#Clock to control frame rate
clock = pygame.time.Clock()

#Fonts
font = pygame.font.SysFont('Arial', 30)

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#Character and Stats
class CharacterClass:
    def __init__(self, name, stats: dict):
        self.name = name
        self.stats = stats

    def display_stats(self):
        print(f"--- {self.name} Stats ---")
        for stat, value in self.stats.items():
            print(f"{stat.capitalize()}: {value}")

class MAGE(CharacterClass):
    def __init__(self):
        super().__init__("MAGE", {
            "health": None,
            "mana": None,
            "attack": None,
            "defense": None,
            "speed": None,
        })

class Warrior(CharacterClass):
    def __init__(self):
        super().__init__("Warrior", {
            "health": None,
            "mana": None,
            "attack": None,
            "defense": None,
            "speed": None,
        })

class Rogue(CharacterClass):
    def __init__(self):
        super().__init__("Rogue", {
            "health": None,
            "mana": None,
            "attack": None,
            "defense": None,
            "speed": None,
        })
#Enemies
class Enemy:
    def __init__(self, name, base_stats):
        self.name = name
        self.base_stats = base_stats.copy()
        self.stats = base_stats.copy()

    def scale_stats(self, floor):
        scale_factor = 1 + (floor / 10)
        for stat in self.stats:
            self.stats[stat] = int(self.base_stats[stat] * scale_factor)

class Goblin(Enemy):
    def __init__(self):
        super().__init__("Goblin", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class SkeletonWarrior(Enemy):
    def __init__(self):
        super().__init__("Skeleton Warrior", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class GiantRat(Enemy):
    def __init__(self):
        super().__init__("Giant Rat", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class BatSwarm(Enemy):
    def __init__(self):
        super().__init__("Bat Swarm", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Orc(Enemy):
    def __init__(self):
        super().__init__("Orc", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Spider(Enemy):
    def __init__(self):
        super().__init__("Spider", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class CursedKnight(Enemy):
    def __init__(self):
        super().__init__("Cursed Knight", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Minitor(Enemy):
    def __init__(self):
        super().__init__("Minitor", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Necromancer(Enemy):
    def __init__(self):
        super().__init__("Necromancer", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class DarkElf(Enemy):
    def __init__(self):
        super().__init__("Dark Elf", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Hydra(Enemy):
    def __init__(self):
        super().__init__("Hyrda", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class Lich(Enemy):
    def __init__(self):
        super().__init__("Lich", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class VampireLord(Enemy):
    def __init__(self):
        super().__init__("Vampire Lord", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

class DarkPalidin(Enemy):
    def __init__(self):
        super().__init__("Dark Palidin", {
            "health": 5,
            "mana": 5,
            "attack": 5,
            "defense": 5,
            "speed": 5,
        })

FLOOR_ENEMY_TIERS = {
    "low": [Goblin, SkeletonWarrior, GiantRat, BatSwarm, Orc, Spider],
    "mid": [Spider, CursedKnight, Minitor, Necromancer, DarkElf],
    "high": [Hydra, Lich, DarkPalidin, VampireLord],
}



def get_random_enemy_for_floor(floor):
    if floor % 5 == 0:
        return None

    if floor <= 19:
        enemy_class = random.choice(FLOOR_ENEMY_TIERS["low"])
    elif floor <= 39:
        enemy_class = random.choice(FLOOR_ENEMY_TIERS["mid"])
    elif floor <= 50:
        enemy_class = random.choice(FLOOR_ENEMY_TIERS["high"])
    else:
        return None

    enemy = enemy_class()
    enemy.scale_stats(floor)
    return enemy

def generate_enemies_for_floor(floor, enemy_pool):
    num_enemies = random.randint(3, 6)
    enemies = []

    for i in range(num_enemies):
        enemy_class = random.choice(enemy_pool)
        enemy = enemy_class()
        enemy.scale_stats(floor)
        enemies.append(enemy)

    return enemies


current_floor = 1
floor_intro_start_time = None
FLOOR_INTRO_DURATION  = 2000

def get_enemy_pool_for_floor(floor):
    if floor <= 19:
        return FLOOR_ENEMY_TIERS["low"]
    elif floor <= 39:
        return FLOOR_ENEMY_TIERS["mid"]
    elif floor <= 50:
        return FLOOR_ENEMY_TIERS["high"]
    else:
        return []


def start_floor(floor):
    global current_floor, floor_intro_start_time, game_state, floor_enemies, selected_enemy
    current_floor = floor
    floor_intro_start_time = pygame.time.get_ticks()
    game_state = STATE_FLOOR_INTRO
    selected_enemy = None
    enemy_pool = get_enemy_pool_for_floor(current_floor)
    floor_enemies = generate_enemies_for_floor(current_floor, enemy_pool)

def draw_floor_intro_screen():
    screen.fill(DARK_GRAY)
    floor_text = font.render(f"Floor {current_floor}", True, WHITE)
    screen.blit(floor_text, floor_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))


#Game States
STATE_TITLE = "title"
STATE_START = "start"
STATE_CHARACTER_SELECTION = "character_selection"
STATE_STATS = "stats"
STATE_GAME = "game"
STATE_FLOOR_INTRO = "floor_intro"

game_state = STATE_TITLE

#Add start button
start_game_button_rect = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 110, 200, 60)

#Variable for character selection
selected_class = None

#Character instance
mage = MAGE()
warrior = Warrior()
rogue = Rogue()





#Buttons location
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)#
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_title_screen():
    screen.fill(DARK_GRAY)
    title_text = font.render("Tower Game", True, WHITE)
    screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2,200)))

def draw_start_screen():
    screen.fill(DARK_GRAY)
    draw_title_screen()
    draw_button(start_button_rect, "Start")
    draw_button(quit_button_rect, "Quit")

#Define the boxes globally
mage_box = pygame.Rect(0, 0, 0, 0)
warrior_box = pygame.Rect(0, 0, 0, 0)
rogue_box = pygame.Rect(0, 0, 0, 0)


def draw_character_selection():
    global mage_box, warrior_box, rogue_box
    screen.fill(DARK_GRAY)

    #Draw character box
    box_width = 200
    box_height = 100
    gap = 100

    warrior_box = pygame.Rect(SCREEN_WIDTH // 2 - box_width // 2, SCREEN_HEIGHT // 2 - box_height // 2, box_width, box_height)
    mage_box = pygame.Rect(warrior_box.x - (box_width + gap), SCREEN_HEIGHT // 2 - box_height // 2, box_width, box_height)
    rogue_box = pygame.Rect(warrior_box.x + (box_width + gap), SCREEN_HEIGHT // 2 - box_height // 2, box_width, box_height)

    pygame.draw.rect(screen, BLUE, mage_box)
    pygame.draw.rect(screen, RED, warrior_box)
    pygame.draw.rect(screen, GREEN, rogue_box)

    mage_text = font.render("Mage", True, WHITE)
    warrior_text = font.render("Warrior", True, WHITE)
    rogue_text = font.render("Rogue", True, WHITE)

    screen.blit(mage_text, mage_text.get_rect(center=mage_box.center))
    screen.blit(warrior_text, warrior_text.get_rect(center=warrior_box.center))
    screen.blit(rogue_text, rogue_text.get_rect(center=rogue_box.center))

#Draw stats screen
def draw_stats_screen():
    screen.fill(DARK_GRAY)

    #Display the selected class stats
    stats_text = font.render(f"{selected_class.name} Stats", True, WHITE)
    screen.blit(stats_text, stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)))

    stats_y = SCREEN_HEIGHT // 3
    for stat, value in selected_class.stats.items():
        stat_text = font.render(f"{stat.capitalize()}: {value}", True, WHITE)
        screen.blit(stat_text, (SCREEN_WIDTH // 3, stats_y))
        stats_y += 40

    #Draw START button
    draw_button(start_game_button_rect, "Start")


def draw_game_screen():
    screen.fill(DARK_GRAY)
    game_text = font.render(f"Main game started", True, WHITE)
    screen.blit(game_text, game_text.get_rect(center =(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

#Game Loop
running = True
while running:
    for event in pygame.event.get():
        #Close window
        if event.type == pygame.QUIT:
            running = False

        #ESC key to close game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        #Transition
        if game_state == STATE_TITLE:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_state = STATE_START

        elif game_state == STATE_START:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    game_state = STATE_CHARACTER_SELECTION
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False

        elif game_state == STATE_CHARACTER_SELECTION:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mage_box.collidepoint(mouse_pos):
                    selected_class = mage
                    game_state = STATE_STATS
                elif warrior_box.collidepoint(mouse_pos):
                    selected_class = warrior
                    game_state = STATE_STATS
                elif rogue_box.collidepoint(mouse_pos):
                    selected_class = rogue
                    game_state = STATE_STATS

        elif game_state == STATE_STATS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_game_button_rect.collidepoint(mouse_pos):
                    start_floor(1)

    if game_state == STATE_FLOOR_INTRO:
        draw_floor_intro_screen()
        now = pygame.time.get_ticks()
        if now - floor_intro_start_time >= FLOOR_INTRO_DURATION:
            print("Floor intro ended, switching to STATE_GAME")
            game_state = STATE_GAME







    #Screen rendering based on state
    if game_state == STATE_TITLE:
        draw_title_screen()
    elif game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_CHARACTER_SELECTION:
        draw_character_selection()
    elif game_state == STATE_STATS:
        draw_stats_screen()
    elif game_state == STATE_GAME:
        draw_game_screen()




    #Update the screen
    pygame.display.flip()

    #Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()
