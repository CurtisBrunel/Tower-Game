import pygame
import sys


# --- Character Classes ---
class Mage:
    def __init__(self, x, y):
        self.image = pygame.Surface((80, 120))
        self.image.fill((0, 100, 255))  # Blue
        self.rect = self.image.get_rect(center=(x, y))
        self.name = "Mage"

        # Stats
        self.max_hp = 80
        self.hp = 80
        self.defense = 15
        self.ad = 20
        self.md = 50
        self.sp = 30
        self.energy = 100

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Rogue:
    def __init__(self, x, y):
        self.image = pygame.Surface((80, 120))
        self.image.fill((50, 200, 50))  # Green
        self.rect = self.image.get_rect(center=(x, y))
        self.name = "Rogue"

        # Stats
        self.max_hp = 100
        self.hp = 100
        self.defense = 10
        self.ad = 40
        self.md = 10
        self.sp = 50
        self.energy = 120

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Warrior:
    def __init__(self, x, y):
        self.image = pygame.Surface((80, 120))
        self.image.fill((200, 50, 50))  # Red
        self.rect = self.image.get_rect(center=(x, y))
        self.name = "Warrior"

        # Stats
        self.max_hp = 150
        self.hp = 150
        self.defense = 30
        self.ad = 45
        self.md = 5
        self.sp = 20
        self.energy = 80

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# --- Game States ---
class GameState:
    CHARACTER_SELECT = 0
    GAMEPLAY = 1


# --- Main Game ---
def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Character Select Demo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

    # Game state
    game_state = GameState.CHARACTER_SELECT
    selected_character = None

    # Create character selection options
    mage = Mage(screen_width // 4, screen_height // 2)
    rogue = Rogue(screen_width // 2, screen_height // 2)
    warrior = Warrior(3 * screen_width // 4, screen_height // 2)
    characters = [mage, rogue, warrior]

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == GameState.GAMEPLAY:
                        game_state = GameState.CHARACTER_SELECT
                    else:
                        running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GameState.CHARACTER_SELECT:
                    for character in characters:
                        if character.rect.collidepoint(event.pos):
                            selected_character = character
                            game_state = GameState.GAMEPLAY

        # Drawing
        screen.fill((20, 20, 20))  # Dark gray background

        if game_state == GameState.CHARACTER_SELECT:
            # Draw title
            title = font.render("Select Your Character", True, (255, 255, 255))
            screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

            # Draw character options
            for i, character in enumerate(characters):
                character.draw(screen)

                # Draw character name
                name_text = small_font.render(character.name, True, (255, 255, 255))
                screen.blit(name_text, (character.rect.centerx - name_text.get_width() // 2,
                                        character.rect.bottom + 10))

                # Draw hover effect
                if character.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (255, 255, 255), character.rect, 2)

            # Draw instructions
            instructions = small_font.render("Click a character to select or ESC to quit",
                                             True, (200, 200, 200))
            screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2,
                                       screen_height - 50))

        elif game_state == GameState.GAMEPLAY:
            # Draw gameplay screen with selected character
            char_text = font.render(f"Playing as: {selected_character.name}", True, (255, 255, 255))
            screen.blit(char_text, (screen_width // 2 - char_text.get_width() // 2, 50))

            selected_character.draw(screen)

            # Draw stats
            stats = [
                f"HP: {selected_character.hp}/{selected_character.max_hp}",
                f"DEF: {selected_character.defense}",
                f"AD: {selected_character.ad}",
                f"MD: {selected_character.md}",
                f"SP: {selected_character.sp}",
                f"Energy: {selected_character.energy}"
            ]

            for i, stat in enumerate(stats):
                stat_text = small_font.render(stat, True, (255, 255, 255))
                screen.blit(stat_text, (selected_character.rect.centerx - stat_text.get_width() // 2,
                                        selected_character.rect.bottom + 30 + i * 25))

            # Draw instructions
            instructions = small_font.render("Press ESC to return to character select",
                                             True, (200, 200, 200))
            screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2,
                                       screen_height - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()