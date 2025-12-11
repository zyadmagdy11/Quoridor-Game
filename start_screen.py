import tkinter as tk
from tkinter import ttk
from constants import *

class StartScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Quoridor Game - Setup")
        self.root.configure(bg=START_SCREEN_BG)
        self.root.geometry("500x700")  # Increased size to ensure everything fits
        self.root.resizable(False, False)

        # Create a main frame with scrollbar to ensure everything fits
        main_frame = tk.Frame(self.root, bg=START_SCREEN_BG)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a canvas for scrolling if needed
        canvas = tk.Canvas(main_frame, bg=START_SCREEN_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=START_SCREEN_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        title_label = tk.Label(
            scrollable_frame, 
            text="Quoridor Game", 
            font=("Arial", 20, "bold"),
            bg=START_SCREEN_BG
        )
        title_label.pack(pady=20)
        
        player_frame = tk.LabelFrame(
            scrollable_frame, 
            text="Number of Players",
            font=("Arial", 12, "bold"),
            bg=START_SCREEN_BG,
            padx=10,
            pady=10,
            labelanchor="nw"
        )
        player_frame.pack(fill="x", pady=10)
        
        self.player_count = tk.IntVar(value=2)
        
        tk.Radiobutton(
            player_frame, text="2 Players", variable=self.player_count,
            value=2, font=("Arial", 10), bg=START_SCREEN_BG,
            command=self.on_player_count_change
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            player_frame, text="4 Players", variable=self.player_count,
            value=4, font=("Arial", 10), bg=START_SCREEN_BG,
            command=self.on_player_count_change
        ).pack(anchor="w", pady=5)
        
        mode_frame = tk.LabelFrame(
            scrollable_frame, 
            text="Game Mode",
            font=("Arial", 12, "bold"),
            bg=START_SCREEN_BG,
            padx=10,
            pady=10,
            labelanchor="nw"
        )
        mode_frame.pack(fill="x", pady=10)
        
        self.game_mode = tk.StringVar(value="human_human")
        
        tk.Radiobutton(
            mode_frame, text="Human vs Human", variable=self.game_mode,
            value="human_human", font=("Arial", 10), bg=START_SCREEN_BG,
            command=self.on_mode_change
        ).pack(anchor="w", pady=5)
        
        self.ai_mode_rb = tk.Radiobutton(
            mode_frame, text="Human vs AI", variable=self.game_mode,
            value="human_ai", font=("Arial", 10), bg=START_SCREEN_BG,
            command=self.on_mode_change
        )
        self.ai_mode_rb.pack(anchor="w", pady=5)
        
        self.ai_frame = tk.LabelFrame(
            scrollable_frame, 
            text="AI Settings",
            font=("Arial", 12, "bold"),
            bg=START_SCREEN_BG,
            padx=10,
            pady=10,
            labelanchor="nw"
        )

        ai_diff_frame = tk.Frame(self.ai_frame, bg=START_SCREEN_BG)
        ai_diff_frame.pack(fill="x", pady=5)
        
        tk.Label(
            ai_diff_frame, text="AI Difficulty:", font=("Arial", 10),
            bg=START_SCREEN_BG, width=12, anchor="w"
        ).pack(side="left")
        
        self.ai_difficulty = tk.StringVar(value="medium")
        ai_combo = ttk.Combobox(
            ai_diff_frame, textvariable=self.ai_difficulty,
            values=["easy", "medium", "hard"], state="readonly",
            width=15
        )
        ai_combo.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # AI Level Indicators
        ai_levels_frame = tk.Frame(self.ai_frame, bg=START_SCREEN_BG)
        ai_levels_frame.pack(fill="x", pady=8)
        
        tk.Label(ai_levels_frame, text="AI Level Descriptions:", 
                font=("Arial", 9, "bold"), bg=START_SCREEN_BG).pack(anchor="w", pady=(5, 8))
        
        # Easy Level
        easy_frame = tk.Frame(ai_levels_frame, bg=START_SCREEN_BG)
        easy_frame.pack(fill="x", pady=1)
        tk.Label(easy_frame, text="• Easy", font=("Arial", 9, "bold"), 
                bg=START_SCREEN_BG, width=8, anchor="w", fg="darkgreen").pack(side="left")
        tk.Label(easy_frame, text="Random moves", 
                font=("Arial", 8), bg=START_SCREEN_BG, fg="darkgreen").pack(side="left")
        
        # Medium Level
        medium_frame = tk.Frame(ai_levels_frame, bg=START_SCREEN_BG)
        medium_frame.pack(fill="x", pady=1)
        tk.Label(medium_frame, text="• Medium", font=("Arial", 9, "bold"), 
                bg=START_SCREEN_BG, width=8, anchor="w", fg="darkblue").pack(side="left")
        tk.Label(medium_frame, text="Basic strategy", 
                font=("Arial", 8), bg=START_SCREEN_BG, fg="darkblue").pack(side="left")
        
        # Hard Level
        hard_frame = tk.Frame(ai_levels_frame, bg=START_SCREEN_BG)
        hard_frame.pack(fill="x", pady=1)
        tk.Label(hard_frame, text="• Hard", font=("Arial", 9, "bold"), 
                bg=START_SCREEN_BG, width=8, anchor="w", fg="darkred").pack(side="left")
        tk.Label(hard_frame, text="Advanced blocking", 
                font=("Arial", 8), bg=START_SCREEN_BG, fg="darkred").pack(side="left")
        
        note_label = tk.Label(
            self.ai_frame, text="Note: AI only available in 2-player mode",
            font=("Arial", 9), bg=START_SCREEN_BG, fg="blue"
        )
        note_label.pack(pady=8)
        
        # Board Size Frame with Slider
        self.size_frame = tk.LabelFrame(
            scrollable_frame, 
            text="Board Size",
            font=("Arial", 12, "bold"),
            bg=START_SCREEN_BG,
            padx=10,
            pady=10,
            labelanchor="nw"
        )
        self.size_frame.pack(fill="x", pady=10)
        
        tk.Label(
            self.size_frame, text="Select board size (5-12):",
            font=("Arial", 10), bg=START_SCREEN_BG
        ).pack(anchor="w")
        
        self.board_size = tk.IntVar(value=DEFAULT_BOARD_SIZE)
        
        # Current size display
        value_frame = tk.Frame(self.size_frame, bg=START_SCREEN_BG)
        value_frame.pack(fill="x", pady=5)
        
        self.size_value_label = tk.Label(
            value_frame, text=str(DEFAULT_BOARD_SIZE),
            font=("Arial", 12, "bold"), bg=START_SCREEN_BG
        )
        self.size_value_label.pack()
        
        # Slider for board size
        size_slider_frame = tk.Frame(self.size_frame, bg=START_SCREEN_BG)
        size_slider_frame.pack(fill="x", pady=10)
        
        # Minimum value label
        tk.Label(size_slider_frame, text="5", font=("Arial", 9), 
                bg=START_SCREEN_BG).pack(side="left")
        
        # The actual slider
        size_slider = tk.Scale(
            size_slider_frame, 
            from_=MIN_BOARD_SIZE, 
            to=MAX_BOARD_SIZE,
            orient="horizontal",
            variable=self.board_size,
            length=300,
            bg=START_SCREEN_BG,
            highlightthickness=0,
            showvalue=0,  # Don't show value on slider
            command=self.on_board_size_change
        )
        size_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Maximum value label
        tk.Label(size_slider_frame, text="12", font=("Arial", 9), 
                bg=START_SCREEN_BG).pack(side="right")
        
        # Start Button - placed in its own frame to ensure visibility
        button_frame = tk.Frame(scrollable_frame, bg=START_SCREEN_BG)
        button_frame.pack(fill="x", pady=20)
        
        start_button = tk.Button(
            button_frame, 
            text="Start Game", 
            font=("Arial", 14, "bold"),
            bg="#4CAF50", 
            fg="white", 
            padx=30, 
            pady=12,
            command=self.start_game
        )
        start_button.pack(pady=10)

        # Initialize UI state
        self.ai_frame.pack_forget()
        self.on_player_count_change()
        self.on_mode_change()
        
        # Update scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def on_board_size_change(self, value):
        self.size_value_label.config(text=str(int(float(value))))
    
    def on_player_count_change(self):
        player_count = self.player_count.get()
        
        if player_count == 4:
            self.game_mode.set("human_human")
            self.ai_mode_rb.config(state="disabled")
            self.ai_frame.pack_forget()
        else:
            self.ai_mode_rb.config(state="normal")
            self.on_mode_change()
    
    def on_mode_change(self):
        mode = self.game_mode.get()
        
        if mode == "human_human":
            self.ai_frame.pack_forget()
        else:
            # Pack AI frame before size frame
            self.ai_frame.pack(fill="x", pady=10, before=self.size_frame)
    
    def start_game(self):
        mode = self.game_mode.get()
        board_size = self.board_size.get()
        player_count = self.player_count.get()
        
        if mode == "human_human" or player_count == 4:
            ai_settings = {1: None, 2: None, 3: None, 4: None}
        else:
            ai_settings = {1: None, 2: self.ai_difficulty.get(), 3: None, 4: None}
        
        self.callback(board_size, player_count, ai_settings)