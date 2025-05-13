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

#Game States
STATE_TITLE = "title"
STATE_START = "start"
game_state = STATE_TITLE

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

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
                    print("Start Game Clicked")
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False

    #Screen rendering based on state
    if game_state == STATE_TITLE:
        draw_title_screen()
    elif game_state == STATE_START:
        draw_start_screen()



    #Update the screen
    pygame.display.flip()

    #Limit FPS
    clock.tick(60)
pygame.quit()
sys.exit()
