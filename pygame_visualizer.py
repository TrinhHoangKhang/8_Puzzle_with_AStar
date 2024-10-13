import pygame
import numpy as np
from Puzzle_Solver import Puzzle_Solver
import threading
import time

# Elements size constant
GAME_SIZE = 3
SQUARE_SIZE = 100
SCREEN_WIDTH = GAME_SIZE * SQUARE_SIZE
SCREEN_HEIGHT = GAME_SIZE * SQUARE_SIZE + SQUARE_SIZE / 2
BUTTON_REGION_HEIGHT = SCREEN_HEIGHT - SCREEN_WIDTH
# Color constant
BUTTON_REGION_C = (47, 255, 255)
SQUARE_C = (249, 249, 69)
BLANK_SQUARE_C = (255, 255, 255)
BUTTON_C = (108, 238, 238)
FADED_BUTTON_C = (150, 150, 150)
# Elements
game_region = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH)
button_region = pygame.Rect(
    0, SCREEN_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT - SCREEN_WIDTH)
reset_button = pygame.Rect(
    0, SCREEN_WIDTH, SCREEN_WIDTH / 2, BUTTON_REGION_HEIGHT)
run_button = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_WIDTH,
                         SCREEN_WIDTH / 2, BUTTON_REGION_HEIGHT)

# Running state variable
puzzle_solver = Puzzle_Solver()
blank_pos = puzzle_solver.start.blank_pos
path = []
is_moving_piece = False


def draw_region(screen):
    pygame.draw.rect(screen, 'white', game_region)
    pygame.draw.rect(screen, BUTTON_REGION_C, button_region)

def draw_squares(screen):
    global blank_pos
    font = pygame.font.Font(None, 72)

    for row in range(GAME_SIZE):
        for col in range(GAME_SIZE):
            if (row, col) != blank_pos:
                square_c = SQUARE_C
            else:
                square_c = BLANK_SQUARE_C
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(screen, square_c,
                             (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0),
                             (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

            # Draw the number
            if (row, col) != blank_pos:
                text = font.render(
                    str(puzzle_solver.start.matrix[row, col]), True, (0, 0, 9))
                text_rect = text.get_rect(
                    center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                screen.blit(text, text_rect)

def draw_button(screen):
    button_c = FADED_BUTTON_C if is_moving_piece else BUTTON_C

    font = pygame.font.Font(None, 45)
    pygame.draw.rect(screen, button_c, reset_button)
    pygame.draw.rect(screen, (0, 0, 0), reset_button, 2)
    text = font.render('Reset', True, (0, 0, 9))
    text_rect = text.get_rect(center=(reset_button.center))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, button_c, run_button)
    pygame.draw.rect(screen, (0, 0, 0), run_button, 2)
    text = font.render('Run', True, (0, 0, 9))
    text_rect = text.get_rect(center=(run_button.center))
    screen.blit(text, text_rect)

def update_state_on_path():
    global path, blank_pos, is_moving_piece
    for new_pos in path:
        puzzle_solver.start.matrix[blank_pos], puzzle_solver.start.matrix[
            new_pos] = puzzle_solver.start.matrix[new_pos], puzzle_solver.start.matrix[blank_pos]
        blank_pos = new_pos
        time.sleep(0.25)
    is_moving_piece = False

def run_game():
    global path, is_moving_piece
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not is_moving_piece:
                    if run_button.collidepoint(event.pos):
                        path = puzzle_solver.perform_search()
                        print("Path: \n", path)
                        is_moving_piece = True
                        # A theard that constantly update the state base on path list
                        t = threading.Thread(target=update_state_on_path)
                        t.start()

                    if reset_button.collidepoint(event.pos):
                        print("\n Generate new random game...")
                        puzzle_solver.randomize_start_state()

        # Do something
        draw_squares(screen)
        draw_button(screen)
        # Refresh screen
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()


run_game()
