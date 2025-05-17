
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

show_quit_popup = False
quit_popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
yes_button_rect = pygame.Rect(quit_popup_rect.x +  40, quit_popup_rect.y + 120, 120, 40)
no_button_rect = pygame.Rect(quit_popup_rect.x +  240, quit_popup_rect.y + 120, 120, 40)

def draw_quit_popup():
    pygame.draw.rect(screen, DARK_GRAY, quit_popup_rect)
    pygame.draw.rect(screen, WHITE, quit_popup_rect, 3)

    prompt_text = font.render('Do you want to quit?', True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(quit_popup_rect.centerx, quit_popup_rect.y + 50))
    screen.blit(prompt_text, prompt_rect)

    for rect, label in [(yes_button_rect, "Yes"), (no_button_rect, "No")]:
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)
        text = font.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))


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
        super().__init__("Mage", {
            "health": 60,
            "mana": 120,
            "attack": 20,
            "defense": 5,
            "speed": 8,
        })

class Warrior(CharacterClass):
    def __init__(self):
        super().__init__("Warrior", {
            "health": 100,
            "mana": 40,
            "attack": 25,
            "defense": 5,
            "speed": 8,
        })

class Rogue(CharacterClass):
    def __init__(self):
        super().__init__("Rogue", {
            "health": 80,
            "mana": 60,
            "attack": 18,
            "defense": 8,
            "speed": 12,
        })


show_stats_popup = False

def draw_stats_popup():
    if not selected_class:
        return

    popup_width = 400
    popup_height = 300
    popup_x = SCREEN_WIDTH // 2 - popup_width // 2
    popup_y = SCREEN_HEIGHT // 2 - popup_height // 2

    #Popup background
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, GRAY, popup_rect, 0)
    pygame.draw.rect(screen, WHITE, popup_rect, 3) #Border

    #Header
    header_text = font.render(f"{selected_class.name}'s Stats", True, WHITE)
    screen.blit(header_text, header_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 30)))

    #Stats list
    stat_y = popup_y + 70
    for stat, value in selected_class.stats.items():
        stat_text = font.render(f"{stat.capitalize()}: {value}", True, WHITE)
        screen.blit(stat_text, (popup_x +30, stat_y))
        stat_y += 40

show_attack_options = False
combat_menu_state = None

#Big box for action buttons
action_menu_rect = pygame.Rect(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT - 300, 400, 200)

#Button size and spacing
button_width = 170
button_height = 60
button_spacing_x = 20
button_spacing_y = 20

#Top left corner of action menu
menu_x = action_menu_rect.x + 20
menu_y = action_menu_rect.y + 20

#Root buttons
attack_root_button_rect = pygame.Rect(action_menu_rect.x + 20, action_menu_rect.y + 30, 360, 60)
spell_root_button_rect = pygame.Rect(action_menu_rect.x + 20, action_menu_rect.y + 110, 360, 60)

#Submenu buttons
attack_sub_button_1 = pygame.Rect(menu_x, menu_y, button_width, button_height)
attack_sub_button_2 = pygame.Rect(menu_x + button_width + button_spacing_x, menu_y, button_width, button_height)
attack_sub_button_3 = pygame.Rect(menu_x, menu_y + button_height + button_spacing_y, button_width, button_height)
attack_sub_button_4 = pygame.Rect(menu_x + button_width + button_spacing_x, menu_y + button_height + button_spacing_y, button_width, button_height)

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
            "health": 40,
            "mana": 10,
            "attack": 8,
            "defense": 2,
            "speed": 10,
        })

class SkeletonWarrior(Enemy):
    def __init__(self):
        super().__init__("Skeleton Warrior", {
            "health": 50,
            "mana": 20,
            "attack": 10,
            "defense": 4,
            "speed": 6,
        })

class GiantRat(Enemy):
    def __init__(self):
        super().__init__("Giant Rat", {
            "health": 35,
            "mana": 5,
            "attack": 7,
            "defense": 2,
            "speed": 9,
        })

class BatSwarm(Enemy):
    def __init__(self):
        super().__init__("Bat Swarm", {
            "health": 30,
            "mana": 0,
            "attack": 5,
            "defense":1,
            "speed": 12,
        })

class Orc(Enemy):
    def __init__(self):
        super().__init__("Orc", {
            "health": 60,
            "mana": 10,
            "attack": 12,
            "defense": 6,
            "speed": 5,
        })

class Spider(Enemy):
    def __init__(self):
        super().__init__("Spider", {
            "health": 40,
            "mana": 10,
            "attack": 8,
            "defense": 3,
            "speed": 8,
        })

class CursedKnight(Enemy):
    def __init__(self):
        super().__init__("Cursed Knight", {
            "health": 80,
            "mana": 30,
            "attack": 18,
            "defense": 10,
            "speed": 5,
        })

class Minitor(Enemy):
    def __init__(self):
        super().__init__("Minitor", {
            "health": 90,
            "mana": 10,
            "attack": 22,
            "defense": 12,
            "speed": 4,
        })

