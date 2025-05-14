

import pygame
import sys


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


#Game States
STATE_TITLE = "title"
STATE_START = "start"
STATE_CHARACTER_SELECTION = "character_selection"
STATE_STATS = "stats"
STATE_GAME = "game"

game_state = STATE_TITLE

#Add start button
start_game_button_rect = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 110, 200, 60)

#Variable for character selection
selected_class = None

#Character instance
mage = MAGE()
warrior = Warrior()
rogue = Rogue()


#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


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
                    game_state = STATE_GAME

        elif game_state == STATE_GAME:
            draw_game_screen()




    #Screen rendering based on state
    if game_state == STATE_TITLE:
        draw_title_screen()
    elif game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_CHARACTER_SELECTION:
        draw_character_selection()
    elif game_state == STATE_STATS:
        draw_stats_screen()




    #Update the screen
    pygame.display.flip()

    #Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()
