from copy import deepcopy
from datetime import datetime

nums = cols = "123456789"
rows = "ABCDEFGHI"


def cross_product(A, B):
    return [a + b for a in A for b in B]


squares = cross_product(rows, cols)


class csp(object):

    def __init__(self, domain=nums, puzzle=[]):
        self.variables = squares
        self.domain = self.values = self.get_values(puzzle)
        self.groups = self.get_groups()
        self.units = self.get_units()
        self.neighbors = self.get_neighbors()
        self.constraints = self.get_constraints()

    def get_constraints(self):
        """
        Returns set of variable to its neighbors
        """
        constraints = set()
        for variable in self.variables:
            for peer in self.neighbors[variable]:
                constraints.add((variable, peer))
        return constraints

    def get_neighbors(self):
        """
        Returns dictionary of square to the other squares this value can't be equal to
        """
        neighbors = dict()
        for square in squares:
            all_neighbors = sum(self.units[square], [])
            square_set = [square]
            neighbors[square] = set(all_neighbors) - set(square_set)

        return neighbors

    def get_units(self):
        """
        Returns dictionary of square mapped to the list of groups the square is in
        """
        units = dict((s, [u for u in self.groups if s in u])
                     for s in squares)
        return units

    def get_values(self, puzzle=[]):
        """
        Use the puzzle input and get the dictionary of variable to current value
        where the value is '123456789' if the value is unknown or '0'
        """
        i = 0
        values = dict()
        for cell in self.variables:
            if puzzle[i] == '0':
                values[cell] = nums
            else:
                values[cell] = puzzle[i]
            i = i + 1
        return values

    def get_groups(self):
        """
        Returns list of the 27 groups of squares that cannot contain the same value
        """
        col_lst = []
        for c in cols:
            col_lst += [cross_product(rows, c)]

        row_lst = []
        for r in rows:
            row_lst += [cross_product(r, cols)]

        block_lst = []
        for block_rows in ('ABC', 'DEF', 'GHI'):
            for block_cols in ('123', '456', '789'):
                block_lst += [cross_product(block_rows, block_cols)]

        return col_lst + row_lst + block_lst


# Set the initial placement of squares to values to be empty and backtrack
def csp_solver(csp):
    start = datetime.now()
    result = backtrack({}, csp, start)
    placement = result[0]
    time = result[1]
    return (placement_to_list(placement), time)


# Convert the final placement from a dictionary of squares to values to a list
def placement_to_list(placement):
    result = []
    if placement != "Not solved!":
        for square in squares:
            result.append(placement[square])
    return result


# Backtrack to assign values for the given puzzle
def backtrack(placement, csp, start):
    # Check if all squares have been assigned
    if set(placement.keys()) == set(squares):
        return placement, (datetime.now()-start).total_seconds()

    d = deepcopy(csp.values)
    # Determine the next variable to assign using MRV
    v = next_unknown_var(placement, csp)

    for val in csp.values[v]:
        if is_consistent(csp, placement, v, val):
            placement[v] = val
            guesses = {}
            guesses = get_guesses(
                placement, guesses, csp, v, val)
            if guesses != "Not solved!":
                result = backtrack(placement, csp, start)
                if result != "Not solved!":
                    return result

            del placement[v]
            csp.values.update(d)

    return ("Not solved!", -1)


# Use guesses to check value for a variable
def get_guesses(placement, guesses, csp, square, val):
    guesses[square] = val

    for n in csp.neighbors[square]:
        if n not in placement:
            if val in csp.values[n]:
                guesses_helper(csp, placement, guesses, n, val)

    return guesses


# Return if the guesses do not solve the puzzle or not
def guesses_helper(csp, placement, guesses, neighbor, val):
    if len(csp.values[neighbor]) == 1:
        return "Not solved!"

    remaining = csp.values[neighbor] = csp.values[neighbor].replace(
        val, "")

    if len(remaining) == 1:
        state = get_guesses(placement, guesses,
                            csp, neighbor, remaining)
        if state == "Not solved!":
            return "Not solved!"


# Use minimum remaining value to select the next variable to solve
def next_unknown_var(placement, csp):
    unknown_vars = dict()
    for square in csp.values:
        if square not in placement:
            unknown_vars[square] = len(csp.values[square])
    mrv = min(unknown_vars, key=unknown_vars.get)
    return mrv


# Checks if placement is consistent meaning none of its neighbors have the same value
def is_consistent(csp, placement, square, val):
    for n in csp.neighbors[square]:
        if n in placement:
            if placement[n] == val:
                return False
    return True
