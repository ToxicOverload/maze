import pygame
import os
from Maze import *

wait = False

# Uses the storage method using a 2-dimensional array where:
# . is a wall, # is nothing, @ is finish, and & is start
# Also, for our purposes, * is a filled dead end
maze = [["&",".",".",".",".",".","#","#","#","#"],
        ["#","#","#","#","#",".","#",".",".","."],
        ["#",".","#",".","#",".","#","#","#","#"],
        ["#",".","#",".","#",".","#",".",".","#"],
        ["#",".","#",".","#","#","#","#",".","#"],
        ["#",".",".",".","#",".","#",".",".","#"],
        ["#",".","#","#","#",".","#","#",".","#"],
        ["#","#","#",".",".",".",".",".",".","#"],
        [".",".","#","#","#",".","#","#","#","#"],
        ["#","#","#",".",".",".",".",".",".","@"]]

# Is it solving?
solving = True

# Draw the inputted board. Black is a wall, white is open, blue is start,
# gray is filled dead end, and purple is the end
def draw(board):
    screen.fill(white)
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == ".":
                pygame.draw.rect(screen, black, [y*tile_size,x*tile_size,tile_size,tile_size])
            elif board[x][y] == "@":
                pygame.draw.rect(screen, blue, [y*tile_size,x*tile_size,tile_size,tile_size])
            elif board[x][y] == "*":
                pygame.draw.rect(screen, gray, [y*tile_size,x*tile_size,tile_size,tile_size])
            elif board[x][y] == "&":
                pygame.draw.rect(screen, purple, [y*tile_size,x*tile_size,tile_size,tile_size])

    pygame.display.update()

# Check if a cell is a dead end by seeing the number of adjacent walls
def check_cell_for_dead_end(board, x, y):
    walls_adjacent = 0
    open_wall = ()
    if not x < 1:
        if board[y][x-1] in ".*":
            walls_adjacent += 1
        else:
            open_wall = (x-1, y)
    else:
        walls_adjacent += 1
    if not x >= len(board[y]) - 1:
        if board[y][x+1] in ".*":
            walls_adjacent += 1
        else:
            open_wall = (x+1, y)
    else:
        walls_adjacent += 1
    if not y < 1:
        if board[y-1][x] in ".*":
            walls_adjacent += 1
        else:
            open_wall = (x, y-1)
    else:
        walls_adjacent += 1
    if not y >= len(board) - 1:
        if board[y+1][x] in ".*":
            walls_adjacent += 1
        else:
            open_wall = (x, y+1)
    else:
        walls_adjacent += 1

    # Returns either false or the coords of the open side
    if walls_adjacent == 3 and board[y][x] not in ".*":
        return open_wall
    else:
        return False

# Fill a dead end
def fill_dead_end(start_x, start_y):
    x = start_x
    y = start_y
    filling = True

    while filling:
        # While filling, check each cell in a row and fill it if it's a dead end
        checker = check_cell_for_dead_end(maze, x, y)
        if checker != False and maze[y][x] not in "&@":
            maze[y][x] = "*"
            x = checker[0]
            y = checker[1]
        else:
            filling = False
        if wait:
            draw(maze)
            event_handler(pygame.event.get())
    return True

# Simple event handler, test for quitting
def event_handler(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

if __name__ == "__main__":
    # If the user wants it, import a maze
    if input("Do you want to load a file? ") in yes_synonyms:
        maze = import_maze()

    # Set the size of the tiles
    tile_size = int(600/len(maze))

    # Initiate pygame and board
    pygame.init()
    size = [len(maze)*tile_size,len(maze[0])*tile_size]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze Solver!")

    while solving:
        event_handler(pygame.event.get())
        draw(maze)

        # Go through board and fill all dead ends
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                fill_dead_end(x, y)
                if wait:
                    pygame.time.wait(1)
    pygame.time.wait(10)
