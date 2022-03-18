"""
    Module which contains the implementation of the Console User Interface
"""
from services.game_service import GameServices, GameOutcome
from enum import IntEnum
from random import randint


class GameState(IntEnum):
    ROLLING = 0,
    PLAYING = 1,
    GAME_OVER = 2


class Console:
    def __init__(self, game_service: GameServices, ai):
        self.__game_service = game_service
        self.__ai = ai
        self.__game_state = GameState.ROLLING
        self.__starting_player = -1
        self.__game_finished = False

    @staticmethod
    def player1_roll():
        roll = randint(0, 101)
        print('Player 1 rolls ' + str(roll))
        return roll

    @staticmethod
    def player2_roll():
        roll = randint(0, 101)
        print('Player 2 rolls ' + str(roll))
        return roll

    def roll(self):
        player1_roll = self.player1_roll()
        player2_roll = self.player2_roll()
        if player1_roll >= player2_roll:
            print('Player 1 goes first!\n')
            self.__starting_player = 1
        else:
            print('Player 2 goes first!\n')
            self.__starting_player = 2
        self.__game_state = GameState.PLAYING

    def player1_move(self):
        column = self.get_column()
        return self.__game_service.make_player1_move(column)

    @staticmethod
    def get_column():
            return int(input('On which column would you like to place?\n')) - 1

    def player2_move(self):
        column = self.__ai.make_move(self.__game_service)
        return self.__game_service.make_player2_move(column)

    def is_game_over(self, point, player):
        if self.__game_service.is_game_over(point, player) == GameOutcome.PLAYER1_WIN:
            print('Player 1 wins!')
            return True
        elif self.__game_service.is_game_over(point, player) == GameOutcome.PLAYER2_WIN:
            print('Player 2 wins!')
            return True
        elif self.__game_service.is_game_over(point, player) == GameOutcome.DRAW:
            print('Game is a draw')
            return True
        return False

    def print_board(self):
        print(str(self.__game_service.board) + '\n\n\n\n')

    def game_loop(self):
        if self.__starting_player == 1:
            while True:
                try:
                    self.print_board()
                    point = self.player1_move()
                    if self.is_game_over(point, 1):
                        self.__game_state = GameState.GAME_OVER
                        break
                    self.print_board()
                    point = self.player2_move()
                    if self.is_game_over(point, 2):
                        self.__game_state = GameState.GAME_OVER
                        break
                    self.print_board()
                except Exception as e:
                    print(e)
        elif self.__starting_player == 2:
            while True:
                try:
                    self.print_board()
                    point = self.player2_move()
                    if self.is_game_over(point, 2):
                        self.__game_state = GameState.GAME_OVER
                        break
                    self.print_board()
                    point = self.player1_move()
                    if self.is_game_over(point, 1):
                        self.__game_state = GameState.GAME_OVER
                        break
                    self.print_board()
                except Exception as e:
                    print(e)
        else:
            raise Exception('Invalid player!')

    def choose_replay(self):
        option = input('Would you like to replay?Y for yes, N for no\n')
        post_game_options = {
            'Y': self.replay_game,
            'y': self.replay_game,
            'N': self.end_game,
            'n': self.end_game
        }
        post_game_options[option]()

    def replay_game(self):
        self.__game_state = GameState.ROLLING
        self.__game_service.reset_board()

    def end_game(self):
        self.__game_finished = True

    def run_application(self):
        state_options = {
            0: self.roll,
            1: self.game_loop,
            2: self.choose_replay
        }

        while not self.__game_finished:
            state_options[self.__game_state.value]()
