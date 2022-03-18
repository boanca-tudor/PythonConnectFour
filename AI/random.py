"""
    Module which holds the implementation of the random AI
"""
from services.game_service import GameServices
from random import choice


class RandomAI:
    def make_move(self, service: GameServices):
        """
        Randomly picks one of the available columns as a move target
        :param service: The game service
        :return: The index of the column
        """
        possible_wins = []
        for index in range(len(service.board.column_height)):
            if service.board.column_height[index] != service.board.rows:
                possible_wins.append(index)

        if len(possible_wins) != 0:
            return choice(possible_wins)

        return -1

