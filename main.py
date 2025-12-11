# main.py

import tkinter as tk
from start_screen import StartScreen
from gui import QuoridorGUI

def show_start_screen():
    """Show the start screen"""
    root = tk.Tk()
    start_screen = StartScreen(root, start_game)
    root.mainloop()

def start_game(board_size, player_count, ai_settings):
    """Start the game with the selected settings"""
    # Close the start screen and start the main game
    root = tk.Tk()
    
    # Start the main game
    app = QuoridorGUI(root, board_size, player_count, ai_settings)
    
    root.mainloop()

if __name__ == "__main__":
    show_start_screen()