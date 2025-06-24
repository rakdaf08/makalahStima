from typing import List
from config import INITIAL_GRID, DISPLAY_SYMBOLS, SIMULATION_LIMIT
from logic import (
    update_game_state,
    check_game_end,
    get_target_ring,
    find_players,
    calculate_all_attacker_costs,
)
from utils import print_grid
import time


def print_game_analysis(game_info: dict, current_tick: int = 0):
    if not game_info:
        return

    print("\n📊 ANALISIS A* COST:")

    if game_info.get("ball_carrier"):
        ball_pos = game_info["ball_carrier"]

    if game_info.get("attacker_costs"):
        print(f"\n💰 Cost tiap pemain penyerang ke target ring - State {current_tick}:")
        costs = game_info["attacker_costs"]
        ball_carrier_pos = game_info.get("ball_carrier_after_move")

        sorted_costs = sorted(costs.items(), key=lambda x: x[1])

        for pos, cost in sorted_costs:
            player_type = "🏀" if pos == ball_carrier_pos else "🔵"
            total_cost_with_tick = cost + current_tick
            print(
                f"   {player_type} Baris {pos[0]}, Kolom {pos[1]}: cost {total_cost_with_tick}"
            )
        print("\n")

    if game_info.get("pass_decision"):
        pass_info = game_info["pass_decision"]

        if "cost" in pass_info.lower() and game_info.get("attacker_costs"):
            costs = game_info["attacker_costs"]

            updated_decision = pass_info
            for pos, cost in costs.items():
                total_cost_with_tick = cost + current_tick

                old_cost_pattern = f"cost {cost}"
                new_cost_pattern = f"cost {total_cost_with_tick}"
                updated_decision = updated_decision.replace(
                    old_cost_pattern, new_cost_pattern
                )

        print("=" * 80)


def run_simulation():
    grid = [row[:] for row in INITIAL_GRID]
    tick = 0

    target_ring = get_target_ring(grid)

    print("\n📋 KONDISI AWAL")
    print_grid(grid, DISPLAY_SYMBOLS, target_ring)
    print("=" * 80)

    initial_players = find_players(grid)
    initial_attackers = initial_players["A"] + initial_players["B"]

    while tick < SIMULATION_LIMIT:
        tick += 1

        grid, game_info = update_game_state(grid, tick)
        target_ring = game_info.get("target_ring")

        print(f"\nState: {tick}")
        print_grid(grid, DISPLAY_SYMBOLS, target_ring)

        print_game_analysis(game_info, tick)

        if check_game_end(grid) or game_info.get("goal_scored"):
            print("\n🎉 Bola berhasil masuk ring!!")
            break

        time.sleep(2)

    if tick >= SIMULATION_LIMIT:
        print(f"\n⏰ Simulasi berakhir setelah {SIMULATION_LIMIT} ticks tanpa gol.")

    print(f"📊 Simulasi selesai dalam {tick} ticks.")


def print_legend():
    print("📋 LEGENDA:")
    print("=" * 50)

    legend_items = [
        ("🏀 B", "Pemain dengan bola"),
        ("🔵 A", "Pemain penyerang"),
        ("🔴 D", "Pemain bertahan"),
        ("🎯 R", "Ring basket (target)"),
        ("  . ", "Area kosong"),
    ]

    for symbol, description in legend_items:
        print(f"{symbol} = {description}")
