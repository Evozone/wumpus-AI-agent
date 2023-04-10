# Main file to run the Wumpus World game
# Uses tkinter for the GUI and pygame for the sound effects

import tkinter as tk
import pygame as pg
import time


class WumpusWorld(tk.Frame):
    # Constructor for the game instance

    def __init__(self, master=None):
        # Call the constructor of the parent class
        super(WumpusWorld, self).__init__(master)

        # Initialize the pygame mixer
        pg.mixer.init()

        # Denoting total moves made by the player
        self.moves = 0

        # Denoting the current score of the player
        self.score = 0

        self.canvasWidth = 800
        self.canvasHeight = 600

        # Create the canvas
        self.canvas = tk.Canvas(
            self, width=self.canvasWidth, height=self.canvasHeight, bg="black")

        # Pack the canvas
        self.canvas.pack()
        self.pack()

        # Create the game board
        self.createGameBoard()

    def createGameBoard(self):
        # Create the game board using rectangles
        for row in range(4):
            for col in range(4):
                x1 = (col * 100) + 200
                y1 = (row * 100) + 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill='white', outline='black')

    def gameLoop(self):
        # Game loop
        while True:
            # Update the canvas with the current state of the game
            self.canvas.update()

            # Wait for some time before updating the canvas again
            time.sleep(0.01)


if __name__ == "__main__":
    # Create a new Frame
    root = tk.Tk()

    # Set the title of the window
    root.title("Wumpus World")

    # Create a new instance of the game
    game = WumpusWorld(master=root)

    # Start the game loop
    game.gameLoop()
