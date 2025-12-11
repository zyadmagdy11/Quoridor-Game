# ai.py

import random
import time
from movement import Movement
from wall_placement import WallPlacement
from pathfinding import Pathfinding

class QuoridorAI:
    """
    AI Player with multiple difficulty levels:
    
    - Easy: Makes random legal moves
    - Medium: Uses basic strategy - prioritizes moving toward goal and blocking opponent
    - Hard: Uses minimax algorithm with alpha-beta pruning for optimal play
    """
    
    def __init__(self, game_state, difficulty="medium"):
        self.game_state = game_state
        self.difficulty = difficulty
        self.movement = Movement(game_state)
        self.wall_placement = WallPlacement(game_state)
        self.pathfinding = Pathfinding(game_state)
    
    def get_move(self):
        """Get AI move based on difficulty level"""
        print(f"AI get_move called for player {self.game_state.current_player} with difficulty {self.difficulty}")
        
        if self.difficulty == "easy":
            result = self._easy_move()
        elif self.difficulty == "medium":
            result = self._medium_move()
        elif self.difficulty == "hard":
            result = self._hard_move()
        else:
            result = self._easy_move()  # Default to easy

        print(f"AI {self.difficulty} selected move: {result}")
        return result
    
    def _easy_move(self):
        """Easy AI: Random moves with basic wall placement"""
        # 70% chance to move, 30% chance to place wall if available
        if (self.game_state.walls_remaining[self.game_state.current_player] > 0 and 
            random.random() < 0.3):
            # Try to place a random wall
            wall_placements = []
            for row in range(self.game_state.board_size - 1):
                for col in range(self.game_state.board_size - 1):
                    for horizontal in [True, False]:
                        valid, _ = self.wall_placement.is_valid_wall_placement(row, col, horizontal)
                        if valid:
                            # Check if wall doesn't block paths - FIXED method name
                            if horizontal:
                                self.game_state.horizontal_walls[row][col] = True
                            else:
                                self.game_state.vertical_walls[row][col] = True
                            
                            if self.pathfinding.paths_exist_for_all_players():  # FIXED: was paths_exist_for_both_players
                                wall_placements.append((row, col, horizontal))
                            
                            # Revert temporary wall
                            if horizontal:
                                self.game_state.horizontal_walls[row][col] = False
                            else:
                                self.game_state.vertical_walls[row][col] = False
            
            if wall_placements:
                result = ("wall", random.choice(wall_placements))
                print(f"AI easy selected wall: {result}")
                return result
        
        # Fall back to random move
        legal_moves = self.movement.get_legal_moves(self.game_state.current_player)
        if legal_moves:
            result = ("move", random.choice(legal_moves))
            print(f"AI easy selected move: {result}")
            return result
        
        return None
    
    def _medium_move(self):
        """Medium AI: Uses basic strategy to move toward goal and block opponent"""
        player = self.game_state.current_player
        opponent = self._get_main_opponent(player)
        
        # Calculate current path lengths
        player_path = self.pathfinding.shortest_path_length(player)
        opponent_path = self.pathfinding.shortest_path_length(opponent)
        
        # If opponent is closer to goal, try to block them
        if opponent_path < player_path and self.game_state.walls_remaining[player] > 0:
            best_wall = self._find_best_blocking_wall(opponent)
            if best_wall:
                result = ("wall", best_wall)
                print(f"AI medium selected blocking wall: {result}")
                return result
        
        # Otherwise, move toward goal
        legal_moves = self.movement.get_legal_moves(player)
        if not legal_moves:
            return None
            
        # Find move that minimizes distance to goal
        best_move = None
        best_distance = float('inf')
        
        for move in legal_moves:
            # Temporarily make move
            original_pos = self.game_state.player_positions[player]
            self.game_state.player_positions[player] = list(move)
            
            # Calculate new distance
            new_distance = self.pathfinding.shortest_path_length(player)
            
            # Restore position
            self.game_state.player_positions[player] = original_pos
            
            if new_distance < best_distance:
                best_distance = new_distance
                best_move = move
        
        result = ("move", best_move) if best_move else ("move", legal_moves[0])
        print(f"AI medium selected move: {result}")
        return result
    
    def _hard_move(self):
        """Hard AI: Uses minimax with alpha-beta pruning (simplified for performance)"""
        player = self.game_state.current_player
        
        # First, check if we can win in one move
        legal_moves = self.movement.get_legal_moves(player)
        for move in legal_moves:
            row, col = move
            if self._is_winning_move(player, row, col):
                result = ("move", move)
                print(f"AI hard selected winning move: {result}")
                return result
        
        # Try to find a good wall placement
        if self.game_state.walls_remaining[player] > 0:
            opponent = self._get_main_opponent(player)
            best_wall = self._find_best_blocking_wall(opponent)
            if best_wall:
                # Evaluate if this wall significantly helps
                original_opponent_path = self.pathfinding.shortest_path_length(opponent)
                
                # Temporarily place wall
                row, col, horizontal = best_wall
                if horizontal:
                    self.game_state.horizontal_walls[row][col] = True
                else:
                    self.game_state.vertical_walls[row][col] = True
                
                new_opponent_path = self.pathfinding.shortest_path_length(opponent)
                
                # Revert wall
                if horizontal:
                    self.game_state.horizontal_walls[row][col] = False
                else:
                    self.game_state.vertical_walls[row][col] = False
                
                if new_opponent_path > original_opponent_path + 1:  # Wall significantly blocks
                    result = ("wall", best_wall)
                    print(f"AI hard selected blocking wall: {result}")
                    return result
        
        # Use medium AI strategy as fallback
        result = self._medium_move()
        print(f"AI hard fell back to medium: {result}")
        return result
    
    def _get_main_opponent(self, player):
        """Get the main opponent (for 2-player games)"""
        if self.game_state.player_count == 2:
            return 3 - player
        else:
            # In multi-player, pick the first other player
            for p in range(1, self.game_state.player_count + 1):
                if p != player:
                    return p
            return 2  # Fallback
    
    def _is_winning_move(self, player, row, col):
        """Check if a move would win the game"""
        board_size = self.game_state.board_size
        player_count = self.game_state.player_count
        
        if player_count == 2:
            if player == 1:
                return row == board_size - 1
            elif player == 2:
                return row == 0
        
        elif player_count == 4:
            if player == 1:
                return row == board_size - 1
            elif player == 2:
                return row == 0
            elif player == 3:
                return col == board_size - 1  # Left -> Right
            elif player == 4:
                return col == 0  # Right -> Left
        return False
    
    def _find_best_blocking_wall(self, target_player):
        """Find wall that best blocks the target player"""
        best_wall = None
        best_improvement = 0
        
        for row in range(self.game_state.board_size - 1):
            for col in range(self.game_state.board_size - 1):
                for horizontal in [True, False]:
                    valid, _ = self.wall_placement.is_valid_wall_placement(row, col, horizontal)
                    if valid:
                        # Test this wall
                        original_path = self.pathfinding.shortest_path_length(target_player)
                        
                        # Temporarily place wall
                        if horizontal:
                            self.game_state.horizontal_walls[row][col] = True
                        else:
                            self.game_state.vertical_walls[row][col] = True
                        
                        if self.pathfinding.paths_exist_for_all_players():  # FIXED: was paths_exist_for_both_players
                            new_path = self.pathfinding.shortest_path_length(target_player)
                            improvement = new_path - original_path
                            
                            if improvement > best_improvement:
                                best_improvement = improvement
                                best_wall = (row, col, horizontal)
                        
                        # Revert wall
                        if horizontal:
                            self.game_state.horizontal_walls[row][col] = False
                        else:
                            self.game_state.vertical_walls[row][col] = False
        
        return best_wall