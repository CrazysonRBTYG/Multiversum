import random
from model.local_consts import *
from collections import deque

class Match3Game:
    def __init__(self, rows=MATCH3_ROWS, cols=MATCH3_COLS, num_types=MATCH3_COLORS):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.board = []
        self.moves = 0
        self.score = 0
        self.timer = GAME_TIMER
        self._generate_board()

    def _generate_board(self):
        self.board = [[random.randint(1, self.num_types) for _ in range(self.cols)] for _ in range(self.rows)]
        while self.find_matches():
            self.board = [[random.randint(1, self.num_types) for _ in range(self.cols)] for _ in range(self.rows)]

    def find_matches(self):
        matches = set()
        visited = [[False] * self.cols for _ in range(self.rows)]

        def bfs(row, col, direction):
            queue = deque([(row, col)])
            matched = [(row, col)]
            tile_type = self.board[row][col]

            if direction == 'H':
                while queue:
                    row, col = queue.popleft()
                    for direction in [-1, 1]:
                        next_col = col + direction
                        if 0 <= next_col < self.cols and self.board[row][next_col] == tile_type and (row, next_col) not in matched:
                            queue.append((row, next_col))
                            matched.append((row, next_col))

            elif direction == 'V':
                while queue:
                    row, col = queue.popleft()
                    for direction in [-1, 1]:
                        next_row = row + direction
                        if 0 <= next_row < self.rows and self.board[next_row][col] == tile_type and (next_row, col) not in matched:
                            queue.append((next_row, col))
                            matched.append((next_row, col))

            if len(matched) >= 3:
                return matched
            return []

        for row in range(self.rows):
            for col in range(self.cols):
                if not visited[row][col]:
                    horizontal_match = bfs(row, col, 'H')
                    vertical_match = bfs(row, col, 'V')
                    for row, col in horizontal_match + vertical_match:
                        visited[row][col] = True
                        matches.add((row, col))

        return list(matches)

    def remove_matches(self):
        matches = self.find_matches()
        for row, col in matches:
            self.board[row][col] = 0
        return len(matches)

    def drop_tiles(self):
        matches = self.find_matches()
        self.score += SCORE_ADD_VALUE(matches)
        if self.timer != 0:
            self.timer += TIME_ADD_VALUE(matches)
        for col in range(self.cols):
            empty_row = self.rows - 1
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] != 0:
                    self.board[empty_row][col] = self.board[row][col]
                    if empty_row != row:
                        self.board[row][col] = 0
                    empty_row -= 1
            for row in range(empty_row, -1, -1):
                self.board[row][col] = random.randint(1, self.num_types)

    def make_move(self, row1, col1, row2, col2):
        if abs(row1 - row2) + abs(col1 - col2) != 1:
            return False
        self.board[row1][col1], self.board[row2][col2] = self.board[row2][col2], self.board[row1][col1]
        if self.find_matches():
            return True
        else:
            self.board[row1][col1], self.board[row2][col2] = self.board[row2][col2], self.board[row1][col1]
            return False