
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
pygame.display.set_caption('Warden of the Tower')

#Clock to control frame rate
clock = pygame.time.Clock()

#Fonts
font = pygame.font.SysFont('Arial', 30)
small_font = pygame.font.SysFont('Arial', 20)

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

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
        stats = {
            "health": 60,
            "mana": 120,
            "attack": 20,
            "defence": 5,
            "speed": 8,
        }
        super().__init__("Mage", stats)
        self.base_stats = stats.copy()

class Warrior(CharacterClass):
    def __init__(self):
        stats = {
            "health": 100,
            "mana": 40,
            "attack": 25,
            "defence": 5,
            "speed": 8,
        }
        super().__init__("Warrior", stats)
        self.base_stats = stats.copy()

class Rogue(CharacterClass):
    def __init__(self):
        stats = {
            "health": 80,
            "mana": 60,
            "attack": 18,
            "defence": 8,
            "speed": 12,
        }
        super().__init__("Rogue", stats)
        self.base_stats = stats.copy()

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
            "defence": 2,
            "speed": 10,
        })

class SkeletonWarrior(Enemy):
    def __init__(self):
        super().__init__("Skeleton Warrior", {
            "health": 50,
            "mana": 20,
            "attack": 10,
            "defence": 4,
            "speed": 6,
        })

class GiantRat(Enemy):
    def __init__(self):
        super().__init__("Giant Rat", {
            "health": 35,
            "mana": 5,
            "attack": 7,
            "defence": 2,
            "speed": 9,
        })

class BatSwarm(Enemy):
    def __init__(self):
        super().__init__("Bat Swarm", {
            "health": 30,
            "mana": 0,
            "attack": 5,
            "defence":1,
            "speed": 12,
        })

class Orc(Enemy):
    def __init__(self):
        super().__init__("Orc", {
            "health": 60,
            "mana": 10,
            "attack": 12,
            "defence": 6,
            "speed": 5,
        })

class Spider(Enemy):
    def __init__(self):
        super().__init__("Spider", {
            "health": 40,
            "mana": 10,
            "attack": 8,
            "defence": 3,
            "speed": 8,
        })

class CursedKnight(Enemy):
    def __init__(self):
        super().__init__("Cursed Knight", {
            "health": 80,
            "mana": 30,
            "attack": 18,
            "defence": 10,
            "speed": 5,
        })

class Minitor(Enemy):
    def __init__(self):
        super().__init__("Minitor", {
            "health": 90,
            "mana": 10,
            "attack": 22,
            "defence": 12,
            "speed": 4,
        })

class Necromancer(Enemy):
    def __init__(self):
        super().__init__("Necromancer", {
            "health": 70,
            "mana": 60,
            "attack": 15,
            "defence": 6,
            "speed": 7,
        })

class DarkElf(Enemy):
    def __init__(self):
        super().__init__("Dark Elf", {
            "health": 65,
            "mana": 50,
            "attack": 16,
            "defence": 5,
            "speed": 11,
        })

class Hydra(Enemy):
    def __init__(self):
        super().__init__("Hydra", {
            "health": 120,
            "mana": 40,
            "attack": 25,
            "defence": 12,
            "speed": 5,
        })

class Lich(Enemy):
    def __init__(self):
        super().__init__("Lich", {
            "health": 90,
            "mana": 100,
            "attack": 30,
            "defence": 10,
            "speed": 7,
        })

class VampireLord(Enemy):
    def __init__(self):
        super().__init__("Vampire Lord", {
            "health": 100,
            "mana": 80,
            "attack": 22,
            "defence": 10,
            "speed": 10,
        })

class Dark_Paladin(Enemy):
    def __init__(self):
        super().__init__("Dark Paladin", {
            "health": 110,
            "mana": 30,
            "attack": 28,
            "defence": 15,
            "speed": 6,
        })

#Bosses
class GoblinKing(Enemy):
    def __init__(self):
        super().__init__("Goblin King", {
            "health": 80,
            "mana": 50,
            "attack": 30,
            "defence": 10,
            "speed": 7,
        })

