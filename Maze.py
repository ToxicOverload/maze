import os
import pygame

# Synonyms for yes
yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

# Some basic colors
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (100,100,100)
purple = (255,0,255)

class Maze:
    maze = []
    def __init__ (self, width=None, height=None):
        self.maze = []
        self.width = width
        self.height = height
        if width != None and height != None:
            for y in range(height):
                self.maze.append(list())
                for x in range(width):
                    self.maze[y].append("")
    def import_file (self, filename = None):
        """Import maze from a file"""
        if not os.path.exists("Mazes"):
            os.makedirs("Mazes")
        valid_mazes = [i.name for i in list(os.scandir("Mazes")) if i.is_file()]
        if len(valid_mazes) == 0:
            return False
        self.maze = []
        # Ask filename
        while filename not in valid_mazes:
            for i in valid_mazes:
                print(i)
            filename = input("File name: ")
        # Open the file
        with open(os.path.join("Mazes", filename), "r") as file:
            # Read the file as lines
            lines = file.readlines()
            # Read in dimensions
            self.width = int(lines[0].strip("\n").split("x")[0])
            self.height = int(lines[0].strip("\n").split("x")[1])
            # Set maze to the body lines and remove the strip lines
            for line in lines:
                self.maze.append(list(line.strip("\n")))
        return True
    def save (self, filename = None):
        """Save maze to file"""
        while len(filename) == 0:
            filename = input("Save file name: ")
        if not os.path.exists("Mazes"):
            os.makedirs("Mazes")
        with open(os.path.join("Mazes", filename), "w") as f:
            print(self.width, "x", self.height, sep="", file=f)
            for row in self.maze:
                for cell in row:
                    print(cell, file=f, end="")
                print("", file=f)
        return True
    def at (self, x, y):
        """Return value in maze"""
        if x < self.width and y < self.height:
            return self.maze[y][x]
        else:
            return False
    def set (self, x, y, value):
        """Set a value to maze"""
        if x < self.width and y < self.height:
            self.maze[y][x] = value
            return True
        else:
            return False
    def draw (self, screen, tile_size):
        if not type(screen) is pygame.Surface:
            return False
        screen.fill(white)
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) == ".":
                    pygame.draw.rect(screen, black, [x * tile_size, y * tile_size, tile_size, tile_size])
                elif self.at(x, y) == "@":
                    pygame.draw.rect(screen, blue, [x * tile_size, y * tile_size, tile_size, tile_size])
                elif self.at(x, y) == "&":
                    pygame.draw.rect(screen, purple, [x * tile_size, y * tile_size, tile_size, tile_size])
        pygame.display.update()
        return True
