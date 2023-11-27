import pygame
import pygame.locals
import sys
import random

from snake import Snake
from food import Food

pygame.init()

# Window setup
WIDTH = 1000
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Optimised Path Snake')

clock = pygame.time.Clock()

# Grid setup
resolution = 25
cols = WIDTH // resolution
rows = HEIGHT // resolution

grid = []

# Snake setup
snake = Snake()
snake.x = 500
snake.y = 500
snake.WIDTH = resolution
snake.HEIGHT = resolution
snake_rect = pygame.Rect(snake.x, snake.y, snake.WIDTH, snake.HEIGHT)

# Snake movement
snake.x_vel = 0
snake.y_vel = 0

# Food
food = Food()
food.x = random.randint(0, cols)
food.y = random.randint(0, rows)

def draw_grid(grid):
    # Fields of grid
    for col in range(len(grid[0])):
        for row in range(len(grid)):
            if grid[row][col] == 0:
                pygame.draw.rect(window, (65,65,65), pygame.Rect(col*resolution, row*resolution, resolution, resolution))
            else:
                pygame.draw.rect(window, (255,0,0), pygame.Rect(col*resolution, row*resolution, resolution, resolution))


    # Grid lines
    for col in range(0, WIDTH, resolution):
        pygame.draw.rect(window, (50,50,50), pygame.Rect(col, 0, 1, HEIGHT))

    for row in range(0, HEIGHT, resolution):
        pygame.draw.rect(window, (50,50,50), pygame.Rect(0, row, WIDTH, 1))

def fill_grid(cols: int, rows: int):
    return [[0 for col in range(cols)] for row in range(rows)]

def move_right(snake:Snake) -> int:
    snake.x_vel = resolution
    return snake.x_vel

def move_left(snake:Snake) -> int:
    snake.x_vel = -resolution
    return snake.x_vel

def move_up(snake:Snake) -> int:
    snake.y_vel = -resolution
    return snake.y_vel

def move_down(snake:Snake) -> int:
    snake.y_vel = resolution
    return snake.y_vel

def check_border_collison(snake:Snake) -> bool:
    if snake.x > WIDTH:
        return True
        # snake.x_vel = 0
        # snake.x = WIDTH -snake.WIDTH
    if snake.x < 0:
        return True
        # snake.x_vel = 0
        # snake.x = 0
    if snake.y > HEIGHT:
        return True
        # snake.y_vel = 0
        # snake.y = HEIGHT - snake.HEIGHT
    if snake.y < 0:
        return True
        # snake.y_vel = 0
        # snake.y = 0 

def main(snake:Snake, grid):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)

        key_pressed = pygame.key.get_pressed()
        
        # Handling key presses for movement
        if key_pressed[pygame.locals.K_RIGHT]:
            snake.y_vel = 0
            snake.x_vel = move_right(snake)

        if key_pressed[pygame.locals.K_LEFT]:
            snake.y_vel = 0
            snake.x_vel = move_left(snake)

        if key_pressed[pygame.locals.K_UP]:
            snake.x_vel = 0
            snake.y_vel = move_up(snake)

        if key_pressed[pygame.locals.K_DOWN]:
            snake.x_vel = 0
            snake.y_vel = move_down(snake)
        
        # Snake movement
        snake.x += snake.x_vel
        snake.y += snake.y_vel

        # Checking collision with border of window
        if (check_border_collison(snake)):
            print('GAME OVER')
            sys.exit(0)

        window.fill((65,65,65))

        # Filling grid array and drawing it onto window
        if not grid:
            grid = fill_grid(cols, rows)

        draw_grid(grid)

        # Randomly placing the food in the grid and having it be drawn
        grid[food.y][food.x] = -1

        snake_rect = pygame.Rect(snake.x,snake.y,snake.WIDTH,snake.HEIGHT)
        snake_rect_draw = pygame.draw.rect(window, (255,255,255), snake_rect)

        pygame.display.update()

        clock.tick(30)


main(snake, grid)