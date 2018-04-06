import pygame
import os

# Things that mean yes
yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

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

# Some basic colors
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (100,100,100)
purple = (255,0,255)

# Set the current directory
path = os.path.dirname(__file__)

# If the mazes file doesn't exist, create it
if not os.path.exists(os.path.join(path, "mazes")):
    os.makedirs(os.path.join(path, "mazes"))

# Is it solving?
solving = True

# Import a maze from an .rle file
def import_maze():
    global maze

    # Reset maze
    maze = []
    
    # Ask filename
    file_name = input("What is the name of the file? (.rle files only, don't include the extension) ")

    # Include path and extension in file name
    file_name = os.path.join(path, "mazes", file_name + ".rle")

    # Open the file
    file = open(file_name, "r")

    # Read the file as lines
    lines = file.readlines()

    # Remove header line
    lines.pop(0)

    # Set maze to the body lines and remove the \n at the end of each line
    for line in lines:
        line = line.replace("\n","")
        row = line.split(",")
        maze.append(row)

    file.close()

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

# If the user wants it, import a maze
if input("Do you want to load a file? ") in yes_synonyms:
    import_maze()

# Set the size of the tiles
tile_size = int(600/len(maze))

# Initiate pygame and board
pygame.init()
size = [len(maze)*tile_size,len(maze[0])*tile_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Solver!")

while solving:
    event_handler(pygame.event.get())

    #Go through board and fill all dead ends
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            fill_dead_end(x, y)
            pygame.time.wait(1)

    draw(maze)

    pygame.time.wait(10)
