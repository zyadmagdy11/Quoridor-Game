# gui.py

import tkinter as tk
from tkinter import messagebox
from constants import *
from game_state import GameState
from movement import Movement
from wall_placement import WallPlacement
from pathfinding import Pathfinding
from ai import QuoridorAI

class QuoridorGUI:
    def __init__(self, root, board_size, player_count, ai_players):
        self.root = root
        self.root.title("Quoridor Game")
        
        # Initialize game components with settings from start screen
        self.game_state = GameState(board_size, player_count, ai_players)
        self.movement = Movement(self.game_state)
        self.wall_placement = WallPlacement(self.game_state)
        self.pathfinding = Pathfinding(self.game_state)
        
        self.setup_ui()
        self.bind_events()
        self.update_display()
        
        # Single AI check after a short delay
        self.root.after(500, self.check_ai_move)
    
    def setup_ui(self):
        # Configure root window
        self.root.geometry("900x900")  # Increased width to accommodate larger controls
        
        # Create main frames for two halves
        self.top_frame = tk.Frame(self.root, bg="#DDDDDD")
        self.top_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.bottom_frame = tk.Frame(self.root, bg="#EEEEEE")
        self.bottom_frame.pack(fill="x", padx=10, pady=5)
        
        # Setup canvas in top frame
        self.setup_canvas()
        
        # Setup control panel in bottom frame with three columns
        self.setup_control_panel()
    
    def setup_canvas(self):
        canvas_size = (CELL_SIZE + GAP_SIZE) * self.game_state.board_size + PADDING * 2 - GAP_SIZE
        self.canvas = tk.Canvas(
            self.top_frame, 
            width=canvas_size, 
            height=canvas_size, 
            bg="#DDDDDD",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack(expand=True)
    
    def setup_control_panel(self):
        # Create three columns in bottom frame with adjusted widths
        self.player_controls_frame = tk.LabelFrame(self.bottom_frame, text="Player Controls", 
                                                 font=("Arial", 10, "bold"), bg="#EEEEEE", 
                                                 padx=10, pady=10, width=350)  # Increased width
        self.player_controls_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        
        self.game_controls_frame = tk.LabelFrame(self.bottom_frame, text="Game Controls", 
                                               font=("Arial", 10, "bold"), bg="#EEEEEE",
                                               padx=10, pady=10, width=200)
        self.game_controls_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        
        self.info_frame = tk.LabelFrame(self.bottom_frame, text="Game Information", 
                                      font=("Arial", 10, "bold"), bg="#EEEEEE",
                                      padx=10, pady=10, width=250)  # Reduced width
        self.info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Setup each section
        self.setup_player_controls()
        self.setup_game_controls()
        self.setup_info_display()
    
    def setup_player_controls(self):
        # Make the player controls more compact and use grid for 4 players
        player_colors = {
            1: PLAYER1_COLOR,
            2: PLAYER2_COLOR, 
            3: PLAYER3_COLOR,
            4: PLAYER4_COLOR
        }
        
        # Create a grid layout for player buttons
        if self.game_state.player_count == 4:
            # 2x2 grid for 4 players
            for i, player in enumerate(range(1, self.game_state.player_count + 1)):
                color = player_colors[player]
                
                # Calculate row and column for grid (2x2)
                row = i // 2
                col = i % 2
                
                # Player frame
                player_frame = tk.Frame(self.player_controls_frame, bg="#EEEEEE", relief="solid", bd=1)
                player_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                # Configure grid weights for expansion
                self.player_controls_frame.grid_rowconfigure(row, weight=1)
                self.player_controls_frame.grid_columnconfigure(col, weight=1)
                
                # Player label with color indicator
                label_frame = tk.Frame(player_frame, bg="#EEEEEE")
                label_frame.pack(fill="x", pady=2)
                
                # Color indicator
                color_indicator = tk.Frame(label_frame, bg=color, width=15, height=15)
                color_indicator.pack(side="left", padx=(0, 5))
                
                tk.Label(label_frame, text=f"Player {player}", font=("Arial", 9, "bold"), 
                        bg="#EEEEEE").pack(side="left")
                
                # Action buttons in a single row with spacing
                button_frame = tk.Frame(player_frame, bg="#EEEEEE")
                button_frame.pack(fill="x", pady=2)
                
                tk.Button(button_frame, text="Move", font=("Arial", 8),
                         command=lambda p=player: self.start_move_mode(p),
                         width=6, height=1).pack(side="left", padx=1)
                tk.Button(button_frame, text="H Wall", font=("Arial", 8),
                         command=lambda p=player: self.set_wall_mode(p, 'H'),
                         width=6, height=1).pack(side="left", padx=1)
                tk.Button(button_frame, text="V Wall", font=("Arial", 8),
                         command=lambda p=player: self.set_wall_mode(p, 'V'),
                         width=6, height=1).pack(side="left", padx=1)
        else:
            # Vertical layout for 2 players
            for player in range(1, self.game_state.player_count + 1):
                color = player_colors[player]
                
                # Player frame
                player_frame = tk.Frame(self.player_controls_frame, bg="#EEEEEE")
                player_frame.pack(fill="x", pady=3)
                
                # Player label with color indicator
                label_frame = tk.Frame(player_frame, bg="#EEEEEE")
                label_frame.pack(fill="x", pady=2)
                
                # Color indicator
                color_indicator = tk.Frame(label_frame, bg=color, width=15, height=15)
                color_indicator.pack(side="left", padx=(0, 5))
                
                tk.Label(label_frame, text=f"Player {player}", font=("Arial", 9, "bold"), 
                        bg="#EEEEEE").pack(side="left")
                
                # Action buttons in a single row with spacing
                button_frame = tk.Frame(player_frame, bg="#EEEEEE")
                button_frame.pack(fill="x", pady=2)
                
                tk.Button(button_frame, text="Move", font=("Arial", 8),
                         command=lambda p=player: self.start_move_mode(p),
                         width=6, height=1).pack(side="left", padx=2)
                tk.Button(button_frame, text="H Wall", font=("Arial", 8),
                         command=lambda p=player: self.set_wall_mode(p, 'H'),
                         width=6, height=1).pack(side="left", padx=2)
                tk.Button(button_frame, text="V Wall", font=("Arial", 8),
                         command=lambda p=player: self.set_wall_mode(p, 'V'),
                         width=6, height=1).pack(side="left", padx=2)
    
    def setup_game_controls(self):
        # Action buttons in two rows
        action_row1 = tk.Frame(self.game_controls_frame, bg="#EEEEEE")
        action_row1.pack(fill="x", pady=3)
        
        tk.Button(action_row1, text="Undo", command=self.undo_action, 
                 bg=BUTTON_BG, font=("Arial", 9), width=8).pack(side="left", padx=2)
        tk.Button(action_row1, text="Redo", command=self.redo_action, 
                 bg=BUTTON_BG, font=("Arial", 9), width=8).pack(side="left", padx=2)
        tk.Button(action_row1, text="New Game", command=self.new_game, 
                 bg="#FFFFCC", font=("Arial", 9), width=10).pack(side="left", padx=2)
        
        action_row2 = tk.Frame(self.game_controls_frame, bg="#EEEEEE")
        action_row2.pack(fill="x", pady=3)
        
        tk.Button(action_row2, text="Save Game", command=self.save_game, 
                 bg="#CCCCFF", font=("Arial", 9), width=12).pack(side="left", padx=2)
        tk.Button(action_row2, text="Load Game", command=self.load_game, 
                 bg="#FFCCCC", font=("Arial", 9), width=12).pack(side="left", padx=2)
    
    def setup_info_display(self):
        # Main game information
        self.info_label = tk.Label(self.info_frame, text="", font=("Arial", 9), 
                                 bg="#EEEEEE", wraplength=230, justify="left", anchor="w")
        self.info_label.pack(fill="x", pady=2)
        
        # AI status
        self.ai_status_label = tk.Label(self.info_frame, text="", font=("Arial", 8), 
                                      bg="#EEEEEE", justify="left", anchor="w")
        self.ai_status_label.pack(fill="x", pady=2)
        
        self.update_ai_status()
    
    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_canvas_click)
    
    def update_display(self):
        self.draw_board()
        self.draw_pawns()
        self.draw_initial_positions()
        self.update_info()
    
    def draw_board(self):
        self.canvas.delete("cell")
        self.canvas.delete("wall")
        board_size = self.game_state.board_size
        for row in range(board_size):
            for col in range(board_size):
                x1 = PADDING + col * (CELL_SIZE + GAP_SIZE)
                y1 = PADDING + row * (CELL_SIZE + GAP_SIZE)
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=BOARD_COLOR, outline=LINE_COLOR, width=2, tags="cell")
        self.draw_walls()
    
    def draw_walls(self):
        board_size = self.game_state.board_size
        for row in range(board_size - 1):
            for col in range(board_size - 1):
                if self.game_state.horizontal_walls[row][col]:
                    self.draw_horizontal_wall(row, col)
                if self.game_state.vertical_walls[row][col]:
                    self.draw_vertical_wall(row, col)
    
    def draw_horizontal_wall(self, row, col):
        x1 = PADDING + col * (CELL_SIZE + GAP_SIZE)
        y1 = PADDING + (row + 1) * CELL_SIZE + row * GAP_SIZE
        x2 = x1 + 2 * CELL_SIZE + GAP_SIZE
        y2 = y1 + GAP_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, width=0, tags="wall")
    
    def draw_vertical_wall(self, row, col):
        x1 = PADDING + (col + 1) * CELL_SIZE + col * GAP_SIZE
        y1 = PADDING + row * (CELL_SIZE + GAP_SIZE)
        x2 = x1 + GAP_SIZE
        y2 = y1 + 2 * CELL_SIZE + GAP_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, width=0, tags="wall")
    
    def draw_pawns(self):
        self.canvas.delete("pawn")
        player_colors = {
            1: PLAYER1_COLOR,
            2: PLAYER2_COLOR,
            3: PLAYER3_COLOR,
            4: PLAYER4_COLOR
        }
        
        for player, (row, col) in self.game_state.player_positions.items():
            color = player_colors[player]
            x1 = PADDING + col * (CELL_SIZE + GAP_SIZE) + 10
            y1 = PADDING + row * (CELL_SIZE + GAP_SIZE) + 10
            x2 = x1 + CELL_SIZE - 20
            y2 = y1 + CELL_SIZE - 20
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags="pawn")
    
    def draw_initial_positions(self):
        """Draw empty circles to indicate initial positions"""
        self.canvas.delete("initial_position")
        player_colors = {
            1: PLAYER1_COLOR,
            2: PLAYER2_COLOR,
            3: PLAYER3_COLOR,
            4: PLAYER4_COLOR
        }
        
        for player, (row, col) in self.game_state.initial_positions.items():
            color = player_colors[player]
            x1 = PADDING + col * (CELL_SIZE + GAP_SIZE) + 15
            y1 = PADDING + row * (CELL_SIZE + GAP_SIZE) + 15
            x2 = x1 + CELL_SIZE - 30
            y2 = y1 + CELL_SIZE - 30
            self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=2, tags="initial_position")
    
    def update_ai_status(self):
        """Update AI status display"""
        status_text = "Game Mode:\n"
        for player in range(1, self.game_state.player_count + 1):
            ai_type = self.game_state.ai_players[player]
            if ai_type:
                status_text += f"P{player}: AI ({ai_type})\n"
            else:
                status_text += f"P{player}: Human\n"
        
        self.ai_status_label.config(text=status_text)
    
    def start_move_mode(self, player):
        if not self.game_state.validate_turn(player):
            self.info_label.config(text="Not your turn")
            return
            
        self.game_state.mode = "move"
        self.game_state.legal_moves = self.movement.get_legal_moves(player)
        if not self.game_state.legal_moves:
            self.info_label.config(text=f"Player {player}: no legal moves")
            return
        self.highlight_legal_moves()
        self.info_label.config(text=f"Player {player}: choose move")
    
    def set_wall_mode(self, player, wall_type):
        if not self.game_state.validate_turn(player):
            self.info_label.config(text="Not your turn")
            return
            
        if self.game_state.walls_remaining[player] <= 0:
            self.info_label.config(text="No walls remaining")
            return
            
        self.game_state.mode = f"{wall_type}_wall"
        self.canvas.delete("highlight")
        self.info_label.config(text=f"Player {player}: click to preview {wall_type} wall")
    
    def check_ai_move(self):
        """Check if current player is AI and make move if so"""
        if self.game_state.game_over:
            return
            
        current_player = self.game_state.current_player
        ai_difficulty = self.game_state.ai_players[current_player]
        
        # Debug info
        print(f"Checking AI move: Player {current_player}, AI: {ai_difficulty}, Mode: {self.game_state.mode}")
        
        if ai_difficulty and not self.game_state.mode:
            try:
                # AI's turn - make a move after a short delay
                self.info_label.config(text=f"AI Player {current_player} thinking...")
                print(f"Scheduling AI move for player {current_player} with difficulty {ai_difficulty}")
                self.root.after(800, self.make_ai_move, current_player, ai_difficulty)
            except Exception as e:
                print(f"Error in AI move: {e}")
                self.info_label.config(text=f"AI error: {str(e)}")
                self.game_state.switch_turn()
                self.update_display()

    def make_ai_move(self, player, difficulty):
        """Execute AI move"""
        print(f"Executing AI move for player {player} with difficulty {difficulty}")
        
        # Ensure it's still the AI's turn
        if self.game_state.current_player != player:
            print(f"Not AI's turn anymore. Current player: {self.game_state.current_player}")
            return
            
        try:
            ai = QuoridorAI(self.game_state, difficulty)
            move = ai.get_move()
            
            if not move:
                self.info_label.config(text=f"AI Player {player} has no valid moves")
                print(f"AI found no valid moves")
                return
            
            move_type, move_data = move
            print(f"AI decided: {move_type} at {move_data}")
            
            self.game_state.save_game_state()
            
            if move_type == "move":
                row, col = move_data
                self.game_state.player_positions[player] = [row, col]
                
                winner = self.game_state.check_victory()
                if winner:
                    self.handle_game_over(winner)
                    return
                    
                self.game_state.switch_turn()
                self.update_display()
                
            elif move_type == "wall":
                row, col, horizontal = move_data
                success, message = self.wall_placement.place_wall(row, col, horizontal, self.pathfinding)
                
                if success:
                    self.game_state.switch_turn()
                    self.update_display()
                else:
                    # If wall placement failed, try a move instead
                    print(f"AI wall placement failed: {message}, trying move instead")
                    legal_moves = self.movement.get_legal_moves(player)
                    if legal_moves:
                        row, col = legal_moves[0]  # Pick first legal move
                        self.game_state.player_positions[player] = [row, col]
                        self.game_state.switch_turn()
                        self.update_display()
                    else:
                        self.info_label.config(text="AI has no legal moves")
                        print("AI has no legal moves after failed wall placement")
        except Exception as e:
            print(f"Error during AI move execution: {e}")
            self.info_label.config(text=f"AI move error: {str(e)}")
            # Force switch turn to prevent game lock
            self.game_state.switch_turn()
            self.update_display()
    
    def handle_game_over(self, winner):
        self.game_state.game_over = True
        self.game_state.mode = None
        self.canvas.delete("highlight")
        self.update_display()
        
        # Show victory message
        player_colors = {
            1: "Blue", 2: "Red", 3: "Green", 4: "Purple"
        }
        
        if self.game_state.ai_players[winner]:
            message = f"Game Over! AI Player {winner} ({player_colors[winner]}) wins!"
        else:
            message = f"Game Over! Player {winner} ({player_colors[winner]}) wins!"
        
        self.info_label.config(text=message)
        messagebox.showinfo("Game Over", message)
    
    def highlight_legal_moves(self):
        self.canvas.delete("highlight")
        for row, col in self.game_state.legal_moves:
            x1 = PADDING + col * (CELL_SIZE + GAP_SIZE)
            y1 = PADDING + row * (CELL_SIZE + GAP_SIZE)
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=HIGHLIGHT_COLOR, width=4, tags="highlight")
    
    def on_canvas_click(self, event):
        if self.game_state.game_over:
            return
            
        # Don't process human clicks if current player is AI
        current_player = self.game_state.current_player
        if self.game_state.ai_players[current_player]:
            return
            
        col = (event.x - PADDING) // (CELL_SIZE + GAP_SIZE)
        row = (event.y - PADDING) // (CELL_SIZE + GAP_SIZE)
        
        board_size = self.game_state.board_size
        if not (0 <= row < board_size and 0 <= col < board_size):
            return
            
        if self.game_state.mode == "move":
            self.handle_move_click(row, col)
        elif self.game_state.mode in ["H_wall", "V_wall"]:
            self.preview_wall(row, col)
    
    def handle_move_click(self, row, col):
        if (row, col) not in self.game_state.legal_moves:
            self.info_label.config(text="Illegal move")
            return
            
        self.game_state.save_game_state()
        self.game_state.player_positions[self.game_state.current_player] = [row, col]
        
        winner = self.game_state.check_victory()
        if winner:
            self.handle_game_over(winner)
            return

        self.game_state.switch_turn()
        self.game_state.mode = None
        self.canvas.delete("highlight")
        self.update_display()
        # Check if next player is AI
        self.root.after(500, self.check_ai_move)
    
    def preview_wall(self, row, col):
        board_size = self.game_state.board_size
        wr = min(max(row, 0), board_size-2)
        wc = min(max(col, 0), board_size-2)
        self.canvas.delete("highlight")
        horizontal = (self.game_state.mode == "H_wall")
        self.draw_wall_preview(wr, wc, horizontal=horizontal)
        
        def confirm_place(e):
            self.place_wall(wr, wc)
            
        self.canvas.unbind("<Button-3>")
        self.canvas.bind("<Button-3>", confirm_place)
        self.info_label.config(text="Right-click to confirm wall")
    
    def draw_wall_preview(self, row, col, horizontal=True):
        if horizontal:
            x1 = PADDING + col * (CELL_SIZE + GAP_SIZE)
            y1 = PADDING + (row + 1) * CELL_SIZE + row * GAP_SIZE
            x2 = x1 + 2 * CELL_SIZE + GAP_SIZE
            y2 = y1 + GAP_SIZE
        else:
            x1 = PADDING + (col + 1) * CELL_SIZE + col * GAP_SIZE
            y1 = PADDING + row * (CELL_SIZE + GAP_SIZE)
            x2 = x1 + GAP_SIZE
            y2 = y1 + 2 * CELL_SIZE + GAP_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_PREVIEW_COLOR, width=0, tags="highlight")
    
    def place_wall(self, row, col):
        self.game_state.save_game_state()
        horizontal = (self.game_state.mode == "H_wall")
        success, message = self.wall_placement.place_wall(row, col, horizontal, self.pathfinding)
        
        if not success:
            self.info_label.config(text=message)
            self.canvas.delete("highlight")
            self.canvas.unbind("<Button-3>")
            self.game_state.mode = None
            return
            
        self.game_state.switch_turn()
        self.game_state.mode = None
        self.canvas.delete("highlight")
        self.update_display()
        self.canvas.unbind("<Button-3>")
        # Check if next player is AI
        self.root.after(500, self.check_ai_move)
    
    def undo_action(self):
        if self.game_state.undo_action():
            self.canvas.delete("highlight")
            self.update_display()
            if self.game_state.mode == "move":
                self.game_state.legal_moves = self.movement.get_legal_moves(self.game_state.current_player)
                self.highlight_legal_moves()
        else:
            self.info_label.config(text="No action to undo")
    
    def redo_action(self):
        if self.game_state.redo_action():
            self.canvas.delete("highlight")
            self.update_display()
            if self.game_state.mode == "move":
                self.game_state.legal_moves = self.movement.get_legal_moves(self.game_state.current_player)
                self.highlight_legal_moves()
        else:
            self.info_label.config(text="No action to redo")
    
    def save_game(self):
        """Save current game state to file"""
        filename = "quoridor_save.pkl"
        self.game_state.save_to_file(filename)
        self.info_label.config(text="Game saved successfully!")
    
    def load_game(self):
        """Load game state from file"""
        filename = "quoridor_save.pkl"
        if self.game_state.load_from_file(filename):
            # Reinitialize components with new game state
            self.movement = Movement(self.game_state)
            self.wall_placement = WallPlacement(self.game_state)
            self.pathfinding = Pathfinding(self.game_state)
            
            # Update canvas size for potentially different board size
            canvas_size = (CELL_SIZE + GAP_SIZE) * self.game_state.board_size + PADDING * 2 - GAP_SIZE
            self.canvas.config(width=canvas_size, height=canvas_size)
            
            self.update_display()
            self.info_label.config(text="Game loaded successfully!")
        else:
            self.info_label.config(text="Error loading game file")
    
    def new_game(self):
        """Return to start screen for new game"""
        from main import show_start_screen
        self.root.destroy()
        show_start_screen()
    
    def update_info(self):
        if self.game_state.game_over:
            return
        
        player = self.game_state.current_player
        player_type = "AI" if self.game_state.ai_players[player] else "Human"
        
        # Build walls info string
        walls_info = "Walls: "
        for p in range(1, self.game_state.player_count + 1):
            color = ["Blue", "Red", "Green", "Purple"][p-1]
            walls_info += f"P{p}({color}):{self.game_state.walls_remaining[p]} "
        
        self.info_label.config(
            text=f"Player {player}'s turn ({player_type})\n{walls_info}"
        )