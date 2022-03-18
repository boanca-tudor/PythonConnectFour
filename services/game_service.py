"""
    Module containing the implementation of game logic
"""
from repos.board import Board, BoardPoint
from domain.cell import CellStatus
from enum import Enum


class GameException(Exception):
    """
        Custom exception class for potential game errors
    """
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class MoveOutsideBoundsException(GameException):
    """
        Exception which occurs if the player tries to make a move outside of the board
    """
    pass


class GameOutcome(Enum):
    DRAW = 0,
    PLAYER1_WIN = 1,
    PLAYER2_WIN = 2


class GameServices:
    """
        Class which handles all of the game logic
    """
    def __init__(self, board: Board):
        self.__board = board

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, value):
        self.__board = value

    def mark_move(self, column):
        """
        Marks the move as being made in the list which holds the column height - increases the current column's height
        by 1
        :param column: The column on which the move was made
        :return: -
        """
        self.__board.column_height[column] += 1

    def make_player1_move(self, column):
        """
        Marks the cell as being occupied by the first player and increases the column's size
        :param column: The column on which the move was made
        :return: The point on the board where the move was made
        :raises: MoveOutsideBoundsException if the move was outside of the board
        """
        if not 0 <= column <= self.__board.columns:
            raise MoveOutsideBoundsException('Move is outside of the board!')

        current_row = self.__board.rows - self.__board.column_height[column] - 1
        if current_row < 0:
            raise MoveOutsideBoundsException('Move is outside of the board!')
        self.__board[current_row][column].occupy_by_player1()
        self.mark_move(column)
        return BoardPoint(column, current_row)

    def make_player2_move(self, column):
        """
        Marks the cell as being occupied by the second player and increases the column's size
        :param column: The column on which the move was made
        :return: The point on the board where the move was made
        """
        current_row = self.__board.rows - self.__board.column_height[column] - 1
        if current_row < 0:
            raise MoveOutsideBoundsException('Move is outside of the board!')
        self.__board[current_row][column].occupy_by_player2()
        self.mark_move(column)
        return BoardPoint(column, current_row)

    def is_game_over(self, point, player_index):
        """
        Checks if the game is over - either the board is full or one player has won
        Evaluates if the last move made was a winning one or not
        :param point: Point of the last move
        :param player_index: The index of the player who made the move
        :return: GameOutcome.DRAW if the board is full
                 GameOutcome.PLAYER1_WIN if the first player won
                 GameOutcome.PLAYER2_WIN if the second player won
        """
        spaces_left = []
        for row in range(self.__board.rows):
            spaces_left.append(any([cell.status == CellStatus.EMPTY for cell in self.__board[row]]))
        spaces_left = any(spaces_left)
        if not spaces_left:
            return GameOutcome.DRAW
        elif player_index == 1:
            if self.is_checkmate(point, CellStatus.OCCUPIED_BY_PLAYER1):
                return GameOutcome.PLAYER1_WIN
        elif player_index == 2:
            if self.is_checkmate(point, CellStatus.OCCUPIED_BY_PLAYER2):
                return GameOutcome.PLAYER2_WIN

    def is_checkmate(self, point, cell_status):
        """
        Checks if the last made move is a checkmate
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: True - the last move was a checkmate
                 False - the last move was not a checkmate
        """
        return self.check_horizontal_line(point, cell_status) or self.check_vertical_line(point, cell_status) \
            or self.check_primary_diagonal_line(point, cell_status) \
            or self.check_secondary_diagonal_line(point, cell_status)

    def check_horizontal_line(self, point, cell_status):
        """
        Checks if the last made move completes a horizontal line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: True - the last move completes a line
                 False - the last move does not complete a line
        """
        return self.calculate_horizontal_line(point, cell_status) == 4

    def calculate_horizontal_line(self, point, cell_status):
        """
        Calculates the length of the horizontal line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        return self.calculate_left(point, cell_status) + self.calculate_right(point, cell_status) - 1

    def calculate_left(self, point, cell_status):
        """
        Calculates the length of the line from the left of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.x >= 0 and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.x -= 1
            identical_cells += 1

        return identical_cells

    def calculate_right(self, point, cell_status):
        """
        Calculates the length of the line from the right of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.x < self.__board.columns and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.x += 1
            identical_cells += 1

        return identical_cells

    def check_vertical_line(self, point, cell_status):
        """
        Checks if the last made move completes a vertical line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: True - the last move completes a line
                 False - the last move does not complete a line
        """
        return self.calculate_vertical_line(point, cell_status) == 4

    def calculate_vertical_line(self, point, cell_status):
        """
        Calculates the length of the vertical line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        return self.calculate_up(point, cell_status) + self.calculate_down(point, cell_status) - 1

    def calculate_down(self, point, cell_status):
        """
        Calculates the length of the line from down the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y < self.__board.rows and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y += 1
            identical_cells += 1

        return identical_cells

    def calculate_up(self, point, cell_status):
        """
        Calculates the length of the line from up the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y >= 0 and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y -= 1
            identical_cells += 1

        return identical_cells

    def check_primary_diagonal_line(self, point, cell_status):
        """
        Checks if the last made move completes a primary diagonal parallel line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: True - the last move completes a line
                 False - the last move does not complete a line
        """
        return self.calculate_primary_diagonal_line(point, cell_status) == 4

    def calculate_primary_diagonal_line(self, point, cell_status):
        """
        Calculates the length of the primary diagonal parallel line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        return self.calculate_primary_down(point, cell_status) + self.calculate_primary_up(point, cell_status) - 1

    def calculate_primary_down(self, point, cell_status):
        """
        Calculates the length of the primary diagonal parallel line downwards of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y < self.__board.rows and point_copy.x < self.__board.columns \
                and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y += 1
            point_copy.x += 1
            identical_cells += 1

        return identical_cells

    def calculate_primary_up(self, point, cell_status):
        """
        Calculates the length of the primary diagonal parallel line upwards of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y >= 0 and point_copy.x >= 0 \
                and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y -= 1
            point_copy.x -= 1
            identical_cells += 1

        return identical_cells

    def check_secondary_diagonal_line(self, point, cell_status):
        """
        Checks if the last made move completes a secondary diagonal parallel line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: True - the last move completes a line
                 False - the last move does not complete a line
        """
        return self.calculate_secondary_diagonal_line(point, cell_status) == 4

    def calculate_secondary_diagonal_line(self, point, cell_status):
        """
        Calculates the length of the secondary diagonal parallel line
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        return self.calculate_secondary_down(point, cell_status) + self.calculate_secondary_up(point, cell_status) - 1

    def calculate_secondary_down(self, point, cell_status):
        """
        Calculates the length of the secondary diagonal parallel line downwards of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y < self.__board.rows and point_copy.x >= 0 \
                and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y += 1
            point_copy.x -= 1
            identical_cells += 1

        return identical_cells

    def calculate_secondary_up(self, point, cell_status):
        """
        Calculates the length of the secondary diagonal parallel line upwards of the point
        :param point: The point describing the last made move
        :param cell_status: The status of the last occupied cell
        :return: The length of the line
        """
        point_copy = BoardPoint(point.x, point.y)
        identical_cells = 0
        while point_copy.y >= 0 and point_copy.x < self.__board.columns \
                and self.__board[point_copy.y][point_copy.x].status == cell_status:
            point_copy.y -= 1
            point_copy.x += 1
            identical_cells += 1

        return identical_cells

    def reset_board(self):
        """
        Resets the board for a new game
        :return: -
        """
        for row in range(self.__board.rows):
            for column in range(self.__board.columns):
                self.__board[row][column].reset()

        for row in range(self.__board.rows):
            self.board.column_height[row] = 0