class ElementalLord(Enemy):
    def __init__(self):
        super().__init__("Elemental Lord", {
            "health": 180,
            "mana": 100,
            "attack": 35,
            "defence": 12,
            "speed": 8,
        })

class Dragon(Enemy):
    def __init__(self):
        super().__init__("Dragon", {
            "health": 220,
            "mana": 80,
            "attack": 40,
            "defence": 15,
            "speed": 6,
        })

class FallenRoyalGuard(Enemy):
    def __init__(self):
        super().__init__("Fallen Royal Guard", {
            "health": 250,
            "mana": 70,
            "attack": 45,
            "defence": 18,
            "speed": 5,
        })

class FallenArchangel(Enemy):
    def __init__(self):
        super().__init__("Fallen Archangel", {
            "health": 300,
            "mana": 120,
            "attack": 50,
            "defence": 20,
            "speed": 10,
        })

FLOOR_ENEMY_TIERS = {
    "low": [Goblin, SkeletonWarrior, GiantRat, BatSwarm, Orc, Spider],
    "mid": [Spider, CursedKnight, Minitor, Necromancer, DarkElf],
    "high": [Hydra, Lich, Dark_Paladin, VampireLord],
}


def get_random_enemy_for_floor(floor):
    if floor % 10 == 0:
        boss_fight = {
            10: GoblinKing,
            20: ElementalLord,
            30: Dragon,
            40: FallenRoyalGuard,
            50: FallenArchangel,
        }
        boss_class = boss_fight.get(floor)
        if boss_class:
            boss = boss_class()
            boss.scale_stats(floor)
            return boss
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

def draw_enemies(floor_enemies):
    global enemy_hitboxes
    enemy_hitboxes = []


    enemy_box_width = 50
    enemy_box_height = 50
    spacing_y = 30
    top_margin = 270

    name_font = pygame.font.SysFont("Arial", 15)
    hp_font = pygame.font.SysFont("Arial", 12)

    left_x = SCREEN_WIDTH // 2 + 200
    right_x = SCREEN_WIDTH - 170


    for index, enemy in enumerate(floor_enemies):

        x = left_x if index % 2 == 0 else right_x
        y = top_margin + index * (enemy_box_height + spacing_y)

        #Enemy box
        enemy_rect = pygame.Rect(x, y, enemy_box_width, enemy_box_height)
        enemy_hitboxes.append((enemy, enemy_rect))

        #Draw enemy box
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
    global current_floor, floor_intro_start_time, game_state, floor_enemies, selected_enemy, break_room_action_taken, player_ap, player_turn

    current_floor = floor
    floor_intro_start_time = pygame.time.get_ticks()
    selected_enemy = None
    break_room_action_taken = False

    #Reset player's mana to full
    if selected_class:
        selected_class.stats["mana"] = selected_class.base_stats["mana"]

    #Reset AP
    player_ap = 3
    player_turn = True

    # Boss floor
    if floor % 10 == 0:
        boss = get_random_enemy_for_floor(floor)
        floor_enemies = [boss]
    else:
        enemy_pool = get_enemy_pool_for_floor(current_floor)
        floor_enemies = generate_enemies_for_floor(current_floor, enemy_pool)

    game_state = STATE_FLOOR_INTRO

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
STATE_GAME_OVER = "game_over"
STATE_UPGRADE = "upgrade"
STATE_BREAK_ROOM = "break_room"




game_state = STATE_TITLE

#Buttons
start_game_button_rect = pygame.Rect(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 110, 200, 60)
back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 110, 200, 60)
quit_to_menu_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 110, 200, 60)

#Combat buttons
attack_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 310, SCREEN_HEIGHT - 100, 200, 60)
stats_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 60)
item_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 110, SCREEN_HEIGHT - 100, 200, 60)

#Upgrade Screen Button
continue_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 520, 200, 60)
break_room_action_taken = False

