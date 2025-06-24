import heapq
from typing import List, Tuple, Optional
from utils import get_valid_neighbors, manhattan_distance, get_target_ring


class AStarNode:
    def __init__(
        self,
        position: Tuple[int, int],
        g_cost: int,
        h_cost: int,
        parent: Optional["AStarNode"] = None,
    ):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other: "AStarNode") -> bool:
        if self.f_cost == other.f_cost:
            return self.g_cost > other.g_cost
        return self.f_cost < other.f_cost


def calculate_heuristic(
    pos: Tuple[int, int], goal: Tuple[int, int], grid: List[List[str]]
) -> int:
    base_distance = manhattan_distance(pos, goal)
    penalty = 0

    row, col = pos
    goal_row, goal_col = goal

    if row == goal_row:
        for c in range(min(col, goal_col), max(col, goal_col) + 1):
            if grid[row][c] == "D":
                penalty += 1
    elif col == goal_col:
        for r in range(min(row, goal_row), max(row, goal_row) + 1):
            if grid[r][col] == "D":
                penalty += 1
    else:
        for c in range(min(col, goal_col), max(col, goal_col) + 1):
            if grid[row][c] == "D":
                penalty += 1
        for r in range(min(row, goal_row), max(row, goal_row) + 1):
            if grid[r][goal_col] == "D":
                penalty += 1

    return base_distance + penalty


def is_valid_neighbor(neighbor: Tuple[int, int], grid: List[List[str]]) -> bool:
    """Check if a neighbor position is valid for pathfinding"""
    return grid[neighbor[0]][neighbor[1]] in [".", "R"]


def astar_pathfinding(
    start: Tuple[int, int], goal: Tuple[int, int], grid: List[List[str]]
) -> Tuple[List[Tuple[int, int]], int]:
    """Temukan path terbaik dari start ke goal menggunakan A*"""
    open_list = []
    closed_set = set()
    best_g_cost = {}

    start_node = AStarNode(start, 0, calculate_heuristic(start, goal, grid))
    heapq.heappush(open_list, start_node)
    best_g_cost[start] = 0

    while open_list:
        current = heapq.heappop(open_list)
        if (
            current.position in best_g_cost
            and current.g_cost > best_g_cost[current.position]
        ):
            continue

        if current.position == goal:
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            return path[::-1], current.g_cost

        if current.position in closed_set:
            continue

        closed_set.add(current.position)

        for neighbor in get_valid_neighbors(current.position, grid):
            if neighbor in closed_set or not is_valid_neighbor(neighbor, grid):
                continue
            tentative_g_cost = current.g_cost + 1
            if neighbor not in best_g_cost or tentative_g_cost < best_g_cost[neighbor]:
                best_g_cost[neighbor] = tentative_g_cost
                h_cost = calculate_heuristic(neighbor, goal, grid)
                neighbor_node = AStarNode(neighbor, tentative_g_cost, h_cost, current)
                heapq.heappush(open_list, neighbor_node)

    return [], float("inf") 


def find_best_path_to_ring(
    player_pos: Tuple[int, int], grid: List[List[str]]
) -> Tuple[List[Tuple[int, int]], int]:
    target = get_target_ring(grid)
    if target:
        return astar_pathfinding(player_pos, target, grid)
    return [], float("inf")
