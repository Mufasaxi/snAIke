import pygame
import pygame.locals
import sys
import random
import numpy as np

from snake import Snake
from food import Food
from pathfinder import Pathfinder

pygame.init()

# Window setup
WIDTH = 1000
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Optimised Path Snake')

clock = pygame.time.Clock()

# Grid setup
resolution = 20
cols = WIDTH // resolution
rows = HEIGHT // resolution
grid = []

# Snake setup
snake = Snake()
snake.x = random.randint(0, cols-1)
snake.y = random.randint(0, rows-1)
snake.WIDTH = 1
snake.HEIGHT = 1
snake.length = 1
snake_rect = pygame.Rect(snake.x*resolution, snake.y*resolution,
                         snake.WIDTH*resolution, snake.HEIGHT*resolution)

# Snake movement
snake.x_vel = 0
snake.y_vel = 0

# Food
food = Food()
food.x = random.randint(0, cols-1)
food.y = random.randint(0, rows-1)
food.WIDTH = 1
food.HEIGHT = 1

dataset_goal_length = 70000
dataset = [[],[]]

# Pathfinder
pathfinder = Pathfinder(rows, cols)


def draw_grid(grid: list[list[int]]) -> None:
    # Fields of grid
    for col in range(len(grid[0])):
        for row in range(len(grid)):
            if grid[row][col] == 0:
                pygame.draw.rect(window, (65, 65, 65), pygame.Rect(
                    col*resolution, row*resolution, resolution, resolution))
            elif grid[row][col] == -1:
                pygame.draw.rect(window, (255, 0, 0), pygame.Rect(
                    col*resolution, row*resolution, food.WIDTH*resolution, food.HEIGHT*resolution))
            elif grid[row][col] >= 1:
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(
                    col*resolution, row*resolution, snake.WIDTH*resolution, snake.HEIGHT*resolution))

    # Grid lines
    for col in range(0, WIDTH, resolution):
        pygame.draw.rect(window, (50, 50, 50), pygame.Rect(col, 0, 1, HEIGHT))

    for row in range(0, HEIGHT, resolution):
        pygame.draw.rect(window, (50, 50, 50), pygame.Rect(0, row, WIDTH, 1))


def fill_grid(cols: int, rows: int) -> list[list[int]]:
    return [[0 for col in range(cols)] for row in range(rows)]


def move_right(snake: Snake) -> int:
    snake.x_vel = 1
    return snake.x_vel


def move_left(snake: Snake) -> int:
    snake.x_vel = -1
    return snake.x_vel


def move_up(snake: Snake) -> int:
    snake.y_vel = -1
    return snake.y_vel


def move_down(snake: Snake) -> int:
    snake.y_vel = 1
    return snake.y_vel


def border_collision(snake: Snake) -> bool:
    if snake.x + snake.WIDTH > WIDTH:
        return True
        # snake.x_vel = 0
        # snake.x = WIDTH -snake.WIDTH
    if snake.x < 0:
        return True
        # snake.x_vel = 0
        # snake.x = 0
    if snake.y + snake.HEIGHT > HEIGHT:
        return True
        # snake.y_vel = 0
        # snake.y = HEIGHT - snake.HEIGHT
    if snake.y < 0:
        return True
        # snake.y_vel = 0
        # snake.y = 0


def self_collision(grid: list[list[int]], snake: Snake) -> bool:
    if snake.y > HEIGHT or snake.x < 0:
        return False
    if grid[snake.y][snake.x] > 1:
        return True
    return False


def food_collision(snake: Snake, food: Food) -> bool:
    left_collision, right_collision, top_collision, bottom_collision = False, False, False, False
    if (snake.x + snake.WIDTH > food.x):
        right_collision = True
    if (snake.x < food.x + food.WIDTH):
        left_collision = True
    if (snake.y + snake.HEIGHT > food.y):
        bottom_collision = True
    if (snake.y < food.y + food.HEIGHT):
        top_collision = True

    if (left_collision and right_collision and bottom_collision and top_collision):
        return True