show_next_floor_button = False
next_floor_triggered = False
# next_floor_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 60)

#Variable for character selection
selected_class = None

#Character instance
mage = MAGE()
warrior = Warrior()
rogue = Rogue()

player_inventory = []
show_inventory_popup = False
selected_inventory_index = None
use_item_button_rect = None

player_abilities = []


ITEM_POOL = [
    {"name": "Health Potion", "type": "healing", "effect": 50},
    {"name": "Mega Healing Potion", "type": "healing", "effect": 100},
    {"name": "Mana Potion", "type": "mana", "effect": 50},
    {"name": "Mega Mana Potion", "type": "mana", "effect": 100},
    {"name": "Longsword", "type": "Damage", "effect": 40},

]

ITEM_DATABASE = {
    "Health Potion": {
        "type": "healing",
        "description": "Restores 50 HP",
        "effect":  lambda player: setattr(player.stats, "health", min(player.stats["health"] + 50, 100))
    },
    "Mega Health Potion": {
        "type": "healing",
        "description": "Restores 100 HP",
        "effect":  lambda player: setattr(player.stats, "health", min(player.stats["health"] + 100, 100))
    },
    "Mana Potion": {
        "type": "mana",
        "description": "Increase mana by 50",
        "effect": lambda player: setattr(player.stats, "mana", min(player.stats["mana"] + 50, 100))
    },
}

def draw_inventory_popup():
    global use_item_button_rect

    popup_width = 400
    popup_height = 300
    popup_x = SCREEN_WIDTH // 2 - popup_width // 2
    popup_y = SCREEN_HEIGHT // 2 - popup_height // 2


    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, DARK_GRAY, popup_rect)
    pygame.draw.rect(screen, WHITE, popup_rect, 3)

    title = font.render(f"Inventory", True, WHITE)
    screen.blit(title, title.get_rect(center=(popup_rect.centerx, popup_rect.y + 30)))

    for i, item in enumerate(player_inventory):
        label = f"{item['name']} ({item['type']})"
        item_text = small_font.render(label, True, WHITE)
        item_rect = pygame.Rect(popup_x + 30, popup_y + 70 + i * 40, 300, 30)

        pygame.draw.rect(screen, GRAY, item_rect)
        pygame.draw.rect(screen, YELLOW if selected_inventory_index == i else WHITE, item_rect, 2)
        screen.blit(item_text, item_text.get_rect(center=item_rect.center))

        item["rect"] = item_rect

    if selected_inventory_index is not None:
        use_button = pygame.Rect(popup_x + 100, popup_y + popup_height - 50, 200, 30)
        pygame.draw.rect(screen, GRAY, use_button)
        pygame.draw.rect(screen, WHITE, use_button, 2)
        use_text = font.render("Use Item", True, WHITE)
        screen.blit(use_text, use_text.get_rect(center=use_button.center))
        use_item_button_rect = use_button
    else:
        use_item_button_rect = None



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

def draw_game_over_screen():
    screen.fill(DARK_GRAY)

    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

    draw_button(quit_to_menu_button_rect, "Quit to Menu")


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
        ap_text = font.render(f"AP: {player_ap}", True, WHITE)

        padding = 20
        spacing = 5

        screen.blit(health_text, (padding, padding))

        mana_y = padding + health_text.get_height() + spacing
        screen.blit(mana_text, (padding, mana_y))

        ap_y = mana_y + mana_text.get_height() + spacing
        screen.blit(ap_text, (padding, ap_y))

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

        elif combat_menu_state in "attack":
            for i, attack in enumerate(player_attacks[:4]):
                rect = pygame.Rect(menu_x + (i % 2) * (button_width + button_spacing_x),
                                   menu_y + (i // 2) * (button_height + button_spacing_y),
                                   button_width, button_height)
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)

                # Display ability name
                text_surface = font.render(attack["name"], True, WHITE)
                screen.blit(text_surface, text_surface.get_rect(center=rect.center))

                # Store rect for click detection
                attack["rect"] = rect




        elif combat_menu_state == "spell":
            for i, spell in enumerate(player_spells[:4]):
                rect = pygame.Rect(menu_x + (i % 2) * (button_width + button_spacing_x),
                                   menu_y + (i // 2) * (button_height + button_spacing_y),
                                   button_width, button_height)
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)


                if isinstance(spell, str):
                    player_spells[i] = {"name": spell, "rect": rect}
                else:
                    spell["rect"] = rect

                text_surface = font.render(player_spells[i]["name"], True, WHITE)
                screen.blit(text_surface, text_surface.get_rect(center=rect.center))




    if show_stats_popup:
        draw_stats_popup()


