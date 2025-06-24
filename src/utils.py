import heapq
from typing import List, Tuple, Optional, Dict


def get_valid_neighbors(
    pos: Tuple[int, int], grid: List[List[str]]
) -> List[Tuple[int, int]]:
    row, col = pos
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            neighbors.append((new_row, new_col))

    return neighbors


def find_all_positions(
    grid: List[List[str]], target_symbols: List[str] = None
) -> Dict[str, List[Tuple[int, int]]]:
    if target_symbols is None:
        target_symbols = ["A", "D", "B", "R"]

    positions = {symbol: [] for symbol in target_symbols}

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in positions:
                positions[cell].append((i, j))

    return positions


def get_target_ring(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    rings = find_all_positions(grid, ["R"])["R"]
    if not rings:
        return None
    return max(rings, key=lambda pos: pos[1])


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_path_blocked(
    start: Tuple[int, int], end: Tuple[int, int], grid: List[List[str]]
) -> bool:
    start_row, start_col = start
    end_row, end_col = end

    if start_row != end_row and start_col != end_col:
        return True

    if start_row == end_row:
        for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
            if grid[start_row][col] == "D":
                return True
    else:
        for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
            if grid[row][start_col] == "D":
                return True

    return False


def print_grid(
    grid: List[List[str]], symbols: dict, target_ring: Tuple[int, int] = None
):
    print("     ", end="")
    for col in range(len(grid[0])):
        print(f"{col:3d}", end="")
    print()

    print("     " + "┌" + "─" * (len(grid[0]) * 3) + "┐")

    for row_idx, row in enumerate(grid):
        print(f"  {row_idx:2d} │", end="")
        for col_idx, cell in enumerate(row):
            display_cell = symbols.get(cell, cell)

            if target_ring and (row_idx, col_idx) == target_ring:
                if cell == "R":
                    display_cell = "🎯"
                elif cell == "B":
                    display_cell = "🏆"

            if display_cell in ["🏀", "🔵", "🔴", "🎯", "🏆"]:
                print(f"{display_cell} ", end="")
            else:
                print(f" {display_cell} ", end="")

        print("│")

    print("     " + "└" + "─" * (len(grid[0]) * 3) + "┘")
