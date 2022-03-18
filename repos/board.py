"""
    Module which contains all information related to the implementation of the board
"""
from texttable import Texttable
from enum import Enum
from domain.cell import Cell


class BoardException(Exception):
    """
        Custom exception class for errors regarding the board
    """
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class BoardTypeException(BoardException):
    """
        Subclass of the BoardException class which signals board type errors
    """
    pass


class BoardType(Enum):
    """
        Enum class which holds the type of the board
    """
    NORMAL = 0,
    BIG = 1,
    SMALL = 2


class BoardSizeCreator:
    """
        Class which handles creating the size of the board
    """
    @staticmethod
    def create_normal_size():
        """
        Creates the normal size of the board(7x6)
        :return: Enumeration class containing the normal size of the board
        """
        return Enum('BoardSize', {'ROWS': 6, 'COLUMNS': 7})

    @staticmethod
    def create_big_size():
        """
        Creates the big size of the board(9x7)
        :return: Enumeration class containing the big size of the board
        """
        return Enum('BoardSize', {'ROWS': 7, 'COLUMNS': 9})

    @staticmethod
    def create_small_size():
        """
        Creates the small size of the board(5x4)
        :return: Enumeration class containing the small size of the board
        """
        return Enum('BoardSize', {'ROWS': 4, 'COLUMNS': 5})


class Board:
    """
        Class which describes the behaviour and attributes of the board
    """
    def __init__(self, board_type: BoardType = BoardType.NORMAL):
        self.__type = board_type
        self.__create_size()
        self.__create_board()

    def __create_size(self):
        """
        Creates the size of the board which is represented by the columns and rows properties
        :return: -
        """
        if self.__type == BoardType.NORMAL:
            board_size = BoardSizeCreator.create_normal_size()
        elif self.__type == BoardType.BIG:
            board_size = BoardSizeCreator.create_big_size()
        elif self.__type == BoardType.SMALL:
            board_size = BoardSizeCreator.create_small_size()
        else:
            raise BoardTypeException('Invalid board type!')
        self.__columns = board_size.COLUMNS.value
        self.__rows = board_size.ROWS.value

    def __create_board(self):
        """
        Creates the board itself as a list of list, each list representing a row in the board,
        as well as a list which holds the height of each column - how many cells in the column are occupied by a player
        :return: -
        """
        self.__board = [[Cell() for column in range(self.__columns)]
                        for row in range(self.__rows)]
        self.__column_height = [0 for index in range(self.__columns)]

    @property
    def columns(self):
        return self.__columns

    @property
    def rows(self):
        return self.__rows

    @property
    def column_height(self):
        return self.__column_height

    def __getitem__(self, item):
        """
        Returns the item-th row of the board
        :param item: The index of the row
        :return: The list holding the information of the item-th row of the board
        """
        return self.__board[item]

    def __str__(self):
        """
        Returns the string representation of the board as a text table
        :return: A string containing the current representation of the board
        """
        board = Texttable()
        header = [index + 1 for index in range(self.__columns)]
        board.header(header)

        for row in range(self.__rows):
            row_data = [self.__board[row][column] for column in range(self.__columns)]
            board.add_row(row_data)
        return board.draw()


class BoardPoint:
    """
    A wrapper class for a 2d point on the board
    """
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)
