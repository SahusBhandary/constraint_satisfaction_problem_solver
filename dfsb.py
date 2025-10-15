import sys
import collections

"""
Output:
- On success: writes the color for each variable (0..K-1), one per line.
- On failure (no solution found): "No answer."

"""
if len(sys.argv) != 4:
    sys.stderr.write(" python dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be an integer")
    sys.exit(2)


# problem definition
no_of_variables = None
no_of_constraints = None
no_of_colors = None
constraints = []  # list of [a, b] pairs

with open(input_file, 'r') as f:
    first = f.readline().split()
    no_of_variables = int(first[0])
    no_of_constraints = int(first[1])
    no_of_colors = int(first[2])
    for line in f:
        a, b = map(int, line.split())
        constraints.append((a, b))

# DFS-B (backtracking)
def consistent(var, val, assignment):
    # Check if assigning var=val is consistent with current partial assignment
    # Only check constraints where both ends are assigned (including the proposed var)
    for (a, b) in constraints:
        x = assignment.get(a, None) if a != var else val
        y = assignment.get(b, None) if b != var else val
        if x is not None and y is not None and x == y:
            return False
    return True

def dfs_backtrack(assignment):
     # recursive backtracking on variables in index order (0..N-1)
    if len(assignment) == no_of_variables:
        return assignment
    var = len(assignment)  # next variable by index order
    for val in range(no_of_colors):
        if consistent(var, val, assignment):
            assignment[var] = val
            res = dfs_backtrack(assignment)
            if res is not None:
                return res
            # backtrack
            del assignment[var]
    return None

# DFS B++ Code

# The generate_csp function is used to initially generate all domains for each variable.
# Takes in a reference to csp and initializes it with all possible color values (since we didn't make an assignment yet).     
def generate_csp(csp):
    for n in range(no_of_variables):
        if n not in csp:
            csp[n] = [i for i in range(no_of_colors)]

# Get the neighbors of a variable
def get_neighbors(var):
    neighbors = set()
    for a, b in constraints:
        if a == var:
            neighbors.add(b)
        elif b == var:
            neighbors.add(a)
    
    return neighbors

# MCV Heuristic: Make assignment based on which variable has the least number of options
def make_assignment(csp, assignment):
    var_assigned = 0

    # Figure out a list that has elements
    for keys in csp:
        if keys not in assignment and csp[keys]:
            var_assigned = keys
            break
    
    # Find the key with the smallest length
    for keys in csp:
        if keys in assignment or not csp[keys]:
            continue
        if len(csp[keys]) < len(csp[var_assigned]):
            var_assigned = keys
        
    return var_assigned

# LCV Heurisitc: Choose value based on the fewest number of changes it makes
def value_ordering(var, assignment, csp):
    values = {}
    neighbors = get_neighbors(var)

    for val in csp[var]:
        count = 0

        for neighbor in neighbors:
            if neighbor not in assignment and val in csp[neighbor]:
                count += 1
        
        values[val] = count
    
    return sorted(csp[var], key=lambda v: values[v])

# Forward Check function: propagates the change through the entire network
def forward_check(var, assignment, csp):
    neighbors = get_neighbors(var)
    assignment_var = assignment[var]

    for neighbor in neighbors:
        if neighbor in assignment:
            continue

        if csp[neighbor] and assignment_var in csp[neighbor]:
            # Prune from the domain of neighbors
            csp[neighbor].remove(assignment_var)

            # Early Termination
            if len(csp[neighbor]) == 0:
                return False
    
    return True

    
# *** Check forward checking function, csp is not being updated properly
iter = [0]
def dfs_backtracking_plus(assignment, csp):
    iter[0] += 1

    if len(assignment) == no_of_variables:
        return assignment
    
    # Terminates after 500,000 Iterations
    if iter[0] == 500000:
        return None
    
    var = make_assignment(csp, assignment)

    
    if not csp[var] or len(csp[var]) == 0:
        return None

    for val in value_ordering(var, assignment, csp):
        
        assignment[var] = val
        
        # Generate New CSP with updated vals
        new_csp = {k: v[:] if v else v for k, v in csp.items()}
        new_csp[var] = None

        if forward_check(var, assignment, new_csp):
            res = dfs_backtracking_plus(assignment, new_csp)
            if res is not None:
                return res
            
        del assignment[var]
    
    return None




# mode 0 dfsb
if mode == 0:
    solution = dfs_backtrack({})
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")

# mode 1 dfsb++  You should implement here
else:
    csp = {}
    generate_csp(csp)
    solution = dfs_backtracking_plus(assignment={}, csp=csp)
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")
    
