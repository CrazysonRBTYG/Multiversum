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
        self.timer = 30
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

        def bfs(row, col, direction):
            queue = deque([(row, col)])
            matched = [(row, col)]
            tile_type = self.board[row][col]

            if direction == 'H':
                while queue:
                    r, c = queue.popleft()
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < self.cols and self.board[r][nc] == tile_type and (r, nc) not in matched:
                            queue.append((r, nc))
                            matched.append((r, nc))

            elif direction == 'V':
                while queue:
                    r, c = queue.popleft()
                    for dr in [-1, 1]:
                        nr = r + dr
                        if 0 <= nr < self.rows and self.board[nr][c] == tile_type and (nr, c) not in matched:
                            queue.append((nr, c))
                            matched.append((nr, c))

            if len(matched) >= 3:
                return matched
            return []

        for row in range(self.rows):
            for col in range(self.cols):
                if not visited[row][col]:
                    horizontal_match = bfs(row, col, 'H')
                    vertical_match = bfs(row, col, 'V')
                    for r, c in horizontal_match + vertical_match:
                        visited[r][c] = True
                        matches.add((r, c))

        return list(matches)

    def remove_matches(self):
        matches = self.find_matches()
        for row, col in matches:
            self.board[row][col] = 0
        return len(matches)

    def drop_tiles(self):
        matches = self.find_matches()
        self.score += len(matches) + 2**len(matches)
        if self.timer != 0:
            self.timer += len(matches) // 3
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