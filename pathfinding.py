# pathfinding.py

from collections import deque

class Pathfinding:
    def __init__(self, game_state):
        self.game_state = game_state
    
    def neighbors(self, r, c):
        """Get reachable neighbors from a position"""
        from movement import Movement
        mover = Movement(self.game_state)
        
        results = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.game_state.board_size and 0 <= nc < self.game_state.board_size:
                if not mover.is_blocked_between(r, c, nr, nc):
                    results.append((nr, nc))
        return results
    
    def exists_path_to_goal(self, player):
        """BFS to check if player can reach their goal"""
        start = tuple(self.game_state.player_positions[player])
        goal_cells = self.get_goal_cells(player)
        visited = set()
        queue = deque([start])
        
        while queue:
            r, c = queue.popleft()
            if (r, c) in goal_cells:
                return True
            for nr, nc in self.neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return False
    
    def get_goal_cells(self, player):
        """Get goal cells for a player based on player count and position"""
        board_size = self.game_state.board_size
        player_count = self.game_state.player_count
        
        if player_count == 2:
            if player == 1:
                return [(board_size - 1, col) for col in range(board_size)]  # Bottom row
            elif player == 2:
                return [(0, col) for col in range(board_size)]  # Top row
        elif player_count == 4:
            if player == 1:
                return [(board_size - 1, col) for col in range(board_size)]  # Bottom row
            elif player == 2:
                return [(0, col) for col in range(board_size)]  # Top row
            elif player == 3:
                return [(row, board_size - 1) for row in range(board_size)]  # Right column
            elif player == 4:
                return [(row, 0) for row in range(board_size)]  # Left column
        return set()
    
    def paths_exist_for_all_players(self):
        """Check if all players have paths to their goals"""
        for player in range(1, self.game_state.player_count + 1):
            if not self.exists_path_to_goal(player):
                return False
        return True
    
    def shortest_path_length(self, player):
        """Calculate shortest path length for a player to their goal (for AI)"""
        start = tuple(self.game_state.player_positions[player])
        goal_cells = self.get_goal_cells(player)
        visited = set()
        queue = deque([(start, 0)])  # (position, distance)
        
        while queue:
            (r, c), dist = queue.popleft()
            if (r, c) in goal_cells:
                return dist
            for nr, nc in self.neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), dist + 1))
        return float('inf')  # No path found