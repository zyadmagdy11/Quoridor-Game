# movement.py

class Movement:
    def __init__(self, game_state):
        self.game_state = game_state
    
    def is_blocked_between(self, r1, c1, r2, c2):
        """Check if movement between two adjacent cells is blocked by a wall"""
        board_size = self.game_state.board_size
        
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return True
            
        if r2 == r1 - 1:  # Moving up
            wr = r2
            if 0 <= wr < board_size - 1:
                if 0 <= c1 < board_size - 1 and self.game_state.horizontal_walls[wr][c1]:
                    return True
                if 0 <= c1 - 1 < board_size - 1 and self.game_state.horizontal_walls[wr][c1 - 1]:
                    return True
            return False
            
        if r2 == r1 + 1:  # Moving down
            wr = r1
            if 0 <= wr < board_size - 1:
                if 0 <= c1 < board_size - 1 and self.game_state.horizontal_walls[wr][c1]:
                    return True
                if 0 <= c1 - 1 < board_size - 1 and self.game_state.horizontal_walls[wr][c1 - 1]:
                    return True
            return False
            
        if c2 == c1 - 1:  # Moving left
            wc = c2
            if 0 <= wc < board_size - 1:
                if 0 <= r1 < board_size - 1 and self.game_state.vertical_walls[r1][wc]:
                    return True
                if 0 <= r1 - 1 < board_size - 1 and self.game_state.vertical_walls[r1 - 1][wc]:
                    return True
            return False
            
        if c2 == c1 + 1:  # Moving right
            wc = c1
            if 0 <= wc < board_size - 1:
                if 0 <= r1 < board_size - 1 and self.game_state.vertical_walls[r1][wc]:
                    return True
                if 0 <= r1 - 1 < board_size - 1 and self.game_state.vertical_walls[r1 - 1][wc]:
                    return True
            return False
            
        return True
    
    def get_legal_moves(self, player):
        board_size = self.game_state.board_size
        row, col = self.game_state.player_positions[player]
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < board_size and 0 <= nc < board_size):
                continue
            if self.is_blocked_between(row, col, nr, nc):
                continue
                
            # Check if target cell has another player
            other_player = self.game_state.other_player_at(nr, nc)
            if other_player:
                # Jump over opponent
                jr, jc = nr + dr, nc + dc
                if (0 <= jr < board_size and 0 <= jc < board_size and 
                    not self.is_blocked_between(nr, nc, jr, jc) and 
                    self.game_state.other_player_at(jr, jc) is None):
                    moves.append((jr, jc))
                else:
                    # Diagonal jumps when blocked
                    perp = [(-dc, -dr), (dc, dr)]
                    for pdr, pdc in perp:
                        diag_r, diag_c = nr + pdr, nc + pdc
                        if (0 <= diag_r < board_size and 0 <= diag_c < board_size and
                            not self.is_blocked_between(nr, nc, diag_r, diag_c) and 
                            self.game_state.other_player_at(diag_r, diag_c) is None):
                            moves.append((diag_r, diag_c))
            else:
                moves.append((nr, nc))
        
        # Remove duplicates
        unique = []
        for m in moves:
            if m not in unique:
                unique.append(m)
        return unique
    
    def make_move(self, player, row, col):
        """Execute a move for the player"""
        legal_moves = self.get_legal_moves(player)
        if (row, col) not in legal_moves:
            return False
            
        self.game_state.player_positions[player] = [row, col]
        return True