class Necromancer(Enemy):
    def __init__(self):
        super().__init__("Necromancer", {
            "health": 70,
            "mana": 60,
            "attack": 15,
            "defense": 6,
            "speed": 7,
        })

class DarkElf(Enemy):
    def __init__(self):
        super().__init__("Dark Elf", {
            "health": 65,
            "mana": 50,
            "attack": 16,
            "defense": 5,
            "speed": 11,
        })

class Hydra(Enemy):
    def __init__(self):
        super().__init__("Hydra", {
            "health": 120,
            "mana": 40,
            "attack": 25,
            "defense": 12,
            "speed": 5,
        })

class Lich(Enemy):
    def __init__(self):
        super().__init__("Lich", {
            "health": 90,
            "mana": 100,
            "attack": 30,
            "defense": 10,
            "speed": 7,
        })

class VampireLord(Enemy):
    def __init__(self):
        super().__init__("Vampire Lord", {
            "health": 100,
            "mana": 80,
            "attack": 22,
            "defense": 10,
            "speed": 10,
        })

class Dark_Paladin(Enemy):
    def __init__(self):
        super().__init__("Dark Paladin", {
            "health": 110,
            "mana": 30,
            "attack": 28,
            "defense": 15,
            "speed": 6,
        })

FLOOR_ENEMY_TIERS = {
    "low": [Goblin, SkeletonWarrior, GiantRat, BatSwarm, Orc, Spider],
    "mid": [Spider, CursedKnight, Minitor, Necromancer, DarkElf],
    "high": [Hydra, Lich, Dark_Paladin, VampireLord],
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
    num_enemies = random.randint(2, 4)
    enemies = []

    for i in range(num_enemies):
        enemy_class = random.choice(enemy_pool)
        enemy = enemy_class()
        enemy.scale_stats(floor)
        enemies.append(enemy)

    return enemies


current_floor = 1
floor_intro_start_time = 20
FLOOR_INTRO_DURATION  = 1000

def get_enemy_pool_for_floor(floor):
    if floor <= 19:
        return FLOOR_ENEMY_TIERS["low"]
    elif floor <= 39:
        return FLOOR_ENEMY_TIERS["mid"]
    elif floor <= 50:
        return FLOOR_ENEMY_TIERS["high"]
    else:
        return []

def draw_enemies(enemies):
    enemy_box_width = 50
    enemy_box_height = 50
    spacing_y = 30
    top_margin = 100

    name_font = pygame.font.SysFont("Arial", 15)
    hp_font = pygame.font.SysFont("Arial", 10)

    left_x = SCREEN_WIDTH // 2 + 200
    right_x = SCREEN_WIDTH - 170


    for index, enemy in enumerate(enemies):

        x = left_x if index % 2 == 0 else right_x
        y = top_margin + index * (enemy_box_height + spacing_y)

        #Enemy box
        enemy_rect = pygame.Rect(x, y, enemy_box_width, enemy_box_height)
        pygame.draw.rect(screen, WHITE, enemy_rect)

        #Draw name of enemy
        name_text = font.render(enemy.name, True, WHITE)
        name_rect = name_text.get_rect(midbottom=(x + enemy_box_width // 2, y - 45))
        screen.blit(name_text, name_rect)

        #Enemy's hp
        health_text = font.render(f"HP: {enemy.stats['health']}", True, WHITE)
        health_rect = health_text.get_rect(midbottom=(x + enemy_box_width // 2, y - 15))
        screen.blit(health_text, health_rect)


def draw_main_character():
    box_width = 120
    box_height = 120
    padding = 250

    x = padding
    y = SCREEN_HEIGHT // 2 - box_height // 2

    if selected_class is not None:
        if selected_class.name == "Mage":
            colour = BLUE
        elif selected_class.name == "Warrior":
            colour = RED
        elif selected_class.name == "Rogue":
            colour = GREEN
        else:
            colour = GRAY

    else:
        colour = GRAY

    pygame.draw.rect(screen, colour, pygame.Rect(x, y, box_width, box_height))

    class_text = font.render(selected_class.name if selected_class else "", True, WHITE)
    text_rect = class_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
    screen.blit(class_text, text_rect)

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
start_game_button_rect = pygame.Rect(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 110, 200, 60)
back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 110, 200, 60)

#Combat buttons
attack_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 310, SCREEN_HEIGHT - 100, 200, 60)
stats_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 60)
item_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 110, SCREEN_HEIGHT - 100, 200, 60)


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

    if not selected_class:
        error_text = font.render("No selected class", True, WHITE)
        screen.blit(error_text, error_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        return

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
    draw_button(back_button_rect, "Back")


def draw_game_screen():
    screen.fill(DARK_GRAY)
    # game_text = font.render(f"Main game started", True, WHITE)
    # screen.blit(game_text, game_text.get_rect(center =(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    draw_enemies(floor_enemies)

    #Draw combat buttons
    draw_button(attack_button_rect, "Attack")
    draw_button(stats_button_rect, "Stats")
    draw_button(item_button_rect, "Item")

    if selected_class:
        health = selected_class.stats.get("health", 0)
        mana = selected_class.stats.get("mana", 0)

        health_text = font.render(f"HP: {health}", True, WHITE)
        mana_text = font.render(f"MANA: {mana}", True, WHITE)

        padding = 20
        screen.blit(health_text, (padding, padding))
        screen.blit(mana_text, (padding, padding + health_text.get_height() + 5))

    if combat_menu_state:
        pygame.draw.rect(screen, DARK_GRAY, action_menu_rect)
        pygame.draw.rect(screen, WHITE, action_menu_rect, 3)

        if combat_menu_state == "root":
            #2 large buttons
            for rect, label in [
                (attack_root_button_rect, "Attack"),
                (spell_root_button_rect, "Spell"),
            ]:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)
                text_surface = font.render(label, True, WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        elif combat_menu_state in ("attack", "spell"):
            #4 option buttons
            labels = ["Option 1", "Option 2", "Option 3", "Option 4"]
            rect = [attack_sub_button_1, attack_sub_button_2, attack_sub_button_3 , attack_sub_button_4]
            for rect, label in zip(rect, labels):
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)
                text_surface = font.render(label, True, WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    if show_stats_popup:
        draw_stats_popup()

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
                if show_quit_popup:
                    show_quit_popup = False
                elif show_stats_popup:
                    show_stats_popup = False
                elif combat_menu_state:
                    combat_menu_state = None
                else:
                    show_quit_popup = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if show_quit_popup:
                if yes_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif no_button_rect.collidepoint(mouse_pos):
                    show_quit_popup = False
                continue


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
                elif back_button_rect.collidepoint(mouse_pos):
                    game_state = STATE_CHARACTER_SELECTION
                    selected_class = None

        elif game_state == STATE_FLOOR_INTRO:
            draw_floor_intro_screen()
            now = pygame.time.get_ticks()
            if now - floor_intro_start_time >= FLOOR_INTRO_DURATION:
                print("Floor intro ended, switching to STATE_GAME")
                game_state = STATE_GAME
            pygame.display.flip()
            clock.tick(60)
            continue

        elif game_state == STATE_GAME:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if attack_button_rect.collidepoint(mouse_pos):
                    combat_menu_state = "root" #Open root menu

                elif combat_menu_state == "root":
                    if attack_root_button_rect.collidepoint(mouse_pos):
                        combat_menu_state = "attack"
                    elif spell_root_button_rect.collidepoint(mouse_pos):
                        combat_menu_state = "spell"

                elif combat_menu_state in ("attack", "spell"):
                    if attack_sub_button_1.collidepoint(mouse_pos):
                        print("Option 1 selected")
                        combat_menu_state = None
                    elif attack_sub_button_2.collidepoint(mouse_pos):
                        print("Option 2 selected")
                        combat_menu_state = None
                    elif attack_sub_button_3.collidepoint(mouse_pos):
                        print("Option 3 selected")
                        combat_menu_state = None
                    elif attack_sub_button_4.collidepoint(mouse_pos):
                        print("Option 4 selected")
                        combat_menu_state = None

                #Click outside closes menu
                elif combat_menu_state and not action_menu_rect.collidepoint(mouse_pos):
                    combat_menu_state = None


                elif attack_button_rect.collidepoint(mouse_pos):
                    show_attack_options = not show_attack_options
                elif show_attack_options and attack_root_button_rect.collidepoint(mouse_pos):
                    print("Basic attack selected")
                    show_attack_options = False #Hides options after selecting
                elif show_attack_options and spell_root_button_rect.collidepoint(mouse_pos):
                    print("Spell option selected")
                    show_attack_options = False
                elif not attack_button_rect.collidepoint(mouse_pos):
                    show_attack_options = False #Click outside hides menu

                elif stats_button_rect.collidepoint(mouse_pos):
                    show_stats_popup = not show_stats_popup
                elif item_button_rect.collidepoint(mouse_pos):
                    print("Item selected")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and show_stats_popup:
                    show_stats_popup = False




    if game_state == STATE_FLOOR_INTRO:
        draw_floor_intro_screen()
        now = pygame.time.get_ticks()
        if now - floor_intro_start_time >= FLOOR_INTRO_DURATION:
            game_state = STATE_GAME
        pygame.display.flip()
        clock.tick(60)
        continue


    #Screen rendering based on state
    elif game_state == STATE_TITLE:
        draw_title_screen()
    elif game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_CHARACTER_SELECTION:
        draw_character_selection()
    elif game_state == STATE_STATS:
        draw_stats_screen()
    elif game_state == STATE_GAME:
        draw_game_screen()
        draw_main_character()


    if show_quit_popup:
        draw_quit_popup()




    #Update the screen
    pygame.display.flip()

    #Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()
