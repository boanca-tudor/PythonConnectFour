import pygame
from services.game_service import GameServices, GameOutcome, MoveOutsideBoundsException
from enum import IntEnum, Enum
from sys import exit


class GameState(IntEnum):
    ROLLING = 0,
    PLAYING = 1,
    GAME_OVER = 2


class MaskedSprite(pygame.sprite.Sprite):
    def __init__(self, image_path: str, color, size: int, top_left_x: int, top_left_y: int):
        super().__init__()

        self.rect = pygame.rect.Rect(top_left_x, top_left_y, size, size)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.rect.size)

        self.change_color(color)

    def change_color(self, color):
        color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        color_image.fill(color)
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def draw(self, surface):
        renderer = pygame.sprite.RenderPlain(self)
        renderer.draw(surface)


class PlayerStatus(Enum):
    THINKING = 0,
    MOVING = 1


class PlayerSprite(MaskedSprite):
    def __init__(self, image_path: str, color, size: int, top_left_x: int, top_left_y: int, status: PlayerStatus):
        super().__init__(image_path, color, size, top_left_x, top_left_y)
        self.__status = status

    def update(self):
        if self.__status == PlayerStatus.THINKING:
            self.rect.center = (pygame.mouse.get_pos()[0], 50)


class GUI:
    def __init__(self, game_service: GameServices, ai, rectangle_size: int):
        pygame.init()
        pygame.font.init()
        self.__game_service = game_service
        self.__ai = ai
        self.__rectangle_size = rectangle_size
        self.__game_state = GameState.ROLLING
        self.__starting_player = 1
        self.__turn = 1
        self.__game_finished = False

        # screen creation
        self.__screen_size = [self.__game_service.board.columns * self.__rectangle_size,
                              (self.__game_service.board.rows + 1) * self.__rectangle_size]
        self.__screen = pygame.display.set_mode(self.__screen_size)

        # background creation
        self.__background = pygame.image.load('resources/images/bg1.jpg')
        self.__background = pygame.transform.scale(self.__background, self.__screen_size)

        # sprites creation
        self.__player = PlayerSprite('resources/images/circle.png',
                                     pygame.color.THECOLORS['orangered'],
                                     self.__rectangle_size,
                                     0,
                                     0,
                                     PlayerStatus.THINKING)
        self.__board_sprites = []
        for row in range(self.__game_service.board.rows):
            sprite_list = []
            for column in range(self.__game_service.board.columns):
                sprite = MaskedSprite('resources/images/circle.png',
                                      pygame.color.THECOLORS['white'],
                                      self.__rectangle_size,
                                      column * self.__rectangle_size,
                                      (row + 1) * self.__rectangle_size)
                sprite_list.append(sprite)
            self.__board_sprites.append(sprite_list)

        self.__victory_text = None

    def draw_board(self):
        self.__screen.blit(self.__background, [0, 0])

        for row in range(self.__game_service.board.rows):
            for column in range(self.__game_service.board.columns):
                pygame.draw.rect(self.__screen, pygame.color.THECOLORS['lightblue'],
                                 (column * self.__rectangle_size, (row + 1) * self.__rectangle_size,
                                  self.__rectangle_size, self.__rectangle_size))
                self.__board_sprites[row][column].draw(self.__screen)

        self.__player.draw(self.__screen)

    def is_game_over(self, point, player):
        if self.__game_service.is_game_over(point, player) == GameOutcome.PLAYER1_WIN:
            font = pygame.font.Font(pygame.font.get_default_font(), 64)
            font.set_italic(True)
            self.__victory_text = font.render('Player 1 wins!!', True, pygame.color.THECOLORS['darkgreen'])
            return True
        elif self.__game_service.is_game_over(point, player) == GameOutcome.PLAYER2_WIN:
            font = pygame.font.Font(pygame.font.get_default_font(), 64)
            font.set_italic(True)
            self.__victory_text = font.render('Player 2 wins!!', True, pygame.color.THECOLORS['darkred'])
            return True
        elif self.__game_service.is_game_over(point, player) == GameOutcome.DRAW:
            font = pygame.font.Font(pygame.font.get_default_font(), 64)
            font.set_italic(True)
            self.__victory_text = font.render('Draw!!', True, pygame.color.THECOLORS['yellow'])
            return True
        return False

    def run_application(self):
        while not self.__game_finished:
            self.draw_board()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        point = self.make_player_move(event)
                        if self.is_game_over(point, 1):
                            self.__game_state = GameState.GAME_OVER
                            destination_rectangle = self.__victory_text.get_rect()
                            destination_rectangle.center = (self.__screen_size[0] // 2,
                                                            self.__screen_size[1] // 2)
                            self.__screen.blit(self.__victory_text, destination_rectangle)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            exit(0)

                        column = self.__ai.make_move(self.__game_service)
                        point = self.__game_service.make_player2_move(column)
                        self.__board_sprites[point.y][point.x].change_color(pygame.color.THECOLORS['darkblue'])
                        self.draw_board()
                        if self.is_game_over(point, 2):
                            self.__game_state = GameState.GAME_OVER
                            destination_rectangle = self.__victory_text.get_rect()
                            destination_rectangle.center = (self.__screen_size[0] // 2,
                                                            self.__screen_size[1] // 2)
                            self.__screen.blit(self.__victory_text, destination_rectangle)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            exit(0)
                    except MoveOutsideBoundsException as mobe:
                        print(mobe)

                if event.type == pygame.MOUSEMOTION:
                    self.__player.update()

    def make_player_move(self, event):
        position_x = event.pos[0]
        column = int(position_x // self.__rectangle_size)
        point = self.__game_service.make_player1_move(column)
        self.__board_sprites[point.y][point.x].change_color(pygame.color.THECOLORS['orangered'])
        self.draw_board()
        return point
