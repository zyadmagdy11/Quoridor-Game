class WallPlacement:
    def __init__(self, game_state):
        self.game_state = game_state

    def is_valid_wall_placement(self, r, c, horizontal=True):
        N = self.game_state.board_size
        H = self.game_state.horizontal_walls
        V = self.game_state.vertical_walls

        # bounds
        if r < 0 or r >= N - 1 or c < 0 or c >= N - 1:
            return False, "Out of bounds"

        if horizontal:
            # already exists
            if H[r][c]:
                return False, "Wall exists"

            # check adjacency
            if c > 0 and H[r][c - 1]:
                return False, "Adjacent horizontal"
            if c < N - 2 and H[r][c + 1]:
                return False, "Adjacent horizontal"

            # crossing
            if V[r][c]:
                return False, "Cross vertical"
            if r > 0 and V[r - 1][c]:
                return False, "Cross vertical"
        else:
            if V[r][c]:
                return False, "Wall exists"

            # adjacency
            if r > 0 and V[r - 1][c]:
                return False, "Adjacent vertical"
            if r < N - 2 and V[r + 1][c]:
                return False, "Adjacent vertical"

            # crossing
            if H[r][c]:
                return False, "Cross horizontal"
            if c > 0 and H[r][c - 1]:
                return False, "Cross horizontal"

        return True, ""

    def place_wall(self, r, c, horizontal=True, pathfinding=None):
        valid, reason = self.is_valid_wall_placement(r, c, horizontal)
        if not valid:
            return False, reason

        H = self.game_state.horizontal_walls
        V = self.game_state.vertical_walls

        # temporary placement
        if horizontal:
            H[r][c] = True
        else:
            V[r][c] = True

        # verify all players still have a path
        if pathfinding and not pathfinding.paths_exist_for_all_players():
            if horizontal:
                H[r][c] = False
            else:
                V[r][c] = False
            return False, "Blocks a player"

        # consume a wall
        self.game_state.walls_remaining[self.game_state.current_player] -= 1

        return True, "Wall placed"
