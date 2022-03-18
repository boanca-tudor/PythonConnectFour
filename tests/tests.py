import unittest
from repos.board import Board, BoardType, BoardPoint
from domain.cell import CellStatus, Cell
from services.game_service import GameServices, MoveOutsideBoundsException, GameOutcome
from AI.random import RandomAI
from AI.basic import BasicAI


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.normal_board = Board(BoardType.NORMAL)
        self.big_board = Board(BoardType.BIG)
        self.small_board = Board(BoardType.SMALL)

    def testBoardCreation(self):
        self.assertEqual(self.normal_board.columns, 7)
        self.assertEqual(self.normal_board.rows, 6)

        self.assertEqual(self.big_board.columns, 9)
        self.assertEqual(self.big_board.rows, 7)

        self.assertEqual(self.small_board.columns, 5)
        self.assertEqual(self.small_board.rows, 4)

    def testIfEmptyAtCreation(self):
        for row in range(self.normal_board.rows):
            for column in range(self.normal_board.columns):
                self.assertEqual(self.normal_board[row][column].status, CellStatus.EMPTY)

        for row in range(self.big_board.rows):
            for column in range(self.big_board.columns):
                self.assertEqual(self.big_board[row][column].status, CellStatus.EMPTY)

        for row in range(self.small_board.rows):
            for column in range(self.small_board.columns):
                self.assertEqual(self.small_board[row][column].status, CellStatus.EMPTY)

    def testColumnHeightAtCreation(self):
        self.assertEqual(len(self.normal_board.column_height), self.normal_board.columns)
        for index in range(self.normal_board.rows):
            self.assertEqual(self.normal_board.column_height[index], 0)

        self.assertEqual(len(self.big_board.column_height), self.big_board.columns)
        for index in range(self.big_board.rows):
            self.assertEqual(self.big_board.column_height[index], 0)

        self.assertEqual(len(self.small_board.column_height), self.small_board.columns)
        for index in range(self.small_board.rows):
            self.assertEqual(self.small_board.column_height[index], 0)


class TestBoardPoint(unittest.TestCase):
    def setUp(self):
        self.point = BoardPoint(1, 2)

    def testInit(self):
        self.assertEqual(self.point.x, 1)
        self.assertEqual(self.point.y, 2)


class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell()

    def testDefaultCell(self):
        self.assertEqual(self.cell.status, CellStatus.EMPTY)

    def testOccupyPlayer1(self):
        self.cell.occupy_by_player1()
        self.assertEqual(self.cell.status, CellStatus.OCCUPIED_BY_PLAYER1)

    def testOccupyPlayer2(self):
        self.cell.occupy_by_player2()
        self.assertEqual(self.cell.status, CellStatus.OCCUPIED_BY_PLAYER2)

    def tearDown(self):
        pass


