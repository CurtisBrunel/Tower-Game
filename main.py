import pygame
import sys
import random

class Warrior:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue for mage
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Character stats
        self.max_hp = 100
        self.hp = 100  # Health Points
        self.defense = 10  # Defense
        self.ad = 40  # Attack Damage (physical)
        self.md = 10  # Magic Damage
        self.sp = 50  # Speed
        self.energy = 120  # Energy/Stamina

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def modify_stats(self, hp_change=0, defense_change=0, ad_change=0,
                     md_change=0, sp_change=0, energy_change=0):
        """Method to modify character stats during gameplay"""
        self.hp = max(0, min(self.hp + hp_change, self.max_hp))
        self.defense = max(0, self.defense + defense_change)
        self.ad = max(0, self.ad + ad_change)
        self.md = max(0, self.md + md_change)
        self.sp = max(0, self.sp + sp_change)
        self.energy = max(0, self.energy + energy_change)




class Mage:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green for rogue
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Character stats
        self.max_hp = 100
        self.hp = 100  # Health Points
        self.defense = 10  # Defense
        self.ad = 40  # Attack Damage (physical)
        self.md = 10  # Magic Damage
        self.sp = 50  # Speed
        self.energy = 120  # Energy/Stamina

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def modify_stats(self, hp_change=0, defense_change=0, ad_change=0,
                     md_change=0, sp_change=0, energy_change=0):
        """Method to modify character stats during gameplay"""
        self.hp = max(0, min(self.hp + hp_change, self.max_hp))
        self.defense = max(0, self.defense + defense_change)
        self.ad = max(0, self.ad + ad_change)
        self.md = max(0, self.md + md_change)
        self.sp = max(0, self.sp + sp_change)
        self.energy = max(0, self.energy + energy_change)



class Rogue:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red for warrior
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Character stats
        self.max_hp = 100
        self.hp = 100  # Health Points
        self.defense = 10  # Defense
        self.ad = 40  # Attack Damage (physical)
        self.md = 10  # Magic Damage
        self.sp = 50  # Speed
        self.energy = 120  # Energy/Stamina

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def modify_stats(self, hp_change=0, defense_change=0, ad_change=0,
                     md_change=0, sp_change=0, energy_change=0):
        """Method to modify character stats during gameplay"""
        self.hp = max(0, min(self.hp + hp_change, self.max_hp))
        self.defense = max(0, self.defense + defense_change)
        self.ad = max(0, self.ad + ad_change)
        self.md = max(0, self.md + md_change)
        self.sp = max(0, self.sp + sp_change)
        self.energy = max(0, self.energy + energy_change)




def main():
    # Initialise Pygame
    pygame.init()

    # Set up the display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tower Game")

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Update the display
        pygame.display.flip()

    # Clean up and exit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()