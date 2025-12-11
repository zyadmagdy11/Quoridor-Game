# game_state.py

import copy
import pickle
from constants import *

class GameState:
    def __init__(self, board_size, player_count, ai_players):
        self.board_size = board_size
        self.player_count = player_count
        self.ai_players = ai_players
        
        # Initialize game state variables
        self.current_player = 1
        self.mode = None
        self.legal_moves = []
        self.history = []
        self.redo_stack = []
        self.game_over = False
        
        # Initialize walls based on board size
        self.horizontal_walls = [[False] * (board_size - 1) for _ in range(board_size - 1)]
        self.vertical_walls = [[False] * (board_size - 1) for _ in range(board_size - 1)]
        
        # Set initial positions and walls
        self.set_initial_positions()
        self.walls_remaining = self.get_initial_walls(player_count, board_size)
    
    def set_initial_positions(self):
        """Set initial positions based on board size and player count"""
        mid = self.board_size // 2
        self.initial_positions = {}
        self.player_positions = {}
        
        if self.player_count >= 2:
            # Player 1 (top) -> goal: bottom row
            self.initial_positions[1] = [0, mid]
            self.player_positions[1] = [0, mid]
            # Player 2 (bottom) -> goal: top row
            self.initial_positions[2] = [self.board_size - 1, mid]
            self.player_positions[2] = [self.board_size - 1, mid]
        
        if self.player_count >= 4:
            # Player 3 (left) -> goal: right column
            self.initial_positions[3] = [mid, 0]
            self.player_positions[3] = [mid, 0]
            # Player 4 (right) -> goal: left column
            self.initial_positions[4] = [mid, self.board_size - 1]
            self.player_positions[4] = [mid, self.board_size - 1]
    
    def get_initial_positions(self, player_count, board_size):
        """Get initial positions based on player count"""
        mid = board_size // 2
        positions = {}
        
        if player_count >= 2:
            positions[1] = [0, mid]  # Top
            positions[2] = [board_size - 1, mid]  # Bottom
        
        if player_count >= 4:
            positions[3] = [mid, 0]  # Left
            positions[4] = [mid, board_size - 1]  # Right
            
        return positions
    
    def get_initial_walls(self, player_count, board_size):
        """Get initial wall counts based on player count and board size"""
        # Base walls adjustment based on player count
        if player_count == 2:
            base_walls = 10
        elif player_count == 4:
            base_walls = 5
        else:
            base_walls = 10  # Default
        
        # Adjust based on board size
        if board_size <= 7:
            base_walls = max(3, base_walls - 2)
        elif board_size >= 11:
            base_walls = base_walls + 2
        
        walls = {}
        for player in range(1, player_count + 1):
            walls[player] = base_walls
        return walls
    
    def save_game_state(self):
        state = {
            "player_positions": copy.deepcopy(self.player_positions),
            "horizontal_walls": copy.deepcopy(self.horizontal_walls),
            "vertical_walls": copy.deepcopy(self.vertical_walls),
            "current_player": self.current_player,
            "walls_remaining": copy.deepcopy(self.walls_remaining),
            "mode": self.mode,
            "game_over": self.game_over,
            "board_size": self.board_size,
            "player_count": self.player_count
        }
        self.history.append(state)
        # Clear redo stack when new action is taken
        self.redo_stack.clear()
        return state
    
    def undo_action(self):
        if not self.history:
            return False
            
        # Save current state to redo stack before undoing
        current_state = {
            "player_positions": copy.deepcopy(self.player_positions),
            "horizontal_walls": copy.deepcopy(self.horizontal_walls),
            "vertical_walls": copy.deepcopy(self.vertical_walls),
            "current_player": self.current_player,
            "walls_remaining": copy.deepcopy(self.walls_remaining),
            "mode": self.mode,
            "game_over": self.game_over,
            "board_size": self.board_size,
            "player_count": self.player_count
        }
        self.redo_stack.append(current_state)
            
        state = self.history.pop()
        self.player_positions = state["player_positions"]
        self.horizontal_walls = state["horizontal_walls"]
        self.vertical_walls = state["vertical_walls"]
        self.current_player = state["current_player"]
        self.walls_remaining = state.get("walls_remaining", self.get_initial_walls(self.player_count, self.board_size))
        self.mode = None
        self.game_over = state.get("game_over", False)
        return True
    
    def redo_action(self):
        if not self.redo_stack:
            return False
            
        # Save current state to history before redoing
        current_state = {
            "player_positions": copy.deepcopy(self.player_positions),
            "horizontal_walls": copy.deepcopy(self.horizontal_walls),
            "vertical_walls": copy.deepcopy(self.vertical_walls),
            "current_player": self.current_player,
            "walls_remaining": copy.deepcopy(self.walls_remaining),
            "mode": self.mode,
            "game_over": self.game_over,
            "board_size": self.board_size,
            "player_count": self.player_count
        }
        self.history.append(current_state)
        
        state = self.redo_stack.pop()
        self.player_positions = state["player_positions"]
        self.horizontal_walls = state["horizontal_walls"]
        self.vertical_walls = state["vertical_walls"]
        self.current_player = state["current_player"]
        self.walls_remaining = state.get("walls_remaining", self.get_initial_walls(self.player_count, self.board_size))
        self.mode = None
        self.game_over = state.get("game_over", False)
        return True
    
    def save_to_file(self, filename):
        """Save complete game state to file"""
        state = {
            "player_positions": self.player_positions,
            "horizontal_walls": self.horizontal_walls,
            "vertical_walls": self.vertical_walls,
            "current_player": self.current_player,
            "walls_remaining": self.walls_remaining,
            "game_over": self.game_over,
            "board_size": self.board_size,
            "history": self.history,
            "redo_stack": self.redo_stack,
            "ai_players": self.ai_players,
            "player_count": self.player_count
        }
        with open(filename, 'wb') as f:
            pickle.dump(state, f)
    
    def load_from_file(self, filename):
        """Load complete game state from file"""
        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
            
            self.player_positions = state["player_positions"]
            self.horizontal_walls = state["horizontal_walls"]
            self.vertical_walls = state["vertical_walls"]
            self.current_player = state["current_player"]
            self.walls_remaining = state["walls_remaining"]
            self.game_over = state["game_over"]
            self.board_size = state["board_size"]
            self.history = state.get("history", [])
            self.redo_stack = state.get("redo_stack", [])
            self.ai_players = state.get("ai_players", {1: None, 2: None, 3: None, 4: None})
            self.player_count = state.get("player_count", 2)
            self.initial_positions = self.get_initial_positions(self.player_count, self.board_size)
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def switch_turn(self):
        print(f"Switching turn from player {self.current_player} to player {self.get_next_player()}")
        self.current_player = self.get_next_player()
    
    def get_next_player(self):
        """Get the next player in sequence, skipping players that don't exist"""
        next_player = self.current_player
        while True:
            next_player = next_player % self.player_count + 1
            if next_player in self.player_positions:
                return next_player
    
    def validate_turn(self, player):
        return self.current_player == player and not self.game_over
    
    def check_victory(self):
        """Check if any player has reached their goal"""
        if self.player_count == 2:
            # 2-player: reach opposite side
            row1, col1 = self.player_positions[1]
            row2, col2 = self.player_positions[2]
            if row1 == self.board_size - 1:
                return 1
            if row2 == 0:
                return 2
        elif self.player_count == 4:
            # 4-player: each has opposite side
            row1, col1 = self.player_positions[1]  # Top -> Bottom
            row2, col2 = self.player_positions[2]  # Bottom -> Top
            row3, col3 = self.player_positions[3]  # Left -> Right
            row4, col4 = self.player_positions[4]  # Right -> Left
            
            if row1 == self.board_size - 1:
                return 1
            if row2 == 0:
                return 2
            if col3 == self.board_size - 1:  # Left -> Right
                return 3
            if col4 == 0:  # Right -> Left
                return 4
        return None
    
    def other_player_at(self, row, col):
        for p, pos in self.player_positions.items():
            if pos == [row, col]:
                return p
        return None
    
    def reset_game(self, board_size=DEFAULT_BOARD_SIZE, player_count=2, ai_players=None):
        """Reset game to initial state"""
        self.board_size = board_size
        self.player_count = player_count
        self.current_player = 1
        self.mode = None
        self.legal_moves = []
        self.history = []
        self.redo_stack = []
        self.game_over = False
        self.ai_players = ai_players or {1: None, 2: None, 3: None, 4: None}
        
        self.initial_positions = self.get_initial_positions(player_count, board_size)
        self.player_positions = copy.deepcopy(self.initial_positions)
        
        self.horizontal_walls = [[False] * (board_size - 1) for _ in range(board_size - 1)]
        self.vertical_walls = [[False] * (board_size - 1) for _ in range(board_size - 1)]
        self.walls_remaining = self.get_initial_walls(player_count, board_size)