#Comabt system
player_turn = True
player_ap = 3
targeting_mode = False
pending_attack_option = None
floor_enemies = []
selected_enemy = None
combat_log = []
enemy_hitboxes = []

def draw_combat_log():
    log_font = pygame.font.SysFont("Arial", 20)
    max_lines = 6
    line_spacing = 25

    log_width = 500
    log_height = max_lines * line_spacing + 20

    log_x = SCREEN_WIDTH - log_width - 20
    log_y = 20

    #Background panel
    log_bg_rect = pygame.Rect(log_x - 10, log_y - 10, log_width, log_height)
    pygame.draw.rect(screen, DARK_GRAY, log_bg_rect)
    pygame.draw.rect(screen, WHITE, log_bg_rect, 2)

    recent_logs = combat_log[-max_lines:]
    for i, line in enumerate(recent_logs):
        log_text = log_font.render(line, True, WHITE)
        screen.blit(log_text, (log_x, log_y + i * line_spacing))



#Upgrade system
upgrade_options = []
show_upgrade_popup = False
selected_upgrade_index = None

just_confirmed_upgrade = False

upgrade_popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 250, 700, 500)

confirm_upgrade_button_rect = None
upgrade_button_rects = []


UPGRADE_TYPE_STATS = "stat"
UPGRADE_TYPE_ITEM = "item"
UPGRADE_TYPE_ABILITY = "ability"

CLASS_ABILITIES = {
    "Mage": {
        "attacks": [
            {"name": "Magic Bolt", "damage": 15},
            {"name": "Arcane Strike", "damage": 20},
            {"name": "Flame Burst", "damage": 25},
            {"name": "Ice Lance", "damage": 30}
        ],
        "spells": [
            {"name": "Mana Shield", "defence": 10, "mana_cost": 20},
            {"name": "Fireball", "damage": 35, "mana_cost": 10},
            {"name": "Heal", "damage": -30, "mana_cost": 20},
            {"name": "Earthquake", "damage": 40, "mana_cost": 20}
        ]
    },
    "Warrior": {
        "attacks": [
            {"name": "Slash", "damage": 20},
            {"name": "Heavy Blow", "damage": 30},
            {"name": "Whirlwind", "damage": 25},
            {"name": "Shield Bash", "damage": 15}
        ],
        "spells": [
            {"name": "Battle Cry", "damage": 40, "mana_cost": 20},
            {"name": "Stone Skin", "defence": 10, "mana_cost": 20},
            {"name": "Charge", "damage": 35, "mana_cost": 20},
            {"name": "Earthquake", "damage": 40, "mana_cost": 20}
        ]
    },
    "Rogue": {
        "attacks": [
            {"name": "Quick Stab", "damage": 15},
            {"name": "Poison Dagger", "damage": 20},
            {"name": "Backstab", "damage": 30},
            {"name": "Shadow Strike", "damage": 25}
        ],
        "spells": [
            {"name": "Smoke Bomb", "damage": 15, "mana_cost": 20},
            {"name": "Agility Boost", "damage": 5, "mana_cost": 20},
            {"name": "Invisibility", "defence": 10, "mana_cost": 20},
            {"name": "Shadow Clone", "damage": 20, "mana_cost": 20}
        ]
    }
}