class ServiceAITests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.services = GameServices(self.board)
        self.basic_ai = BasicAI()
        self.random_ai = RandomAI()

    def testMarkMove(self):
        self.services.mark_move(1)
        self.assertEqual(self.board.column_height[1], 1)

    def testMakePlayerMove(self):
        with self.assertRaises(MoveOutsideBoundsException):
            self.services.make_player1_move(10)
        self.services.make_player1_move(1)
        self.services.make_player2_move(1)
        self.assertEqual(self.board.column_height[1], 2)
        self.assertEqual(self.board[5][1].status, CellStatus.OCCUPIED_BY_PLAYER1)
        self.assertEqual(self.board[4][1].status, CellStatus.OCCUPIED_BY_PLAYER2)

    def testHorizontalLineCalculation(self):
        self.services.make_player1_move(1)
        self.services.make_player1_move(2)
        point = self.services.make_player1_move(3)
        self.assertEqual(self.services.calculate_horizontal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), 3)
        self.assertEqual(self.services.check_horizontal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), False)
        self.services.make_player1_move(4)
        self.assertEqual(self.services.is_game_over(point, 1), GameOutcome.PLAYER1_WIN)

    def testVerticalLineCalculation(self):
        point = self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        self.assertEqual(self.services.calculate_vertical_line(point, CellStatus.OCCUPIED_BY_PLAYER1), 3)
        self.assertEqual(self.services.check_vertical_line(point, CellStatus.OCCUPIED_BY_PLAYER1), False)
        self.services.make_player1_move(1)
        self.assertEqual(self.services.is_game_over(point, 1), GameOutcome.PLAYER1_WIN)

    def testPrimaryLineCalculation(self):
        self.services.make_player1_move(4)
        self.services.make_player2_move(3)
        self.services.make_player2_move(2)
        self.services.make_player2_move(2)
        self.services.make_player2_move(1)
        self.services.make_player2_move(1)
        self.services.make_player2_move(1)
        point = self.services.make_player1_move(3)
        self.services.make_player1_move(2)
        self.assertEqual(self.services.calculate_primary_diagonal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), 3)
        self.assertEqual(self.services.check_primary_diagonal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), False)
        self.services.make_player1_move(1)
        self.assertEqual(self.services.is_game_over(point, 1), GameOutcome.PLAYER1_WIN)

    def testSecondaryLineCalculation(self):
        self.services.make_player1_move(1)
        self.services.make_player2_move(2)
        self.services.make_player2_move(3)
        self.services.make_player2_move(3)
        self.services.make_player2_move(4)
        self.services.make_player2_move(4)
        self.services.make_player2_move(4)
        point = self.services.make_player1_move(2)
        self.services.make_player1_move(3)
        self.assertEqual(self.services.calculate_secondary_diagonal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), 3)
        self.assertEqual(self.services.check_secondary_diagonal_line(point, CellStatus.OCCUPIED_BY_PLAYER1), False)
        self.services.make_player1_move(4)
        self.assertEqual(self.services.is_game_over(point, 1), GameOutcome.PLAYER1_WIN)

    def testReset(self):
        self.services.make_player1_move(1)
        self.services.make_player2_move(2)
        self.services.make_player2_move(3)
        self.services.make_player2_move(3)
        self.services.make_player2_move(4)
        self.services.make_player2_move(4)
        self.services.make_player2_move(4)
        self.services.make_player1_move(2)
        self.services.make_player1_move(3)
        self.services.reset_board()
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                self.assertEqual(self.board[i][j].status, CellStatus.EMPTY)

    def testFullBoard(self):
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                point = self.services.make_player1_move(j)

        self.assertEqual(self.services.is_game_over(point, 1), GameOutcome.DRAW)

    def testRandomAI(self):
        for i in range(self.board.rows):
            self.services.make_player1_move(3)
            self.services.make_player1_move(4)
        for i in range(20):
            column = self.random_ai.make_move(self.services)
            self.assertNotEqual(column, 3)
            self.assertNotEqual(column, 4)

        column = self.random_ai.make_move(self.services)
        self.services.make_player2_move(column)

        self.assertEqual(self.board[5][column].status, CellStatus.OCCUPIED_BY_PLAYER2)

    def testBasicAIWin(self):
        self.services.make_player2_move(1)
        self.services.make_player2_move(2)
        self.services.make_player2_move(3)
        column = self.basic_ai.make_move(self.services)
        self.assertIn(column, [0, 4])

        self.services.reset_board()

        self.services.make_player2_move(1)
        self.services.make_player2_move(1)
        self.services.make_player2_move(1)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 1)

        self.services.reset_board()

        self.services.make_player2_move(4)
        self.services.make_player1_move(3)
        self.services.make_player1_move(2)
        self.services.make_player1_move(2)
        self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        self.services.make_player2_move(3)
        self.services.make_player2_move(2)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 1)

        self.services.reset_board()

        self.services.make_player2_move(1)
        self.services.make_player1_move(2)
        self.services.make_player1_move(3)
        self.services.make_player1_move(3)
        self.services.make_player1_move(4)
        self.services.make_player1_move(4)
        self.services.make_player1_move(4)
        self.services.make_player2_move(2)
        self.services.make_player2_move(3)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 4)

    def testBasicAIBlock(self):
        self.services.make_player1_move(1)
        self.services.make_player1_move(2)
        self.services.make_player1_move(3)
        column = self.basic_ai.make_move(self.services)
        self.assertIn(column, [0, 4])

        self.services.reset_board()

        self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        self.services.make_player1_move(1)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 1)

        self.services.reset_board()

        self.services.make_player1_move(4)
        self.services.make_player2_move(3)
        self.services.make_player2_move(2)
        self.services.make_player2_move(2)
        self.services.make_player1_move(1)
        self.services.make_player2_move(1)
        self.services.make_player2_move(1)
        self.services.make_player1_move(3)
        self.services.make_player1_move(2)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 1)

        self.services.reset_board()

        self.services.make_player1_move(1)
        self.services.make_player2_move(2)
        self.services.make_player2_move(3)
        self.services.make_player2_move(3)
        self.services.make_player1_move(4)
        self.services.make_player2_move(4)
        self.services.make_player2_move(4)
        self.services.make_player1_move(2)
        self.services.make_player1_move(3)
        column = self.basic_ai.make_move(self.services)
        self.assertEqual(column, 4)

