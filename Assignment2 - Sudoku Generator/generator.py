import re
import os
import random
import numpy


class GenerateSudokuBoard(object):
    """
    Will generate a board to play sudoku
    """

    def __init__(self):
        self.testing_board = [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0]
        ]
        self.sudoku_board = []

    def generate_board_with_mace4(self):
        self.__create_sudoku_generator_file()
        self.__call_mace4_to_generate_full_board()
        self.sudoku_board = self.__parse_full_board_from_mace4_file()  # get a full board from mace4
        self.__print_sudoku()
        self.sudoku_board = self.__shuffle(self.sudoku_board)
        self.__print_sudoku()
        self.__complex_solve()
        self.__print_sudoku()

        self.__generate_sudoku_solver_file()  # generate mace4 file for the current board
        self.__call_mace4_to_verify_sudoku()
        if self.__solution_is_unique():
            print("unique")
        else:
            print("not unique")
        return self.sudoku_board

    def __complex_solve(self):
        positions = numpy.arange(0, 81, 1)  # list of positions
        numpy.random.shuffle(positions)  # shuffle the positions
        board_clone = self.__save_a_copy_board()  # duplicate the original board

        values_removed = 0
        current_index = 0

        while values_removed < 64 and current_index < 81:
            row = positions[current_index] // 9
            col = positions[current_index] % 9

            # remove number from current index
            self.sudoku_board[row][col] = 0

            self.__generate_sudoku_solver_file()  # generate mace4 file for the current board
            self.__call_mace4_to_verify_sudoku()  # solve the current board

            if not self.__solution_is_unique():
                # put the number back
                self.sudoku_board[row][col] = board_clone[row][col]
            else:
                # it's still solvable, move on
                values_removed += 1

            current_index += 1

    def __save_a_copy_board(self):
        copy_board = []
        for a_list in self.sudoku_board:
            copy_board.append(list.copy(a_list))
        return copy_board

    def __shuffle(self, old_board):
        board = numpy.array(old_board)
        group = 3  # we can only safely shuffle between groupd of 3 consecutive rows/columns
        number_of_shuffles = random.randrange(1, 10, 1)
        for i in range(number_of_shuffles):
            numpy.random.shuffle(board.reshape(board.shape[0] // group, -1, board.shape[1]))    # shuffles rows
            board = numpy.transpose(board)  # transpose the board so that we can shuffle the columns

        return board.tolist()

    def __simple_solve(self):
        # generation algorithm
        to_remove = 81  # number of attempts to remove numbers from the board

        while to_remove > 0:
            # select a random row and a column
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            # if that position has already been removed, search again
            while self.sudoku_board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)

            # memorize the value to be removed, then remove it
            old_value = self.sudoku_board[row][col]
            self.sudoku_board[row][col] = 0

            self.__generate_sudoku_solver_file()  # generate mace4 file for the current board
            self.__call_mace4_to_verify_sudoku()  # solve the current board
            if not self.__solution_is_unique():
                # the board does not have a unique solution, put the number back and try again
                self.sudoku_board[row][col] = old_value
            to_remove -= 1

    def __print_sudoku(self):
        for r in range(9):
            for c in range(9):
                if c != 8:
                    print(str(self.sudoku_board[r][c]), end=" ")
                else:
                    print(str(self.sudoku_board[r][c]))
        print("\n")

    def __call_mace4_to_generate_full_board(self):
        os.system("mace4 -m 1 -f sudoku_generator_with_1_value.in | interpformat > mace4_complete_sudoku.out")

    def __parse_full_board_from_mace4_file(self):
        sudoku_board = []
        sudoku_file = "mace4_complete_sudoku.out"
        with open(sudoku_file, 'r') as inp:
            lines = inp.read()
            lines_list = lines.splitlines()
            sudoku_lines = []
            for (index, line) in enumerate(lines_list):
                if index >= 2 and index <= 10:
                    sudoku_lines.append(line.strip())
            for line in sudoku_lines:
                parsed_line = re.split(',|\]|\)', line)
                sudoku_line = [ele for ele in parsed_line if ele.strip()]
                sudoku_board.append(self.__get_row_as_list(sudoku_line))
        return sudoku_board

    def __get_row_as_list(self, line):
        row_list = []
        for element in line:
            number = int(element)
            if number == 0:
                number = 9  # transform zeros to 9
            row_list.append(number)
        return row_list

    def __generate_sudoku_solver_file(self):
        sudoku_generator_file = "sudoku_generator.in"
        sudoku_solver_file = "sudoku_solver.in"
        with open(sudoku_solver_file, "w") as f2:
            with open(sudoku_generator_file, "r") as f1:
                for line in f1:
                    f2.write(line)
            f2.write("formulas(sample_puzzle).\n")

            for r in range(9):
                for c in range(9):
                    if self.sudoku_board[r][c] != 0: 
                        if self.sudoku_board[r][c] == 9:
                            f2.write(f"f({r},{c}) = 0.\n")
                        else:
                            f2.write(f"f({r},{c}) = {self.sudoku_board[r][c]}.\n")

            f2.write("end_of_list.\n")

    def __create_sudoku_generator_file(self):
        sudoku_generator_file = "sudoku_generator.in"
        sudoku_solver_file = "sudoku_generator_with_1_value.in"
        with open(sudoku_solver_file, "w") as f2:
            with open(sudoku_generator_file, "r") as f1:
                for line in f1:
                    f2.write(line)
            f2.write("formulas(sample_puzzle).\n")

            random_row = random.randint(0, 8)
            random_column = random.randint(0, 8)
            random_nr = random.randint(0, 8)

            f2.write(f"f({random_row},{random_column}) = {random_nr}.\n")

            f2.write("end_of_list.\n")

    def __call_mace4_to_verify_sudoku(self):
        os.system("mace4 -m 2 -f sudoku_solver.in | interpformat > mace4_verify_sudoku.out")

    def __solution_is_unique(self):
        no_of_solution = None
        solutions_obtained_file = "mace4_verify_sudoku.out"
        with open(solutions_obtained_file, "r") as inp:
            for line in inp.readlines():
                elements_parsed = self.__parse_interpretation_line(line)
                if elements_parsed[0] == "interpretation":
                    no_of_solution = elements_parsed[3]
        if (no_of_solution) == '1':
            return True
        return False

    def __parse_interpretation_line(self, line):
        line_parsed = re.split(',|=|\(|\[|\]', line)
        remove_space = [x.strip(' ') for x in line_parsed]
        delete_empty = [ele for ele in remove_space if ele.strip()]
        return delete_empty


sudokuBoardGenerator = GenerateSudokuBoard()
sudokuBoardGenerator.generate_board_with_mace4()
