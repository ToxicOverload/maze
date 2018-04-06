import pygame

# . is walls, # is nothing, @ is finish, & is start
maze = ["&.....####",
        "#####.#...",
        "#.#.#.####",
        "#.#.#.#..#",
        "#.#.####.#",
        "#...#.#..#",
        "#.###.##.#",
        "###......#",
        "..###.####",
        "###......@"]

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)

players = []
playing = True
events = []

class player():
    def __init__(self, x_coord, y_coord):
        global players
        
        self.x = x_coord
        self.y = y_coord
        players.append(self)

    def tick(self, board):
        global playing
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.y > 0:
                    if board[self.y-1][self.x] != ".":
                        self.y -= 1
                elif event.key == pygame.K_DOWN and self.y < len(board)-1:
                    if board[self.y+1][self.x] != ".":
                        self.y += 1
                if event.key == pygame.K_LEFT and self.x > 0:
                    if board[self.y][self.x-1] != ".":
                        self.x -= 1
                elif event.key == pygame.K_RIGHT and self.x < len(board[self.y])-1:
                    if board[self.y][self.x+1] != ".":
                        self.x += 1
        if board[self.y][self.x] == "@":
            playing = False
            print ("You win!")
            

def create_player():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "&":
                return player(x, y)

player = create_player()

def get_events():
    global events
    events = []
    for event in pygame.event.get():
        events.append(event)

def test_for_quit(events_list):
    global playing
    for event in events_list:
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                playing = False

def tick_players():
    for i in players:
        i.tick(maze)

def draw(board):
    screen.fill(white)
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == ".":
                pygame.draw.rect(screen, black, [y*50,x*50,50,50])
            elif board[x][y] == "@":
                pygame.draw.rect(screen, blue, [y*50,x*50,50,50])
    for i in range(len(players)):
        pygame.draw.rect(screen, green, [players[i].x*50, players[i].y*50, 50, 50])
    pygame.display.update()

pygame.init()
size = [len(maze)*50,len(maze[0])*50]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Fun!")

while playing == True:
    get_events()
    
    test_for_quit(events)

    tick_players()
    
    draw(maze)

pygame.quit()
quit()
