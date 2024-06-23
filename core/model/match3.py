import random
from model.local_consts import *
from collections import deque

class Match3Game:
    def __init__(self, rows=MATCH3_ROWS, cols=MATCH3_COLS, num_types=MATCH3_COLORS):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types - 1
        self.board = []
        self.moves = 0
        self.generate_board()

    def generate_board(self):
        self.board = [[random.randint(1, self.num_types) for _ in range(self.cols)] for _ in range(self.rows)]
        while self.find_matches():
            self.board = [[random.randint(1, self.num_types) for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))
        print()

    def find_matches(self):
        matches = set()
        visited = [[False] * self.cols for _ in range(self.rows)]

        def bfs(row, col):
            queue = deque([(row, col)])
            matched = [(row, col)]
            visited[row][col] = True
            tile_type = self.board[row][col]

            while queue:
                r, c = queue.popleft()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and not visited[nr][nc] and self.board[nr][nc] == tile_type:
                        queue.append((nr, nc))
                        matched.append((nr, nc))
                        visited[nr][nc] = True

            if len(matched) >= 3:
                matches.update(matched)

        for row in range(self.rows):
            for col in range(self.cols):
                if not visited[row][col]:
                    bfs(row, col)

        return list(matches)

    def remove_matches(self):
        matches = self.find_matches()
        for row, col in matches:
            self.board[row][col] = 0
        return len(matches)

    def drop_tiles(self):
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