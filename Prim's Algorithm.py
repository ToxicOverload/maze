import pygame
from random import randint, choice
import os
from math import sqrt

wait = False

# . is walls, # is nothing, @ is finish, & is start
maze = []

maze_size = 0
while not (maze_size >= 5):
    maze_size = input("How big do you want it to be? ")
    try:
        maze_size = int(maze_size)
        if not maze_size >= 5:
            print("Please make it at least 5!")
            pass
    except ValueError:
        print("Please make it an integer.")
        maze_size = 0

for y in range(maze_size):
    row = []
    for x in range(maze_size):
        row.append(".")
    maze.append(row)

cells_list = []

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
purple = (255,0,255)

players = []
creating = True
events = []

wait_time = 0

path = os.path.dirname(__file__)

if not os.path.exists(os.path.join(path, "mazes")):
    os.makedirs(os.path.join(path, "mazes"))

def save_maze(board):
    save_name = ""

    while len(save_name) == 0:
        save_name = input("What do you want to save it as? (Don't include the extension) ")

    save_name = os.path.join(path, "mazes", save_name + ".txt")

    file = open(save_name, "w+")

    file.write("width: " + str(maze_size) + "\n")

    temp_board = board
    for row in temp_board:
        row = str(row)
        row = row.replace("[","")
        row = row.replace("]","")
        row = row.replace("'","")
        row = row.replace(" ","")
        file.write(row + "\n")

def neighbors(cell):
    neighbors = []
    x = cell[0]
    y = cell[1]

    if x-2 >= 0 and maze[y][x-2] == ".":
        neighbors.append([x-2,y])
    if x+2 <= maze_size - 1 and maze[y][x+2] == ".":
        neighbors.append([x+2,y])
    if y-2 >= 0 and maze[y-2][x] == ".":
        neighbors.append([x,y-2])
    if y+2 <= maze_size - 1 and maze[y+2][x] == ".":
        neighbors.append([x,y+2])
    return neighbors

def create_passage(cell, cell2):
    if cell[0] > cell2[0]:
        maze[cell[1]][cell[0]-1] = "#"
    if cell[0] < cell2[0]:
        maze[cell[1]][cell[0]+1] = "#"
    if cell[1] > cell2[1]:
        maze[cell[1]-1][cell[0]] = "#"
    if cell[1] < cell2[1]:
        maze[cell[1]+1][cell[0]] = "#"

def set_start_and_end():
    x = randint(0,maze_size-1)
    y = randint(0,maze_size-1)

    x2 = randint(0,maze_size-1)
    y2 = randint(0,maze_size-1)

    while not (sqrt((x2-x)**2 + (y2-y)**2) > maze_size/2 * 1.5 and maze[y][x] == "#" and maze[y2][x2] == "#"):
        x = randint(0,maze_size-1)
        y = randint(0,maze_size-1)
        
        x2 = randint(0,maze_size-1)
        y2 = randint(0,maze_size-1)

    maze[y][x] = "@"
    maze[y2][x2] = "&"

def create():
    global cells_list
    global creating

    start_cell = [-1,-1]
    while start_cell[0] % 2 == 1 and start_cell[0] < 0 and start_cell[1] % 2 == 1 and start_cell[1] < 0:
        start_cell = [randint(1,maze_size-2),randint(1,maze_size-2)]

    cells_list.append([start_cell[0],start_cell[1]])
    maze[cells_list[0][1]][cells_list[0][0]] = "#"

    while len(cells_list) > 0:
        current_cell = choice(cells_list)

        if len(neighbors(current_cell)) > 0:
            random_neighbor = choice(neighbors(current_cell))
            maze[random_neighbor[1]][random_neighbor[0]] = "#"

            create_passage(current_cell, random_neighbor)

            cells_list.append(random_neighbor)
        else:
            cells_list.remove(current_cell)

        
        get_events()
        handle_events(events)
        if wait:
            draw(maze)
            pygame.time.wait(wait_time)
    set_start_and_end()

def get_events():
    global events
    events = []
    for event in pygame.event.get():
        events.append(event)

def handle_events(events_list):
    global playing
    for event in events_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                playing = False
                pygame.quit()
                quit()
            elif event.key == pygame.K_s:
                save_maze(maze)

def draw(board):
    screen.fill(white)
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == ".":
                pygame.draw.rect(screen, black, [y*tile_size,x*tile_size,tile_size,tile_size])
            elif board[x][y] == "@":
                pygame.draw.rect(screen, blue, [y*tile_size,x*tile_size,tile_size,tile_size])
            elif board[x][y] == "&":
                pygame.draw.rect(screen, purple, [y*tile_size,x*tile_size,tile_size,tile_size])
    pygame.display.update()

tile_size = int(600/len(maze))

pygame.init()
size = [len(maze)*tile_size,len(maze[0])*tile_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Fun!")

create()

while True:
    get_events()
    handle_events(events)
    draw(maze)
    pygame.time.wait(wait_time)

pygame.quit()
quit()
