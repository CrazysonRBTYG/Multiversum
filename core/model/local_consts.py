MATCH3_ROWS = 10
MATCH3_COLS = 10
MATCH3_COLORS = 6

STATS_FILE = "core/stats.json"

DEFAULT_TIMER = 1000
GAME_TIMER = 20

SCORE_DECREASE = lambda score: score // 10
SCORE_ADD_VALUE = lambda matches: len(matches) + 2**len(matches)
TIME_ADD_VALUE = lambda matches: len(matches) // 2