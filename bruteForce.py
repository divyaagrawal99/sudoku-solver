from datetime import datetime, timedelta
import math


class BruteForce(object):
    
    def __init__(self, puzzle):
        """
        Initialization of the different components for the Sudoku Puzzle
        """
        self.num_rows = 9
        self.block_size = 3
        self.puzzle = puzzle
        self.known_values = self.get_known_values(puzzle)
        self.time = datetime.now()

    
    def get_known_values(self, puzzle):
        """
        Returns the list of the known values from the Sudoku puzzle 
        (all values that are not 0)
        """
        lst = []
        for i in range(len(puzzle)):
            if puzzle[i] != 0:
                lst.append(int(i))
        return lst

    def solve(self):
        """
        Solves the sudoku puzzle and returns the puzzle and the time taken
        to solve it.
        """

        try:
          x = self.solve_helper(0, 1)
          while x != -1:
            x = self.solve_helper(x[0], x[1])

          return (self.puzzle, (datetime.now() - self.time).total_seconds())
        except:
          return("Not solved!", -1)
        
        
    def is_found(self, index, start):
        length = len(self.puzzle)
        prev_valid = -1
        found_valid = False

        if not (index > -1 and index < length - 1):
            raise Exception
        
        for i in range(index, length):
            # i is a number/each number represents the index
            # goes through the numbers from index (0) to 81
            if i not in self.known_values:
                found_valid = False
                for test in range(start, self.num_rows + 1):
                    # go through all numbers from 1 to 9 to see if they fit
                    if self.valid(i, test):
                        found_valid = True
                        prev_valid = i
                        self.puzzle[i] = test
                        break
                start = 1
                if not found_valid:
                    break
        return(found_valid, prev_valid)
    
   
    def solve_helper(self, index, start):
        """
        Goes through each unknown value in the puzzle to make a guess to figure
        out valid numbers. Continues through this process until the Sudoku is
        solved.
        """
        found_valid, prev_valid = self.is_found(index, start)
        if not found_valid:
            if (prev_valid != -1):
                i_new = prev_valid
            else:
                i_new = index - 1
            
            start_new = self.puzzle[i_new] + 1
            self.edit_puzzle(i_new)

            while start_new > self.num_rows or i_new in self.known_values:
                i_new = i_new - 1
                start_new = self.puzzle[i_new] + 1
                self.edit_puzzle(i_new)

            return (i_new, start_new)
            
        else:
            return -1

    
    def edit_puzzle(self, index):
        """
        Edits the puzzle so it goes back to its original form.
        """
        length = len(self.puzzle)

        for x in range(index, length):
            if x not in self.known_values:
                self.puzzle[x] = 0

    def valid(self, index, test):
        """
        Checks that the puzzle is valid for row, column, and block constraints.
        """
        r = int(math.floor(index / self.num_rows))
        c = index % self.num_rows
        s = self.num_rows * r
        f = s + self.num_rows
        b_r = int(math.floor(r / self.block_size))
        b_c = int(math.floor(c / self.block_size))

        r_s = b_r * self.block_size
        r_e = r_s + self.block_size - 1
        c_s = b_c * self.block_size
        c_e = c_s + self.block_size - 1

        # check row
        for c_index in range(s, f):
            if c_index != index:
                if self.puzzle[c_index] == test:
                    return False

        # check column
        for x in range(0, self.num_rows):
            r_i = c + (self.num_rows * x)
            if r_i != index:
                if self.puzzle[r_i] == test:
                    return False

        # check block
        for z in range(r_s, r_e + 1):
            for k in range(c_s, c_e + 1):
                t = k + (z * self.num_rows)
                if self.puzzle[t] == test:
                    return False

        return True
