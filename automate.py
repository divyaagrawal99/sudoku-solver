import fileinput
import sys
from bruteForce import *
from CSP import *
from AC3 import *
from stochastic import *
import functools
from colorama import Fore, Back, Style
import csv


def format_puzzle(puzzle):
    solved = ""
    for i in range(0, len(puzzle), 9):
        solved += ' '.join(str(e) for e in puzzle[i:i+9]) + "\n"
    return solved


methods = ["AC3", "CSP", "BF", "ST"]
files = ["almost_filled", "blank", "hard", "impossible", "input_unsolvable",
"input1", "input2", "input3", "multiple_solution"]

for method in methods:
  for file in files:
    file_times = []
    for i in range(5):
      puzzle1 = []
      puzzle2 = []
      puzzle3 = []
      # puzzle 3 is a 1D list of integers
      solved_puzzle = "Unsolved"
      final_time = ""

      with open("inputs/" + file + ".txt", "r") as f:
          data = f.readlines()
          for line in data:
              line = line.split()
              int_line = []
              for i in range(len(line)):
                  puzzle1.append((line[i]))
                  int_line.append(int(line[i]))
              for num in int_line:
                  puzzle3.append(num)
              puzzle2.append(int_line)

      # must return a tuple name solved : (1d list of int for solved puzzle of strs, time)
      if method == "BF":
          sudoku = BruteForce(puzzle3)
          solved = sudoku.solve()

      if method == "CSP":
          sudoku = csp(puzzle=puzzle1)
          solved = csp_solver(sudoku)

      if method == "AC3":
          sudoku = csp(puzzle=puzzle1)
          solved = AC3(sudoku)

      if method == "ST":
          solved = solver(puzzle=puzzle2)

      puzzle = solved[0]
      solved_puzzle = format_puzzle(puzzle)
      final_time = solved[1]

      file_times.append(final_time)

    with open('outputs/data_aggregated.csv', 'a+') as csv_file:
        fieldnames = ['method', 'file', 'averagetime', 'rangetime', 'successrate']
        
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        rangetime = 0
        successrate = 0
        mintime = maxtime = file_times[0]
        totaltime = 0
        for time in file_times:
          totaltime += time
          if time != -1:
            successrate += 1
          mintime = min(mintime, time)
          maxtime = max(maxtime, time)
        successrate = successrate / 5
        rangetime = maxtime - mintime
        avgtime = totaltime / 5
        
        # writer.writeheader()
        writer.writerow({'method': method, 'file': file, 'averagetime':avgtime,
        'rangetime': rangetime, 'successrate': successrate})
    print("Completed file!")
  print("Completed method!")
print("Completed all!")