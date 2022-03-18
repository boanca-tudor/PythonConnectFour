"""
    The entry point of the application
"""
from repos.board import Board
from services.game_service import GameServices
from AI.random import RandomAI
from AI.basic import BasicAI
from UI.console import Console
from UI.gui import GUI

if __name__ == '__main__':
    board = Board()
    services = GameServices(board)
    ai = BasicAI()
    try:
        print('1. Console')
        print('2. GUI')
        ui_type = int(input('Please choose your ui\n'))
    except ValueError as ve:
        print(ve)
    if ui_type == 1:
        ui = Console(services, ai)
    elif ui_type == 2:
        ui = GUI(services, ai, 100)

    ui.run_application()