player_attacks = []
player_spells = []

def initialise_abilities(class_name):
    global player_attacks, player_spells
    player_attacks = [CLASS_ABILITIES[selected_class.name]["attacks"][0]]
    player_spells = [CLASS_ABILITIES[selected_class.name]["spells"][0]]


def get_locked_abilities():
    if not selected_class:
        return []

    class_name = selected_class.name
    if class_name not in CLASS_ABILITIES:
        return []

    class_abilities = CLASS_ABILITIES[class_name]
    known_ability_names = set(a["name"] for a in player_attacks + player_spells)

    # Return only abilities the player hasn't learned yet
    all_abilities = class_abilities["attacks"] + class_abilities["spells"]
    locked_abilities = [a for a in all_abilities if a["name"] not in known_ability_names]
    return locked_abilities


def generate_stat_upgrades():
    global upgrade_options, selected_upgrade_index

    upgrade_options = []
    selected_upgrade_index = None

    all_stats = ["health", "mana", "attack", "defence", "speed"]
    all_items = ITEM_POOL

    for i in range (4):
        upgrade_type = random.choice(["stat", "item", "ability"])

        if upgrade_type == "stat":
            stat = random.choice(all_stats)
            upgrade_options.append({
                "type": "stat",
                "label": f"+10 {stat.capitalize()}",
                "value": stat
            })

        elif upgrade_type == "item":
            item = random.choice(all_items)
            upgrade_options.append({
                "type": "item",
                "label": f"Gain item: {item['name']}",
                "value": item
            })

        elif upgrade_type == "ability":
            locked = get_locked_abilities()
            if locked:
                ability = random.choice(locked)
                upgrade_options.append({
                    "type": "ability",
                    "label": f"Learn: {ability["name"]}",
                    "value": ability
                })





#Draw upgrade popup
def draw_upgrade_popup():
    global upgrade_popup_rect, confirm_upgrade_button_rect, upgrade_button_rects

    upgrade_options[:] = [opt for opt in upgrade_options if isinstance(opt, dict) and "label" in opt]

    popup_width = 700
    popup_height = 500
    popup_x = SCREEN_WIDTH // 2 - popup_width // 2
    popup_y = SCREEN_HEIGHT // 2 - popup_height // 2
    upgrade_popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    #Resets button rects
    upgrade_button_rects.clear()

    #Popup background
    pygame.draw.rect(screen, DARK_GRAY, upgrade_popup_rect)
    pygame.draw.rect(screen, WHITE, upgrade_popup_rect, 3)

    title = font.render("Choose a Stat to Upgrade", True, WHITE)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 40)))

    for i, option in enumerate(upgrade_options):
        rect = pygame.Rect(popup_x + 50, popup_y + 100 + i * 80, 600, 60)
        upgrade_button_rects.append(rect)

        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, YELLOW if selected_upgrade_index == i else WHITE, rect, 3)

        label = option["label"]
        start_text = font.render(label, True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=rect.center))

    if selected_upgrade_index is not None:
        confirm_upgrade_button_rect = pygame.Rect(popup_x + 250, popup_y + 430, 200, 40)
        draw_button(confirm_upgrade_button_rect, "Confirm")
    else:
        confirm_upgrade_button_rect = None





