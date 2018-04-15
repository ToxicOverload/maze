import os
import re

# Synonyms for yes
yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

# Some basic colors
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (100,100,100)
purple = (255,0,255)

# Import a maze from a file
def import_maze (filename = None):

    # Init variable
    maze = []

    if not os.path.exists("Mazes"):
        os.makedirs("Mazes")
    os.chdir("Mazes")

    valid_mazes = [i.name for i in list(os.scandir()) if i.is_file()]

    # Ask filename
    while filename not in valid_mazes:
        for i in valid_mazes:
            print(i)
        filename = input("File name: ")

    # Open the file
    with open(filename, "r") as file:
            # Read the file as lines
            lines = file.readlines()

            # Remove header line
            lines.pop(0)

            # Set maze to the body lines and remove the \n at the end of each line
            for line in lines:
                line = line.strip("\n")
                row = line.split(",")
                maze.append(row)
    return maze

def save_maze(board):
    save_name = ""
    while len(save_name) == 0:
        save_name = input("Save file name: ")
    os.makedirs("Mazes", exist_ok=True)
    os.chdir("Mazes")

    with open(save_name, "w") as f:
        print("width: ", len(board), file=f)
        for row in board:
            print(str(row).translate(str.maketrans("","","[]' ")), file=f)
    return True
