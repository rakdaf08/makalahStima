# Game configuration
GRID_ROWS = 5
GRID_COLS = 11
MOVEMENT_STEPS = 2
SIMULATION_LIMIT = 20

# Initial game grid
INITIAL_GRID = [
    [".", "D", ".", "D", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", "A", ".", ".", ".", ".", ".", ".", ".", "."],
    ["R", "D", "B", "A", ".", ".", ".", ".", ".", ".", "R"],
    [".", "A", "D", "A", ".", ".", ".", ".", ".", ".", "."],
    [".", "D", ".", ".", ".", ".", ".", ".", ".", ".", "."],
]

# Game symbols
SYMBOLS = {
    "ATTACKER": "A",
    "DEFENDER": "D",
    "BALL_CARRIER": "B",
    "RING": "R",
    "EMPTY": ".",
}

# Display symbols
DISPLAY_SYMBOLS = {"R": "🎯", "B": "🏀", "A": "🔵", "D": "🔴", ".": "."}
