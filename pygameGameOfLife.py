import pygame, sys, time, random
from pygame.locals import *

# set up the grid dimensions and display scaling
PIXEL_SIZE = 25
GRID_WIDTH = 6
GRID_HEIGHT = 6

# Defines the interval of time that elapses between generations in milliseconds
GENERATION_AGE = 500

# An identity function which returns the same grid
def Identity(grid, row, col):
    return grid[row][col]

# Counts the number of live neighbours (cells with a value of 1) where
# a neighbour may wrap around to the other side of the grid, horizontally
# or vertically
def CountLiveNeighbours(grid, row, col):
    height = len(grid)
    width = len(grid[0])
    count = (
        grid[row-1][col-1] + grid[row-1][col] + grid[row-1][(col+1) % width] +
        grid[row][col-1] + grid[row][(col+1) % width] +
        grid[(row+1) % height][col-1] + grid[(row+1) % height][col] + grid[(row+1) % height][(col+1) % width]
    )
    return count

# Creates a printable copy of the grid for display in the console
def PrintGrid(grid):
    rows = []
    for row in grid:
        rows.append(' '.join(str(col) for col in row))
    return '\n'.join(rows)

# Conway's Game of Life rule - decides who lives and who dies!
def GameOfLifeRule(grid, row, col):
    isAlive = grid[row][col] == 1
    numNeighbours = CountLiveNeighbours(grid, row, col)

    # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    if (isAlive and numNeighbours < 2):
        return 0

    # Any live cell with two or three live neighbors lives on to the next generation.
    if (isAlive and (numNeighbours == 2 or numNeighbours == 3)):
        return 1

    # Any live cell with more than three live neighbors dies, as if by overpopulation.
    if (isAlive and (numNeighbours >= 4)):
        return 0

    # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    if (not isAlive and numNeighbours == 3):
        return 1
    
    return 0

# Given a grid, returns a new grid with the rule applied
def Generation(grid, rule):
    rows = len(grid)
    cols = len(grid[0])
    next_generation = [[None for col in range(cols)] for row in range(rows)]

    for row in range(rows):
        for col in range(cols):
            next_generation[row][col] = rule(grid, row, col)
    return next_generation

# Draws a grid on a windowSurface using the scaling in PIXEL_SIZE
# Live cells are WHITE and dead cells are BLACK
def DrawGrid(surface, grid):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    for row in range(len(grid)):
        top = row * PIXEL_SIZE
        for column in range(len(grid[row])):
            color = WHITE if grid[row][column] == 1 else BLACK
            left = column * PIXEL_SIZE
            pygame.draw.rect(surface, color, (left, top, PIXEL_SIZE, PIXEL_SIZE))

def RunGame(seedFunction):
    generation = seedFunction()

    print ('Running game with seed:')
    print (PrintGrid(generation))

    # set up pygame
    pygame.init()
    windowSurface = pygame.display.set_mode((PIXEL_SIZE * GRID_HEIGHT, PIXEL_SIZE * GRID_WIDTH), 0)
    pygame.display.set_caption('Conway\'s Game of Life')
    pygame.time.set_timer(pygame.USEREVENT, GENERATION_AGE)

    # run the game loop
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.USEREVENT):
                generation = Generation(generation, GameOfLifeRule)
                DrawGrid(windowSurface, generation)
                pygame.display.update()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Returns a grid which has a glider that will wrap around
def GliderGrid():
    return [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0], 
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

# Returns a random grid of GRID_HEIGHT and GRID_WIDTH
def RandomGrid():
    return [[random.randint(0, 1) for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]

RunGame(RandomGrid)