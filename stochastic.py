from random import randint
import math
from math import sqrt
from functools import reduce
from datetime import datetime

num_branches = 9
beam_width = 10

def conflict_count(board): #number of conflicts used as the heuristic
    rowconflicts = 0
    colconflicts = 0
    blockconflicts = 0
    for row in range(9):
        for col in range(9):
            cell = board[row][col]
          
            for otherrow in range(9):
              if otherrow != row:
                if board[otherrow][col] == cell:
                  rowconflicts += 1
            
            for othercol in range(9):
              if othercol != col:
                if board[row][othercol] == cell:
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
                        if board[r][c] == cell:
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



def generate_successor(board, given):
    size = 9
    choices = list(
        map(lambda x: list(filter(lambda y: (x[0], y) not in given, x[1])),
        enumerate([list(range(size)) for x in range(size)])))

    row = randint(0,size-1)
    if len(choices[row]) == 0:
      raise Exception
    else: 
      index1 = randint(0, len(choices[row])-1)
      choice1 = choices[row][index1]
      del choices[row][index1]
      index2 = randint(0, len(choices[row])-1)
      choice2 = choices[row][index2]
      del choices[row][index2]
      ret = duplicate_board(board)
      ret[row][choice2], ret[row][choice1] = ret[row][choice1], ret[row][choice2]
      return ret


def generate_board(given_board, given_nums):
    size = 9
    board = duplicate_board(given_board)
    choices = [list(filter(lambda y: y not in x, range(1, size+1)))
        for x in given_board
    ]

    for i in range(size):
        for j in range(size):
            if (i,j) not in given_nums:
                index = randint(0, len(choices[i])-1)
                board[i][j] = choices[i][index]
                del choices[i][index]
    return board

def initial_set(puzzle, given_nums, beam_width):
  boards = []
  i = 0
  while i < beam_width:
      board = generate_board(puzzle, given_nums)
      boards.append((board, conflict_count(board)))
      i = i+1
  return boards

def output_format(matrix):
  result = []
  for row in matrix:
    for num in row:
        result.append(num)
  return result



def solver(puzzle):
    size = 9
    given_nums = [[]]
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] != 0:
                given_nums.append((i, j))
    solved = False
    solution = []
  
    start = datetime.now()
    boards = initial_set(puzzle, given_nums, beam_width=beam_width)

    numrestarts = 0
    while not solved:
        randnum = randint(0, 10)
        if numrestarts > 10:
         return ("Not solved", -1)

        if (datetime.now() - start).total_seconds() > 2 and randnum > 8:
          start = datetime.now()
          numrestarts += 1
          boards = initial_set(puzzle, given_nums, beam_width=beam_width)



        # order by heuristic value of boards
        boards.sort(key=lambda board: board[1])

        # take top 10 (lower heuristic values)
        boards = boards[:beam_width]
        # check first board
        # print(boards[0][1])
        if boards[0][1] == 0:
            # if heuristic is 0, set solved to true and set as solution
            solved = True
            solution = boards[0][0]
        else:
            # else, generate successors and loop
            ## generate successor boards
            newboards = []
            for board in boards:
                # board_successors = []
                try:
                  for i in range(num_branches):
                      successor = generate_successor(board[0], given_nums)
                      newboards.append((successor, conflict_count(successor)))
                except:
                  return ("Not solved!", -1)
                    

                # board_successors.sort(key = lambda succ: succ[1])

                
                # newboards.append(board_successors[:6])
                # randbranch = randint(3, num_branches-1)
                # newboards.append(board_successors[randbranch])

            # add each successor to current list with heuristic value
            for board in newboards:
                # print(board[1])
                boards.append(board)

    solution = output_format(solution)
    return (solution, (datetime.now() - start).total_seconds())