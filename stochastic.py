from random import randint
import math
from math import sqrt
from functools import reduce
from datetime import datetime

def conflict_count(puzzle): #number of conflicts used as the heuristic
    rowconflicts = 0
    colconflicts = 0
    blockconflicts = 0
    for row in range(9):
        for col in range(9):
            cell = puzzle[row][col]
          
            for otherrow in range(9):
              if otherrow != row:
                if puzzle[otherrow][col] == cell:
                  rowconflicts += 1
            
            for othercol in range(9):
              if othercol != col:
                if puzzle[row][othercol] == cell:
                  colconflicts += 1

            vert_block_index = row // 3
            hor_block_index = col // 3

            row_start = vert_block_index * 3
            row_end = row_start + 3 - 1

            col_start = hor_block_index * 3
            col_end = col_start + 3 - 1

            for r in range(row_start, row_end+1):
                for c in range(col_start, col_end+1):
                      if row != r and col != c:
                        if puzzle[r][c] == cell:
                          blockconflicts += 1
    totalconflicts = rowconflicts + colconflicts + blockconflicts
    return totalconflicts


def duplicate_board(board):
    copy = []
    for row in board:
        new_row = []
        for num in row:
            new_row.append(num)
        copy.append(new_row)
    return copy


def initial_possibilities(size, input_puzzle):
    possibilities = [list(filter(lambda y: y not in x, range(1, size+1)))
        for x in input_puzzle
    ]
    return possibilities

def random_index(possibilities, row_index):
  return randint(0, len(possibilities[row_index])-1)

def make_swaps(board, swaps, row_index):
  next_board = duplicate_board(board)
  next_board[row_index][swaps[1]], next_board[row_index][swaps[0]] = next_board[row_index][swaps[0]], next_board[row_index][swaps[1]]
  return next_board

def new_board(board, given):
    size = 9
    possibilities = list(
        map(lambda x: list(filter(lambda y: (x[0], y) not in given, x[1])),
        enumerate([list(range(size)) for x in range(size)])))

    row_index = randint(0,size-1)
    if len(possibilities[row_index]) == 0:
      raise Exception
    else: 
      swaps = []
      for i in range(2):
        randind = random_index(possibilities, row_index)
        swaps.append(possibilities[row_index][randind])

        del possibilities[row_index][randind]

      next_board = make_swaps(board, swaps, row_index)
      return next_board


def initial_board(input_puzzle, constraints):
    num_cols = 9
    num_rows = 9
    board = duplicate_board(input_puzzle)
   
    possibilities = initial_possibilities(num_cols, input_puzzle)
      

    for row in range(num_rows):
        for col in range(num_cols):
            if (row,col) not in constraints:
                placement = randint(0, len(possibilities[row])-1)
                board[row][col] = possibilities[row][placement]
                del possibilities[row][placement]
    return board

def initialize_set(puzzle, given_nums, count):
  boards = []
  i = 0
  while i < count:
      board = initial_board(puzzle, given_nums)
      boards.append((board, conflict_count(board)))
      i = i+1
  return boards

def output_format(matrix):
  result = []
  for row in matrix:
    for num in row:
        result.append(num)
  return result

def given_val_list(input_puzzle, num_rows, num_cols):
    given_nums = [[]]
    for i in range(num_rows):
        for j in range(num_cols):
            if input_puzzle[i][j] != 0:
                given_nums.append((i, j))
    return given_nums

def is_solution(num_conflicts):
  if num_conflicts == 0:
    return True
  else:
    return False


def solver(puzzle):
    num_successors = 9
    beam_width = 10
    num_rows = 9
    num_cols = 9
    constraints = given_val_list(puzzle, num_rows, num_cols)

    solution = []
  
    start = datetime.now()

    boards = initialize_set(puzzle, constraints, num_successors)
    
    numrestarts = 0
    numlevels = 0
    while len(solution) == 0:
        numlevels += 1
        randnum = randint(0, 10)
        if numrestarts > 10:
          print("here")
          return ("Not solved", -1)

        if (datetime.now() - start).total_seconds() > 2 and randnum > 8:
          start = datetime.now()
          numrestarts += 1
          boards = initialize_set(puzzle, constraints, num_successors)

        #sort the number of conflicts
        boards.sort(key=lambda board: board[1])

        local_optimum = boards[0][1]
        if is_solution(local_optimum):
            solution = boards[0][0]
        else:
            optimal_boards = boards[:beam_width]

            all_successors = []
            for board in optimal_boards:
                board_successors = []
                for i in range(num_successors):
                    successor = new_board(board[0], constraints)
                    board_successors.append((successor, conflict_count(successor)))
                
                board_successors.sort(key = lambda succ: succ[1])
                best_successor = board_successors[0]
                

                chance_best = randint(1, 10)
                if chance_best > 2:
                  all_successors.append(best_successor)
                else:
                  random_succ = randint(0, len(board_successors)-1)
                  all_successors.append(board_successors[random_succ])
                    
            for board in all_successors:
                boards.append(board)
    endtime = (datetime.now() - start).total_seconds()
    solution = output_format(solution)
    return (solution, endtime)