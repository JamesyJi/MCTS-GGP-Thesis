"""
Will concatenate results from distributed computing effort
"""
import json

with open("overall_trap_stats.json") as f:
    final_trap_stats = json.load(f)

with open("trap_stats.json") as f:
    trap_stats = json.load(f)
    for t, c in trap_stats.items():
        if t in final_trap_stats:
            final_trap_stats[t] += c
        else:
            final_trap_stats[t] = c

with open("overall_turn_stats.json") as f:
    final_turn_stats = json.load(f)

with open("turn_stats.json") as f:
    turn_stats = json.load(f)
    for t, c in turn_stats.items():
        if t in final_turn_stats:
            final_turn_stats[t] += c
        else:
            final_turn_stats[t] = c

with open("overall_trap_stats.json", "w") as f:
    json.dump(final_trap_stats)

with open("overall_turn_stats.json") as f:
    json.dump(final_turn_stats)