"""
Output:
- On success: each variable’s color (0..K-1), one per line.
- On failure (no solution found after iteration cap): "No answer."
"""

import sys
import random

if len(sys.argv) != 4:
    sys.stderr.write("python minconflicts.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be integer")
    sys.exit(2)

# read input
with open(input_file, 'r') as f:
    first_line = list(map(int, f.readline().split()))
    N, M, K = first_line
    edges = [tuple(map(int, line.split())) for line in f]

# build neighbor graph
neighbors = {i: [] for i in range(N)}
for a, b in edges:
    neighbors[a].append(b)
    neighbors[b].append(a)

def conflicting_vars(assign):
    # return list of variables currently in conflict
    bad = []
    for i in range(N):
        for j in neighbors[i]:
            if assign[i] == assign[j]:
                bad.append(i)
                break
    return bad

def min_conflict_color(var, assign):
    # return color (0..K-1) minimizing conflicts for variable var
    best_color, best_conflicts = assign[var], N + 1
    for c in range(K):
        conflicts = sum(1 for j in neighbors[var] if assign[j] == c)
        if conflicts < best_conflicts:
            best_color, best_conflicts = c, conflicts
    return best_color


def min_conflicts_basic(max_steps=500000):
    assign = [random.randint(0, K - 1) for _ in range(N)]
    print(assign)
    for step in range(max_steps):
        bad = conflicting_vars(assign)
        if not bad:
            return assign
        var = random.choice(bad)
        assign[var] = min_conflict_color(var, assign)
    return None

random_restart = random.randint(0, 100000)
max_restart_steps = [500000]
def min_conflicts_restart(max_steps=500000):
    
    assign = [random.randint(0, K - 1) for _ in range(N)]
    for step in range(max_restart_steps[0]):
        bad = conflicting_vars(assign)
        if not bad:
            return assign
        
        if random_restart == random.randint(0,100000):
            return min_conflicts_restart()
        
        var = random.choice(bad)
        assign[var] = min_conflict_color(var, assign)
        max_restart_steps[0] -= 1
    return None


# mode 0 MCRS
if mode == 0:
    solution = min_conflicts_basic()
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")

# mode 1 MCRS with restart  You should implement here
else:
    solution = min_conflicts_restart()
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")
