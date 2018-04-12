import pygame
import os

# A list of things that mean yes
yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

# Uses the storage method using a 2-dimensional array where:
# . is a wall, # is nothing, @ is finish, and & is start
maze = [["&",".",".",".",".",".","#","#","#","#"],
        ["#",".","#","#","#",".","#",".",".","."],
        ["#",".","#",".","#",".","#","#","#","#"],
        ["#",".","#",".","#",".","#",".",".","#"],
        ["#",".","#",".","#","#","#","#",".","#"],
        ["#",".",".",".","#",".","#",".",".","#"],
        ["#",".","#",".","#",".","#","#",".","#"],
        ["#","#","#",".","#","#","#",".",".","#"],
        [".",".","#","#","#",".","#","#",".","#"],
        ["#","#","#",".",".",".",".",".",".","@"]]

# Just the start and end coordinates of the maze
start_coords = []
end_coords = []

# An array that stores the solution tiles
solution = []

# An array that holds the distance from each tile to the start. -1 is the default.
distances = []

# A stack of tiles to be marked with their distance
marking_stack = []

# Some basic colors I use
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (100,100,100)
purple = (255,0,255)

# The time to wait between frames
wait_time = 50

# Set the current directory
path = os.path.dirname(__file__)

# If the mazes file doesn't exist, create it
if not os.path.exists(os.path.join(path, "mazes")):
    os.makedirs(os.path.join(path, "mazes"))

# Draw the board. White is an open space, black is a wall, blue is the start,
# purple is the end, and green is a solution tile
def draw(board):
    screen.fill(white)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == ".":
                pygame.draw.rect(screen, black, [x*tile_size,y*tile_size,tile_size,tile_size])
            elif board[y][x] == "@":
                pygame.draw.rect(screen, blue, [x*tile_size,y*tile_size,tile_size,tile_size])
            elif board[y][x] == "&":
                pygame.draw.rect(screen, purple, [x*tile_size,y*tile_size,tile_size,tile_size])
            if distances[y][x] > 0:
                distance_text = font.render(str(distances[y][x]), False, gray)
                text_size = distance_text.get_size()
                screen.blit(distance_text, [x*tile_size + (tile_size/2) - text_size[0]/2, y*tile_size + (tile_size/2) - text_size[1]/2])
    for tile in solution:
        pygame.draw.rect(screen, green, [tile[0]*tile_size,tile[1]*tile_size,tile_size,tile_size])
    pygame.display.update()

# Import a maze from an .txt file
def import_maze():
    global maze

    # Reset maze
    maze = []
    
    # Ask filename
    file_name = input("What is the name of the file? (.txt files only, don't include the extension) ")

    # Include path and extension in file name
    file_name = os.path.join(path, "mazes", file_name + ".txt")

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

# Returns the tile adjacent to the inputed one with a lower distance value
def return_lower(x, y):
    try:
        if distances[y][x-1] < distances[y][x] and distances[y][x-1] > -1:
            return (x-1, y)
    except IndexError:
        pass
    try:
        if distances[y][x+1] < distances[y][x] and distances[y][x+1] > -1:
            return (x+1, y)
    except IndexError:
        pass
    try:
        if distances[y-1][x] < distances[y][x] and distances[y-1][x] > -1:
            return (x, y-1)
    except IndexError:
        pass
    try:
        if distances[y+1][x] < distances[y][x] and distances[y+1][x] > -1:
            return (x, y+1)
    except IndexError:
        pass

def find_end_path(end_x, end_y):
    global solution
    x = end_x
    y = end_y

    # While the current distance is > 1, set the current tile to the one below
    # the previous one and add it to the solution
    while distances[y][x] > 1:
        lower = return_lower(x, y)
        x = lower[0]
        y = lower[1]
        solution.append([x,y])
        event_handler(pygame.event.get())
        draw(maze)
        pygame.time.wait(wait_time)

# Mark the distance values of the neighboring cells
def mark_neighbors(start_distance, x, y):
    global distances
    global marking_stack

    try:
        if maze[y][x-1] != "." and x > 0 and distances[y][x-1] == -1:
            if maze[y][x-1] == "@":
                print("The end is " + str(start_distance+1) + " away from the start.")
                distances[y][x-1] = start_distance+1
                del marking_stack[:]
                return True
            else:
                distances[y][x-1]  = start_distance + 1
                marking_stack.append([x-1,y,start_distance + 1])
    except IndexError:
        pass
    try:
        if maze[y][x+1] != "." and x < len(maze[y]) and distances[y][x+1] == -1:
            if maze[y][x+1] == "@":
                print("The end is " + str(start_distance+1) + " away from the start.")
                distances[y][x+1] = start_distance+1
                del marking_stack[:]
                return True
            else:
                distances[y][x+1]  = start_distance + 1
                marking_stack.append([x+1,y,start_distance + 1])
    except IndexError:
        pass
    try:
        if maze[y-1][x] != "." and y > 0 and distances[y-1][x] == -1:
            if maze[y-1][x] == "@":
                print("The end is " + str(start_distance+1) + " away from the start.")
                distances[y-1][x] = start_distance+1
                del marking_stack[:]
                return True
            else:
                distances[y-1][x]  = start_distance + 1
                marking_stack.append([x,y-1,start_distance + 1])
    except IndexError:
        pass
    try:
        if maze[y+1][x] != "." and y < len(maze) and distances[y+1][x] == -1:
            if maze[y+1][x] == "@":
                print("The end is " + str(start_distance+1) + " away from the start.")
                distances[y+1][x] = start_distance+1
                del marking_stack[:]
                return True
            else:
                distances[y+1][x]  = start_distance + 1
                marking_stack.append([x,y+1,start_distance + 1])
    except IndexError:
        pass
    return True

def mark_all(start_x, start_y):
    # Mark neighbors of starting cell
    mark_neighbors(distances[start_y][start_x], start_x, start_y)

    # While the stack is not empty, mark the neighbors of the top of the stack,
    # and remove it from the stack
    while len(marking_stack) > 0:
        mark_neighbors(distances[marking_stack[0][1]][marking_stack[0][0]], marking_stack[0][0], marking_stack[0][1])
        try:
            marking_stack.pop(0)
        except IndexError:
            pass
        event_handler(pygame.event.get())
        draw(maze)
        pygame.time.wait(wait_time)

    # Using the newly set distance values, find the path through them
    find_end_path(end_coords[0], end_coords[1])

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

# If the user wants, import a maze
if input("Do you want to load a file? ") in yes_synonyms:
    import_maze()

# Set values for start and end coords and distances
for y in range(len(maze)):
    row = []
    for x in range(len(maze[y])):
        if maze[y][x] == "&":
            row.append(0)
            start_coords.append(x)
            start_coords.append(y)
        elif maze[y][x] == "@":
            row.append(-1)
            end_coords.append(x)
            end_coords.append(y)
        else:
            row.append(-1)
    distances.append(row)

# Set the size of the tiles
tile_size = int(600/len(maze))

# Startup pygame and the display
pygame.init()
size = [len(maze)*tile_size,len(maze[0])*tile_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Solver!")

# Set the font to be arial with a size of half of tile_size
font = pygame.font.SysFont("arial", int(tile_size/2))

draw(maze)

# Mark all tiles' distances
mark_all(start_coords[0],start_coords[1])

# Just keep running after it's all solved
while True:
    event_handler(pygame.event.get())
    draw(maze)
