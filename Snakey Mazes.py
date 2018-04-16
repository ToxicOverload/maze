import pygame
from random import randint, choice
import os
from math import sqrt
import Maze

wait = False

# . is walls, # is nothing, @ is finish, & is start
maze_size = 0
while not (maze_size >= 5):
    maze_size = input("How big do you want it to be? ")
    try:
        maze_size = int(maze_size)
        if not maze_size >= 5:
            print("Please make it at least 5!")
    except ValueError:
        print("Please make it an integer.")
        maze_size = 0

maze = Maze.Maze(maze_size, maze_size)
cells_list = []

players = []
creating = True
events = []

tile_size = int(600 / maze.height)
pygame.init()
size = [maze.width * tile_size, maze.height * tile_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Fun!")

wait_time = 0

def neighbors(cell):
    neighbors = []
    x = cell[0]
    y = cell[1]

    if x-2 >= 0 and maze.at(x-2, y) == ".":
        neighbors.append([x-2,y])
    if x+2 <= maze.width - 1 and maze.at(x+2, y) == ".":
        neighbors.append([x+2,y])
    if y-2 >= 0 and maze.at(x, y-2) == ".":
        neighbors.append([x,y-2])
    if y+2 <= maze_size - 1 and maze.at(x, y+2) == ".":
        neighbors.append([x,y+2])
    return neighbors

def create_passage(cell, cell2):
    if cell[0] > cell2[0]:
        maze.set(cell[0]-1, cell[1], "#")
    if cell[0] < cell2[0]:
        maze.set(cell[0]+1, cell[1], "#")
    if cell[1] > cell2[1]:
        maze.set(cell[0], cell[1]-1, "#")
    if cell[1] < cell2[1]:
        maze.set(cell[0], cell[1]+1, "#")

def set_start_and_end():
    x = randint(0, maze.width - 1)
    y = randint(0, maze.height - 1)

    x2 = randint(0, maze.width-1)
    y2 = randint(0, maze.height-1)

    while not (sqrt((x2-x)**2 + (y2-y)**2) > maze_size/2 * 1.5 and maze.at(x,y) == "#" and maze.at(x2,y2) == "#"):
        x = randint(0, maze.width - 1)
        y = randint(0, maze.height - 1)
        
        x2 = randint(0, maze.width - 1)
        y2 = randint(0, maze.height - 1)

    maze.set(x, y, "@")
    maze.set(x2, x2, "&")

def create():
    global cells_list
    global creating
    start_cell = [-1, -1]
    while start_cell[0] % 2 == 1 and start_cell[0] < 0 and start_cell[1] % 2 == 1 and start_cell[1] < 0:
        start_cell = [randint(1, maze.width - 2), randint(1, maze.height - 2)]
    cells_list.append([start_cell[0], start_cell[1]])
    maze.set(cells_list[0][0], cells_list[0][1], "#")

    while len(cells_list) > 0:
        current_cell = cells_list[len(cells_list) - 1]
        if len(neighbors(current_cell)) > 0:
            random_neighbor = choice(neighbors(current_cell))
            maze.set(random_neighbor[0], random_neighbor[1], "#")
            create_passage(current_cell, random_neighbor)
            cells_list.append(random_neighbor)
        else:
            cells_list.remove(current_cell)
        get_events()
        handle_events(events)
        if wait:
            maze.draw(screen, tile_size)
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
                maze.save()
create()
while True:
    get_events()
    handle_events(events)
    maze.draw(screen, tile_size)
    pygame.time.wait(wait_time)
pygame.quit()
quit()
