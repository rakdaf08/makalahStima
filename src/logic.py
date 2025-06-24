from typing import List, Tuple, Dict
from astar import astar_pathfinding
from utils import (
    get_valid_neighbors,
    manhattan_distance,
    find_all_positions,
    get_target_ring,
)


def find_players(grid: List[List[str]]) -> Dict[str, List[Tuple[int, int]]]:
    return find_all_positions(grid, ["A", "D", "B"])


def move_player_towards_target(
    player_pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    grid: List[List[str]],
    occupied_positions: set,
    steps: int = 2,
) -> Tuple[int, int]:
    current_pos = player_pos
    for _ in range(steps):
        neighbors = get_valid_neighbors(current_pos, grid)
        best_neighbor = None
        best_distance = float("inf")

        for neighbor in neighbors:
            if (
                grid[neighbor[0]][neighbor[1]] == "."
                and neighbor not in occupied_positions
            ):
                dist = manhattan_distance(neighbor, target_pos)
                if dist < best_distance:
                    best_distance = dist
                    best_neighbor = neighbor

        if best_neighbor:
            occupied_positions.add(best_neighbor)
            current_pos = best_neighbor
        else:
            break
    return current_pos


def calculate_all_attacker_costs(
    attackers: List[Tuple[int, int]], grid: List[List[str]]
) -> Dict[Tuple[int, int], int]:
    target_ring = get_target_ring(grid)
    if not target_ring:
        return {}

    costs = {}
    for attacker_pos in attackers:
        _, cost = astar_pathfinding(attacker_pos, target_ring, grid)
        costs[attacker_pos] = cost
    return costs


def create_pass_options_text(
    costs: Dict[Tuple[int, int], int], ball_carrier_pos: Tuple[int, int]
) -> List[str]:
    pass_options = []
    for pos, cost in costs.items():
        player_type = "Ball carrier" if pos == ball_carrier_pos else "Player"
        pass_options.append(f"{player_type} at {pos}: cost {cost}")
    return pass_options


def find_best_pass_option(
    ball_carrier_pos, attackers, grid, moved_positions, current_tick=0
):
    target_ring = get_target_ring(grid)
    if not target_ring:
        return ball_carrier_pos, {}, "No target ring found"

    temp_grid = [row[:] for row in grid]

    for i, row in enumerate(temp_grid):
        for j, cell in enumerate(row):
            if cell in ["A", "B"]:
                temp_grid[i][j] = "."

    ball_carrier_new_pos = moved_positions.get(ball_carrier_pos, ball_carrier_pos)

    for old_pos in attackers:
        new_pos = moved_positions.get(old_pos, old_pos)
        if temp_grid[new_pos[0]][new_pos[1]] == ".":

            if new_pos == ball_carrier_new_pos:
                temp_grid[new_pos[0]][new_pos[1]] = "B"
            else:
                temp_grid[new_pos[0]][new_pos[1]] = "A"

    costs = {}
    for old_pos in attackers:
        new_pos = moved_positions.get(old_pos, old_pos)
        _, cost = astar_pathfinding(new_pos, target_ring, temp_grid)
        costs[new_pos] = cost

    if not costs:
        return ball_carrier_pos, {}, "No valid costs calculated"

    ball_carrier_new_pos = moved_positions.get(ball_carrier_pos, ball_carrier_pos)

    best_teammate = min(costs.keys(), key=lambda pos: costs[pos])
    best_cost = costs[best_teammate]

    best_cost_with_tick = best_cost + current_tick

    pass_options = []
    for pos, cost in costs.items():
        cost_with_tick = cost + current_tick
        player_type = "Ball carrier" if pos == ball_carrier_new_pos else "Player"
        pass_options.append(f"{player_type} at {pos}: cost {cost_with_tick}")

    if best_teammate == ball_carrier_new_pos:
        pass_decision = f"Keep ball (best option: cost {best_cost_with_tick})"
    else:
        pass_decision = f"Pass to {best_teammate} (cost: {best_cost_with_tick})"

    pass_decision += f" | Options: {' | '.join(pass_options)}"

    return best_teammate, costs, pass_decision


def move_defenders(
    players: Dict[str, List[Tuple[int, int]]],
    grid: List[List[str]],
    new_grid: List[List[str]],
) -> Dict[Tuple[int, int], Tuple[int, int]]:
    defender_moved_positions = {}

    for defender_pos in players["D"]:
        current_pos = defender_pos

        for step in range(2):
            next_i, next_j = current_pos

            if (
                next_j + 1 < len(grid[0])
                and new_grid[next_i][next_j + 1] == "."
                and (next_i, next_j + 1) not in defender_moved_positions.values()
            ):
                current_pos = (next_i, next_j + 1)
            else:
                break

        defender_moved_positions[defender_pos] = current_pos

    return defender_moved_positions


def update_game_state(
    grid: List[List[str]], current_tick: int = 0
) -> Tuple[List[List[str]], Dict]:

    new_grid = [["." for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "R":
                new_grid[i][j] = "R"

    players = find_players(grid)
    game_info = {
        "attacker_costs": {},
        "pass_decision": "",
        "ball_carrier": None,
        "target_ring": None,
        "goal_scored": False,
    }

    ball_carrier_pos = players["B"][0] if players["B"] else None
    if not ball_carrier_pos:
        return grid, game_info

    all_attackers = players["A"] + players["B"]
    target_ring = get_target_ring(grid)
    if not target_ring:
        return grid, game_info

    game_info["target_ring"] = target_ring
    game_info["ball_carrier"] = ball_carrier_pos

    moved_positions = {}
    occupied_positions = set()

    for attacker_pos in all_attackers:
        new_pos = move_player_towards_target(
            attacker_pos, target_ring, new_grid, occupied_positions, 2
        )
        moved_positions[attacker_pos] = new_pos

    best_pass_target, costs, pass_decision = find_best_pass_option(
        ball_carrier_pos, all_attackers, new_grid, moved_positions, current_tick
    )
    game_info["attacker_costs"] = costs
    game_info["pass_decision"] = pass_decision
    game_info["ball_carrier_after_move"] = best_pass_target

    goal_achieved = False
    ball_carrier_cost = costs.get(best_pass_target, float("inf"))

    if ball_carrier_cost <= 1:
        goal_achieved = True
        game_info["goal_scored"] = True

    for old_pos in all_attackers:
        new_pos = moved_positions[old_pos]

        if new_pos == best_pass_target and goal_achieved:
            if new_grid[target_ring[0]][target_ring[1]] == "R":
                new_grid[target_ring[0]][target_ring[1]] = "B"
                game_info["ball_carrier_after_move"] = target_ring
        else:
            if new_grid[new_pos[0]][new_pos[1]] == ".":
                new_grid[new_pos[0]][new_pos[1]] = (
                    "B" if new_pos == best_pass_target else "A"
                )

    defender_moved_positions = move_defenders(players, grid, new_grid)
    moved_positions.update(defender_moved_positions)

    for defender_pos in players["D"]:
        new_pos = defender_moved_positions[defender_pos]
        if new_grid[new_pos[0]][new_pos[1]] == ".":
            new_grid[new_pos[0]][new_pos[1]] = "D"

    return new_grid, game_info


def check_game_end(grid: List[List[str]]) -> bool:
    ball_carrier_pos = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "B":
                ball_carrier_pos = (i, j)
                break
        if ball_carrier_pos:
            break

    if not ball_carrier_pos:
        return False

    target_ring = get_target_ring(grid)
    if not target_ring:
        return False

    _, cost = astar_pathfinding(ball_carrier_pos, target_ring, grid)

    return cost <= 1
