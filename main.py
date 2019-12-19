import fileinput
import sys
from bruteForce import *
from CSP import *
from AC3 import *
from stochastic import *
import functools
from colorama import Fore, Back, Style


def format_puzzle(puzzle):
    solved = ""
    for i in range(0, len(puzzle), 9):
        solved += ' '.join(str(e) for e in puzzle[i:i+9]) + "\n"
    return solved


if __name__ == "__main__":

    print(Fore.CYAN +
          "Are you ready for us to solve your sudoku puzzles? \n" + Fore.RESET)
    print(Fore.CYAN + "Enter the name of the file like '<file_name>' without the .txt ending:" + Fore.RESET)
    file = input()
    print(Fore.RED + "\nEnter the method you'd like to use" + Fore.RESET)
    print(Fore.RED + "Available Methods: BF = Brute Force, CSP = Constraint Satisfaction Problem, AC3 = arc-consistency, ST=stochastic" + Fore.RESET)
    method = input()

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
    final_time = str(solved[1])

    with open("outputs/"+file+"_"+method+"_"+"output.txt", "a+") as f:
        f.write("\n=================================== \n" + solved_puzzle + "\n \n" +
                "Solved In: " + final_time + " seconds")
        f.close()
    print(Fore.GREEN + "Check the outputs folder to see your result!" + Fore.RESET)