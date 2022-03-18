"""
    Module that contains the implementation of the basic cell of the board game
"""
from enum import IntEnum
from dataclasses import dataclass


class CellStatus(IntEnum):
    """
        Enum class which holds the possible states of a cell
    """
    EMPTY = 0
    OCCUPIED_BY_PLAYER1 = 1
    OCCUPIED_BY_PLAYER2 = 2


@dataclass
class Cell:
    """
        Class which describes the behaviour and attributes of a cell
    """
    status: CellStatus = CellStatus.EMPTY

    def occupy_by_player1(self):
        """
        Mark the cell as being occupied by the first player
        :return: -
        """
        self.status = CellStatus.OCCUPIED_BY_PLAYER1

    def occupy_by_player2(self):
        """
        Mark the cell as being occupied by the second player(AI)
        :return: -
        """
        self.status = CellStatus.OCCUPIED_BY_PLAYER2

    def reset(self):
        """
        Mark the cell as being empty
        :return: -
        """
        self.status = CellStatus.EMPTY

    def __str__(self):
        status_display = \
        {
            0: ' ',
            1: '1',
            2: '2'
        }
        return status_display[self.status.value]