def remove_tail(grid: list[list[int]]) -> None:
    for col in range(len(grid[0])):
        for row in range(len(grid)):
            if grid[row][col] > 0:
                grid[row][col] -= 1


def populate_dataset_list(grid: list[list[int]], direction: str) -> None:
   # convert string direction to numbers (in this case 2 bit binary)
    # while len(dataset[0]) < dataset_goal_length:
    match direction:
        case 'UP':
            direction_encoding = 0b00
        case 'RIGHT':
            direction_encoding = 0b01
        case 'DOWN':
            direction_encoding = 0b10
        case 'LEFT':
            direction_encoding = 0b11

    dataset[0].append(grid)
    dataset[1].append(direction_encoding)

        # print('added grid and direction pair')

    # print('done')
    # create_numpy_dataset(dataset)

def create_numpy_dataset(dataset: tuple[list[list[int]], int]) -> None:
    print('creating numpy dataset')
    x_file = 'X_data1.npy'
    y_file = 'y_data1.npy' 
    X = np.array(dataset[0], 'float32')
    y = np.array(dataset[1], 'float32')
    print(X.shape(), y.shape())
    np.save(x_file, X)
    np.save(y_file, y)
    sys.exit(0)

def main(snake:Snake, grid: list[list[int]]) -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print('dataset len', len(dataset[0]))
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
        
        # Filling grid array and drawing it onto window
        if not grid:
            grid = fill_grid(cols, rows)

        # Snake movement
        snake.x += snake.x_vel
        snake.y += snake.y_vel

        # Checking collision with border of window and with itself
        if (border_collision(snake)):
            print('GAME OVER')
            print('dataset len', len(dataset[0]))
            sys.exit(0)
        elif (self_collision(grid, snake)):
            print('SELF COLLISION')
            snake.x_vel = 0
            snake.y_vel = 0
            print('dataset len', len(dataset[0]))
            sys.exit(0)
        else:
            grid[snake.y][snake.x] = 1 + snake.length
            remove_tail(grid)

        # Checking collision with food
        if (food_collision(snake, food)):
            # print('ATE FOOD')
            snake.length += 1
            grid[food.y][food.x] = 0
            food.x = random.randint(0, cols-1)
            food.y = random.randint(0, rows-1)
            # Ensure that food doesn't spawn where snake is, this doesn't entirely work since I'm not checking entire snake body
            while True:
                if food.x != snake.x and food.y != snake.y:
                    break
                food.x = random.randint(0, cols-1)
                food.y = random.randint(0, rows-1)

        window.fill((65,65,65))

        draw_grid(grid)

        # Randomly placing the food in the grid and having it be drawn
        grid[food.y][food.x] = -1

        grid[snake.y][snake.x] = snake.length

        # Pathfinding using A* (still isn't flawless but good enough)
        numbered_grid = pathfinder.number_cells(grid)
        adjacency_list = pathfinder.make_adjacency_list(numbered_grid)
        edge_costs = pathfinder.calculate_edge_costs(adjacency_list, grid, numbered_grid)

        origin = numbered_grid[snake.y][snake.x]
        destination = numbered_grid[food.y][food.x]

        taxicab_distances = pathfinder.taxi_cab_distance(numbered_grid, destination)
        path = pathfinder.a_star(adjacency_list, edge_costs, taxicab_distances, origin, destination)[0]

        current_position = numbered_grid[snake.y][snake.x]

        for position in path:
            if position == current_position:
                continue
            if position == current_position + 1:
                snake.x += 1
                direction = 'RIGHT'
            elif position == current_position - 1:
                snake.x -= 1
                direction = 'LEFT'
            elif position == current_position + cols:
                snake.y += 1
                direction = 'DOWN'
            elif position == current_position - cols:
                snake.y -= 1
                direction = 'UP'
            if len(dataset[0]) < dataset_goal_length:
                populate_dataset_list(grid, direction)
            else:
                create_numpy_dataset(dataset)

        pygame.display.update()

        clock.tick(120)


if __name__ == '__main__':
    main(snake, grid)