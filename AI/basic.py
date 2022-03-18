"""
    Module containing the basic required AI
"""
from services.game_service import GameServices, GameOutcome
from copy import deepcopy
from random import choice


class BasicAI:
    def make_move(self, service: GameServices):
        """
        Picks one of the available columns as a move target
        If it can win, it places on the corresponding column which would be a win
        Otherwise, if it can block, it places on the corresponding column which would be a block
        Otherwise, it picks a random available column
        :param service: The game service
        :return: The index of the column
        """
        base_board = service.board
        available_columns = []
        for index in range(len(service.board.column_height)):
            if service.board.column_height[index] != service.board.rows:
                available_columns.append(index)
        wins = self.simulate_win(service, base_board, available_columns)
        blocks = self.simulate_block(service, base_board, available_columns)
        if len(wins) == 0:
            if len(blocks) == 0:
                self.reset_board(service, base_board)
                return choice(available_columns)
            else:
                self.reset_board(service, base_board)
                return choice(blocks)
        else:
            self.reset_board(service, base_board)
            return choice(wins)

    def simulate_block(self, service, base_board, available_columns):
        """
        Simulates all possible moves and returns a list of possible blocks
        :param service: The game service
        :param base_board: The board in the current moment of the game
        :param available_columns: The available columns for placing
        :return: The list of possible blocks
        """
        possible_wins = []
        for column in available_columns:
            self.replace_board_with_copy(service, base_board)
            point = service.make_player1_move(column)
            if service.is_game_over(point, 1) == GameOutcome.PLAYER1_WIN:
                possible_wins.append(column)

        return possible_wins

    def simulate_win(self, service, base_board, available_columns):
        """
        Simulates all possible moves and returns a list of possible wins
        :param service: The game service
        :param base_board: The board in the current moment of the game
        :param available_columns: The available columns for placing
        :return: The list of possible blocks
        """
        possible_wins = []
        for column in available_columns:
            self.replace_board_with_copy(service, base_board)
            point = service.make_player2_move(column)
            if service.is_game_over(point, 2) == GameOutcome.PLAYER2_WIN:
                possible_wins.append(column)

        return possible_wins

    @staticmethod
    def replace_board_with_copy(service, board):
        """
        Replaces the board of the service with a copy of the given board
        :param service: The game service
        :param board: The board to replace by
        :return: -
        """
        new_board = deepcopy(board)
        service.board = new_board

    @staticmethod
    def reset_board(service, base_board):
        """
        Resets the board of the service back to the base board
        :param service: The game service
        :param base_board: The base board
        :return: -
        """
        service.board = base_board
