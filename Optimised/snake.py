import pygame
import pygame.locals
import sys

from food import Food

pygame.init()

# Window setup
WIDTH = 1000
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Optimised Path Snake')

clock = pygame.time.Clock()

# Grid setup
resolution = 50
cols = WIDTH // resolution
rows = HEIGHT // resolution

grid = []

# Snake setup
snake_x = 500
snake_y = 500
SNAKE_WIDTH = resolution
SNAKE_HEIGHT = resolution
snake_rect = pygame.Rect(snake_x, snake_y, SNAKE_WIDTH, SNAKE_HEIGHT)

# Snake movement
snake_x_vel = 0
snake_y_vel = 0

# Food
food = Food()

def draw_grid(cols, rows):
    # Fields of grid
    for col in range(cols):
        for row in range(rows):
            pygame.draw.rect(window, (0,0,255), pygame.Rect(col*resolution, row*resolution, resolution, resolution))

    # Grid lines
    for col in range(0, WIDTH, resolution):
        pygame.draw.rect(window, (50,50,50), pygame.Rect(col, 0, 1, HEIGHT))

    for row in range(0, HEIGHT, resolution):
        pygame.draw.rect(window, (50,50,50), pygame.Rect(0, row, WIDTH, 1))

def fill_grid(cols, rows):
    return [[0 for col in range(cols)] for row in range(rows)]

def move_right(snake_x_vel):
    snake_x_vel = resolution
    return snake_x_vel

def move_left(snake_x_vel):
    snake_x_vel = -resolution
    return snake_x_vel

def move_up(snake_y_vel):
    snake_y_vel = -resolution
    return snake_y_vel

def move_down(snake_y_vel):
    snake_y_vel = resolution
    return snake_y_vel

def main(snake_x, snake_x_vel, snake_y, snake_y_vel, grid):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)

        key_pressed = pygame.key.get_pressed()
        
        # Handling key presses for movement
        if key_pressed[pygame.locals.K_RIGHT]:
            snake_y_vel = 0
            snake_x_vel = move_right(snake_x_vel)

        if key_pressed[pygame.locals.K_LEFT]:
            snake_y_vel = 0
            snake_x_vel = move_left(snake_x_vel)

        if key_pressed[pygame.locals.K_UP]:
            snake_x_vel = 0
            snake_y_vel = move_up(snake_y_vel)

        if key_pressed[pygame.locals.K_DOWN]:
            snake_x_vel = 0
            snake_y_vel = move_down(snake_y_vel)
        
        # Snake movement
        snake_x += snake_x_vel
        snake_y += snake_y_vel

        # Keeping snake within screen
        if snake_x > WIDTH:
            snake_x_vel = 0
            snake_x = WIDTH -SNAKE_WIDTH
        if snake_x < 0:
            snake_x_vel = 0
            snake_x = 0
        if snake_y > HEIGHT:
            snake_y_vel = 0
            snake_y = HEIGHT - SNAKE_HEIGHT
        if snake_y < 0:
            snake_y_vel = 0
            snake_y = 0

        window.fill((65,65,65))

        if not grid:
            grid = fill_grid(cols, rows)

        draw_grid(cols, rows)

        snake_rect = pygame.Rect(snake_x,snake_y,SNAKE_WIDTH,SNAKE_HEIGHT)
        snake = pygame.draw.rect(window, (255,255,255), snake_rect)

        pygame.display.update()

        clock.tick(30)

main(snake_x, snake_x_vel, snake_y, snake_y_vel, grid)