#Game Loop
running = True
while running:
    next_floor_triggered = False


    for event in pygame.event.get():
        #Close window
        if event.type == pygame.QUIT:
            running = False

        #ESC key to close game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if show_quit_popup:
                    show_quit_popup = False
                elif show_inventory_popup:
                    show_inventory_popup = False
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

        elif event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            start_floor(current_floor + 1)

        if game_state == STATE_GAME and next_floor_triggered:
            next_floor_triggered = False
            start_floor(current_floor + 1)

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

                if selected_class:
                    full_abilities = CLASS_ABILITIES[selected_class.name]
                    selected_class.attacks = full_abilities["attacks"]
                    selected_class.spells = full_abilities["spells"]
                    player_attacks = [selected_class.attacks[0]]
                    player_spells = [selected_class.spells[0]]

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

                if show_inventory_popup:
                    for i, item in enumerate(player_inventory):
                        if "rect" in item and item["rect"].collidepoint(mouse_pos):
                            selected_inventory_index = i
                            break

                if selected_inventory_index is not None and use_item_button_rect and use_item_button_rect.collidepoint(mouse_pos):
                    item = player_inventory[selected_inventory_index]
                    effect = item["effect"]
                    name = item["name"]
                    type = item["type"].lower()

                    #Apply item effect based on type
                    if item["type"] == "healing":
                        selected_class.stats["health"] += effect
                        combat_log.append(f"Used {item["name"]} - Restored {effect} HP.")
                    elif item["type"] == "mana":
                        selected_class.stats["mana"] += effect
                        combat_log.append(f"Used {item["name"]} - Increased mana by {effect}.")
                    elif item["type"].lower() == "damage":
                        selected_class.stats["attack"] += effect
                        combat_log.append(f"Used {item["name"]} - Attack increased by {effect}.")

                    #Removed used items
                    player_inventory.pop(selected_inventory_index)
                    selected_inventory_index = None
                    show_inventory_popup = False
                    use_item_button_rect = None




                if show_upgrade_popup:

                    for i, rect in enumerate(upgrade_button_rects):
                        if rect.collidepoint(mouse_pos):
                            selected_upgrade_index = i
                            break

                    if just_confirmed_upgrade:
                        continue

                    if (
                            selected_upgrade_index is not None
                            and confirm_upgrade_button_rect
                            and confirm_upgrade_button_rect.collidepoint(mouse_pos)
                            and not just_confirmed_upgrade
                    ):
                        chosen = upgrade_options[selected_upgrade_index]

                        if chosen["type"] == "stat":
                            selected_class.stats[chosen["value"]] += 10
                            combat_log.append(f"Upgraded {chosen['value']} by 10")

                        elif chosen["type"] == "item":
                            player_inventory.append(chosen["value"])
                            combat_log.append(f"Obtained item: {chosen['value']['name']}")

                        elif chosen["type"] == "ability":
                            ability = chosen["value"]  # This is a dict: {"name": ..., "damage": ...}
                            ability_name = ability["name"]

                            # Determine whether it's an attack or a spell based on class
                            if ability_name in [a["name"] for a in CLASS_ABILITIES[selected_class.name]["attacks"]]:
                                player_attacks.append(ability)
                                combat_log.append(f"Learned new attack: {ability_name}")
                            elif ability_name in [s["name"] for s in CLASS_ABILITIES[selected_class.name]["spells"]]:
                                player_spells.append(ability)
                                combat_log.append(f"Learned new spell: {ability_name}")
                            else:
                                combat_log.append(f"Learned unknown ability: {ability_name}")

                        just_confirmed_upgrade = True
                        show_upgrade_popup = False

                        # Prepare for next floor
                        pygame.time.set_timer(pygame.USEREVENT + 1, 200)

                if targeting_mode:
                    for enemy, enemy_rect in enemy_hitboxes:
                        if enemy_rect.collidepoint(mouse_pos):
                            # Get base attack and skill bonus
                            base_attack = selected_class.stats.get("attack", 0)
                            ability_damage = pending_attack_option.get("damage", 0)
                            total_damage = base_attack + ability_damage

                            # Apply damage
                            enemy.stats["health"] -= total_damage

                            # Add to combat log
                            combat_log.append(
                                f"{selected_class.name} used {pending_attack_option['name']} on {enemy.name} for {total_damage} damage!"
                            )

                            # Remove dead enemies
                            floor_enemies = [enemy for enemy in floor_enemies if enemy.stats["health"] > 0]

                            # Rebuild enemy hitboxes
                            enemy_hitboxes = []
                            draw_enemies(floor_enemies)

                            # Check for floor clear
                            if not floor_enemies:
                                show_upgrade_popup = True
                                generate_stat_upgrades()
                                just_confirmed_upgrade = False
                                selected_upgrade_index = None
                                confirm_upgrade_button_rect = None

                            # Use up action point
                            player_ap -= 1
                            player_turn = player_ap > 0
                            targeting_mode = False
                            pending_attack_option = None
                            break

                elif player_turn:
                    if player_ap > 0:
                        if attack_button_rect.collidepoint(mouse_pos):
                            combat_menu_state = "root" #Open root menu

                        elif combat_menu_state == "root":
                            if attack_root_button_rect.collidepoint(mouse_pos):
                                combat_menu_state = "attack"
                            elif spell_root_button_rect.collidepoint(mouse_pos):
                                combat_menu_state = "spell"

                        elif combat_menu_state == "attack":
                            for ability in player_attacks:
                                if isinstance(ability, dict) and "rect" in ability and ability["rect"].collidepoint(mouse_pos):
                                    pending_attack_option = ability
                                    combat_log.append(f"Used Attack: {ability['name']}")
                                    targeting_mode = True
                                    combat_menu_state = None
                                    break

                        elif combat_menu_state == "spell":
                            for ability in player_spells:
                                if ability["rect"].collidepoint(mouse_pos):
                                    ability_name = ability["name"]
                                    mana_cost = ability.get("mana_cost", 0)

                                    current_mana = selected_class.stats.get("mana", 0)
                                    if current_mana < mana_cost:
                                        combat_log.append(f"Not enough mana to cast {ability_name}!")
                                        combat_menu_state = None
                                        break

                                    #Deduct mana
                                    selected_class.stats["mana"] -= mana_cost
                                    combat_log.append(f"{selected_class.name} cast {ability_name} (-{mana_cost} mana)")

                                    #Handle special spells
                                    if ability_name == "Mana Shield":
                                        selected_class.stats["defence"] += 10
                                        combat_log.append(f"{selected_class.name}'s defence increased by 10.")
                                        player_ap -= 1
                                        player_turn = player_ap > 0
                                        combat_menu_state = None
                                        break

                                    elif ability_name == "Heal":
                                        selected_class.stats["health"] = min(selected_class.stats["health"] + 30, 100)
                                        combat_log.append(f"{selected_class.name} healed for 30 HP.")
                                        player_ap -= 1
                                        player_turn = player_ap > 0
                                        combat_menu_state = None
                                        break

                                    #Offensive spell → enter targeting
                                    targeting_mode = True
                                    pending_attack_option = ability
                                    combat_menu_state = None
                                    break


                        elif stats_button_rect.collidepoint(mouse_pos):
                            show_stats_popup = not show_stats_popup
                        elif item_button_rect.collidepoint(mouse_pos):
                            show_inventory_popup = True
                        elif combat_menu_state and not action_menu_rect.collidepoint(mouse_pos):
                            combat_menu_state = None


                    if player_ap <= 0:
                        player_turn = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and show_stats_popup:
                    show_stats_popup = False

            if not player_turn:
                def enemy_turn():
                    global player_turn, player_ap

                    for enemy in floor_enemies:
                        raw_attack = enemy.stats["attack"]
                        player_defence = selected_class.stats["defence"]
                        damage = max(1, raw_attack - player_defence)  # Always at least 1

                        selected_class.stats["health"] -= damage
                        log_msg = f"{enemy.name} attacks for {damage} damage"
                        print(log_msg)
                        combat_log.append(log_msg)

                    player_turn = True
                    player_ap = 3


                enemy_turn()

            if selected_class and selected_class.stats["health"] <= 0:
                game_state = STATE_GAME_OVER



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
        draw_combat_log()

        if show_upgrade_popup:
            draw_upgrade_popup()

        if show_inventory_popup:
            draw_inventory_popup()


    if show_quit_popup:
        draw_quit_popup()


    #Update the screen
    pygame.display.flip()

    #Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()
