from collections import deque
from CSP import csp, squares, placement_to_list
from datetime import datetime


def AC3(csp):
    '''
    Returns resulting puzzle and time elapsed to solve the puzzle 
    whose CSP variables are initialized in CSP
    '''
    time_start = datetime.now()
    arcs_queue = deque([])

    # Each arc is a tuple from start -> end
    for arc in csp.constraints:
        arcs_queue.append(arc)

    i = 0
    while len(arcs_queue) != 0:
        # Get arc from the queue
        (start, end) = arcs_queue.pop()
        i += 1

        # Check if values have been revised for this arc
        if is_revised(csp, start, end):
            if len(csp.values[start]) == 0:
                return ("Not solved!", -1)

            for new_start in (csp.neighbors[start] - set(end)):
                arcs_queue.append((new_start, start))

    placement = placement_to_list(csp.values)
    time_to_solve = (datetime.now()-time_start).total_seconds()
    return (placement, time_to_solve)


# Check if the csp is revised and values are set of possible values for the
# start of the arc, s.t. the arc is start --> end
def is_revised(csp, start, end):
    revised = False
    vals = set(csp.values[start])

    for val in vals:
        if not is_consistent(csp, val, start, end):
            orig_values = csp.values[start]
            csp.values[start] = orig_values.replace(val, '')
            revised = True

    return revised


# Determines if the placement of values is consistent, looking at a particular arc
def is_consistent(csp, var, start, end):
    for val in csp.values[end]:
        if end in csp.neighbors[start]:
            if val != var:
                return True
    return False
