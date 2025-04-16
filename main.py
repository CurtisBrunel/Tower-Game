import pygame
import sys
import random

# ... [Keep all your existing character and enemy classes] ...

class GameState:
    CHARACTER_SELECT = 0
    TOWER_FLOOR = 1
    COMBAT = 2
    COMBAT_RESULT = 3




def main(characters=None):
    pygame.init()
    screen_width, screen_height = 1024, 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tower Adventure")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 32)
    small_font = pygame.font.SysFont('Arial', 24)

    if characters is None:
        characters = [
            Mage(screen_width // 4, screen_height // 2),
            Rogue(screen_width // 2, screen_height // 2),
            Warrior(3 * screen_width // 4, screen_height // 2)
        ]


    # Game state
    game_state = GameState.CHARACTER_SELECT
    selected_character = None
    current_floor = 1
    enemies = []
    combat_result = ""
    selected_action = 0  # 0=Fight, 1=Item

    # Create action boxes
    action_boxes = [
        pygame.Rect(screen_width // 2 - 150, screen_height - 150, 200, 80),
        pygame.Rect(screen_width // 2 + 150, screen_height - 150, 200, 80)
    ]

    def generate_enemies(floor_level):
        """Generate enemies based on floor level"""
        enemy_types = [Goblin, Skeleton, Ogre, Demon]
        num_enemies = min(floor_level + 1, 4)  # More enemies on higher floors

        enemies = []
        for i in range(num_enemies):
            x = 200 + i * 200
            y = 400
            enemy_class = random.choice(enemy_types)

            # Scale enemy stats with floor level
            enemy = enemy_class(x, y)
            enemy.max_hp += floor_level * 10
            enemy.hp = enemy.max_hp
            enemy.ad += floor_level * 2
            enemy.defense += floor_level

            enemies.append(enemy)
        return enemies
    # ... [Keep your existing generate_enemies() function] ...

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == GameState.COMBAT:
                        game_state = GameState.TOWER_FLOOR
                    elif game_state == GameState.TOWER_FLOOR:
                        game_state = GameState.CHARACTER_SELECT
                    elif game_state == GameState.CHARACTER_SELECT:
                        running = False

                elif game_state == GameState.COMBAT:
                    if event.key == pygame.K_LEFT:
                        selected_action = 0
                    elif event.key == pygame.K_RIGHT:
                        selected_action = 1
                    elif event.key == pygame.K_RETURN:
                        if selected_action == 0:  # Fight
                            # Simple combat - player attacks first enemy
                            if enemies:
                                damage = selected_character.ad
                                actual_damage = enemies[0].take_damage(damage)
                                combat_result = f"You hit {enemies[0].name} for {actual_damage} damage!"

                                # Enemy counterattack if alive
                                if enemies[0].is_alive():
                                    enemy_damage = enemies[0].attack()
                                    selected_character.hp -= enemy_damage
                                    combat_result += f"\n{enemies[0].name} hits you for {enemy_damage} damage!"
                                else:
                                    combat_result += f"\nYou defeated {enemies[0].name}!"
                                    enemies.pop(0)

                                # Check if combat ended
                                if not enemies:
                                    combat_result += "\n\nYou cleared this floor!\nPress any key to continue."
                                    current_floor += 1
                                elif selected_character.hp <= 0:
                                    combat_result += "\n\nYou were defeated!\nPress any key to return to character select."

                                game_state = GameState.COMBAT_RESULT

                        elif selected_action == 1:  # Item
                            combat_result = "You used a healing potion!\n+30 HP"
                            selected_character.hp = min(selected_character.max_hp, selected_character.hp + 30)
                            game_state = GameState.COMBAT_RESULT

                elif game_state == GameState.COMBAT_RESULT:
                    # Any key press continues
                    if not enemies or selected_character.hp <= 0:
                        game_state = GameState.CHARACTER_SELECT
                    else:
                        game_state = GameState.COMBAT
                    combat_result = ""

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GameState.CHARACTER_SELECT:
                    for character in characters:
                        if character.rect.collidepoint(event.pos):
                            selected_character = character
                            current_floor = 1
                            enemies = generate_enemies(current_floor)
                            game_state = GameState.TOWER_FLOOR

                elif game_state == GameState.COMBAT:
                    for i, box in enumerate(action_boxes):
                        if box.collidepoint(event.pos):
                            selected_action = i

        # Drawing
        screen.fill((20, 20, 40))

        if game_state == GameState.CHARACTER_SELECT:
            # Draw title
            title = font.render("Select Your Character", True, (255, 255, 255))
            screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

            # Draw all character options
            for character in characters:
                # Draw character sprite
                character.draw(screen)

                # Draw character name label
                name_text = small_font.render(character.name, True, (255, 255, 255))
                screen.blit(name_text, (
                    character.rect.centerx - name_text.get_width() // 2,
                    character.rect.bottom + 10
                ))

                # Highlight if mouse is hovering
                if character.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (255, 255, 255), character.rect, 2)

            # Draw instructions at bottom
            instructions = small_font.render(
                "Click a character to select or ESC to quit",
                True,
                (200, 200, 200)
            )
            screen.blit(instructions, (
                screen_width // 2 - instructions.get_width() // 2,
                screen_height - 50
            ))

        elif game_state == GameState.TOWER_FLOOR:
            # Tower background
            pygame.draw.rect(screen, (60, 60, 80), (100, 100, screen_width - 200, 500))

            # Floor display
            floor_text = font.render(f"Floor {current_floor}", True, (255, 255, 255))
            screen.blit(floor_text, (screen_width // 2 - floor_text.get_width() // 2, 120))

            # Draw player character
            player_display = selected_character
            player_display.rect.center = (screen_width // 2, 250)
            player_display.draw(screen)

            # Player stats
            stats = [
                f"HP: {player_display.hp}/{player_display.max_hp}",
                f"Attack: {player_display.ad}",
                f"Magic: {player_display.md}",
                f"Defense: {player_display.defense}"
            ]
            for i, stat in enumerate(stats):
                stat_text = small_font.render(stat, True, (255, 255, 255))
                screen.blit(stat_text, (screen_width // 2 - 200, 300 + i * 30))

            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)
                name_text = small_font.render(enemy.name, True, (255, 200, 200))
                screen.blit(name_text, (enemy.rect.centerx - name_text.get_width() // 2,
                                        enemy.rect.bottom + 5))

                # Health bar
                health_pct = enemy.hp / enemy.max_hp
                pygame.draw.rect(screen, (200, 0, 0),
                                 (enemy.rect.x, enemy.rect.y - 10,
                                  enemy.rect.width, 5))
                pygame.draw.rect(screen, (0, 200, 0),
                                 (enemy.rect.x, enemy.rect.y - 10,
                                  int(enemy.rect.width * health_pct), 5))

            # Instructions
            continue_text = small_font.render("Press ENTER to enter combat or ESC to return",
                                              True, (200, 200, 200))
            screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2,
                                        screen_height - 50))
            # Just add a "Press any key to continue" message
            continue_text = small_font.render("Press any key to enter combat...", True, (200, 200, 200))
            screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2, screen_height - 50))

        elif game_state == GameState.COMBAT:
            # Combat background
            pygame.draw.rect(screen, (40, 40, 60), (50, 50, screen_width - 100, screen_height - 200))

            # Draw player
            player_rect = pygame.Rect(150, 200, 120, 160)
            pygame.draw.rect(screen, (100, 100, 200), player_rect)
            char_text = font.render(selected_character.name, True, (255, 255, 255))
            screen.blit(char_text, (player_rect.x + 60 - char_text.get_width() // 2, player_rect.y - 40))

            # Player health
            health_text = small_font.render(f"HP: {selected_character.hp}/{selected_character.max_hp}", True,
                                            (255, 255, 255))
            screen.blit(health_text, (player_rect.x, player_rect.y + 170))

            # Draw enemies
            for i, enemy in enumerate(enemies):
                enemy_rect = pygame.Rect(600, 150 + i * 120, 120, 160)
                pygame.draw.rect(screen, (200, 100, 100), enemy_rect)
                enemy_text = font.render(enemy.name, True, (255, 255, 255))
                screen.blit(enemy_text, (enemy_rect.x + 60 - enemy_text.get_width() // 2, enemy_rect.y - 40))

                # Enemy health
                health_pct = enemy.hp / enemy.max_hp
                pygame.draw.rect(screen, (200, 0, 0), (enemy_rect.x, enemy_rect.y + 170, 120, 10))
                pygame.draw.rect(screen, (0, 200, 0), (enemy_rect.x, enemy_rect.y + 170, int(120 * health_pct), 10))

            # Action selection boxes
            actions = ["FIGHT", "ITEM"]
            for i, box in enumerate(action_boxes):
                color = (0, 150, 0) if i == selected_action else (0, 100, 0)
                pygame.draw.rect(screen, color, box)
                pygame.draw.rect(screen, (255, 255, 255), box, 2)
                action_text = font.render(actions[i], True, (255, 255, 255))
                screen.blit(action_text,
                            (box.x + 100 - action_text.get_width() // 2, box.y + 40 - action_text.get_height() // 2))

            # Instructions
            instr_text = small_font.render("Use LEFT/RIGHT to select, ENTER to confirm", True, (200, 200, 200))
            screen.blit(instr_text, (screen_width // 2 - instr_text.get_width() // 2, screen_height - 50))

        elif game_state == GameState.COMBAT_RESULT:
            # Combat results display
            pygame.draw.rect(screen, (30, 30, 50), (100, 100, screen_width - 200, screen_height - 200))

            # Split result text into lines
            lines = combat_result.split('\n')
            for i, line in enumerate(lines):
                result_text = font.render(line, True, (255, 255, 255))
                screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2,
                                          200 + i * 40))

            continue_text = small_font.render("Press any key to continue...", True, (200, 200, 200))
            screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2, screen_height - 150))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()