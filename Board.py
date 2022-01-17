ALL_DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (1, 0)]
LINE_LENGTH_VALUE = {0: 0, 1: 0, 2: 3, 3: 10}  # maybe change a bit


class Board:
    def __init__(self, size: tuple[int, int]):
        self.board = [[None for _ in range(size[1])] for _ in range(size[0])]
        self.available_cols = {i for i in range(size[0])}
        self.piles_height = [0] * size[0]
        self.size = size

        self.current_turn = False

    def __getitem__(self, item: tuple[int, int]):
        return self.board[item[0]][item[1]]

    def __setitem__(self, key: tuple[int, int], value):
        self.board[key[0]][key[1]] = value

    def turn(self, col: int):
        assert col in self.available_cols
        self[col, self.piles_height[col]] = self.current_turn

        self.piles_height[col] += 1

        if self.piles_height[col] == self.size[1]:  # column full
            self.available_cols.remove(col)

        self.current_turn = not self.current_turn

    def undo_tern(self, col: int):
        assert self[col, self.piles_height[col] - 1] is not None

        self.piles_height[col] -= 1
        self.available_cols.add(col)
        self[col, self.piles_height[col]] = None
        self.current_turn = not self.current_turn

    def __repr__(self):
        return f"<Board {self.size}; Turn: {int(self.current_turn)}>"

    def printb(self, **kwargs):
        """Print the game state in ASCII."""
        # "■□"
        print("_" * (self.size[0] + 2), **kwargs)
        for row in range(self.size[1]):
            row = self.size[1] - row - 1
            s = "|"
            for col in range(self.size[0]):
                if self.piles_height[col] > row:
                    if self[col, row]:
                        s += "■"
                    else:
                        s += "□"
                else:
                    s += " "
            s += "|"
            print(s, **kwargs)

        print("_" * (self.size[0] + 2), **kwargs)
        if self.size[0] <= 10:
            print("|" + ''.join([str(x) for x in range(self.size[0])]) + "|", **kwargs)
            print("‾" * (self.size[0] + 2), **kwargs)

    ####################################################################

    def get_line_length(self, origin: tuple[int, int], direction: tuple[int, int]):
        """
        Checks how many of the same pieces are in the given line- without any pieces of the second player.
        :param origin: The starting position of the line.
        :param direction: The direction the line goes in. Vector of the x,y change.
        :return: The number of same pieces in the given line. If there are pieces of the second player returns 0.
        """
        assert self[origin] is not None
        player = self[origin]
        pos: list[int] = list(origin)
        length = 1

        for _ in range(3):  # we look for lines of 4, and we already have started with the origin point.
            pos[0] += direction[0]
            pos[1] += direction[1]

            if 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]:
                value = self[tuple(pos)]
                if value is player:
                    length += 1
                elif value is (not player):
                    return 0
                # o.w. value is None, so we add 0.
            else:
                return 0

        return length

    def state_value(self):
        """
        The `value` of the current game state.
        As the value gets bigger the state is better for the first player.
        """
        f_value = 0  # the first player progress
        t_value = 0  # the second players progress
        for col in range(self.size[0]):
            for row in range(self.piles_height[col]):
                player = self[col, row]

                for direction in ALL_DIRECTIONS:
                    line_length = self.get_line_length((col, row), direction)
                    if line_length == 4:  # some player has won the game
                        return -float('inf') if player else float('inf')

                    value = LINE_LENGTH_VALUE[line_length]
                    if player:
                        t_value += value
                    else:
                        f_value += value

        return f_value - t_value
