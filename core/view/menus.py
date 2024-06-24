import pygame
import gif_pygame
from view.local_consts import *
from model.local_consts import *
from view.interface_elements import *
from eventmanager.events import *


class MainMenu:
    """
    Шаблон главного меню и всех его функций
    """

    def __init__(self):
        self._background_image: gif_pygame.GIFPygame = gif_pygame.load(BACKGROUND["path"])
        gif_pygame.transform.scale(self._background_image, RESOLUTION)
        self._background_image_pos: tuple[int, int] = BACKGROUND["coords"]
        self._buttons: list[Button] = [
                Button(MAIN_MENU_BUTTONS[i]["func"],
                *MAIN_MENU_BUTTONS[i]["coords"],
                MAIN_MENU_BUTTONS[i]["path"], MAIN_MENU_BUTTONS_TRANSFORM_RESOLUTION) 
                for i in MAIN_MENU_BUTTONS.keys()]
        self._animations: pygame.sprite.Group = pygame.sprite.Group()
        self._are_all_animations_ended: bool = False
        self._is_any_button_clicked: bool = False
        self._next_event: Event = None # Отслеживание нажатой кнопки
        for but in self._buttons:
            self._animations.add(but)
        
    def draw(self, where: pygame.Surface):
        """
        Визуальное отображение всех компонентов
        """

        is_cursor_on_button: bool = False
        is_any_button_animating: bool = True
        for but in self._buttons:
            if but.rect.collidepoint(pygame.mouse.get_pos()):
                is_cursor_on_button = True
            if but.is_animating:
                is_any_button_animating = False
        self._are_all_animations_ended = is_any_button_animating
        if is_cursor_on_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._background_image.render(where, self._background_image_pos)
        self._animations.draw(where)
        self._animations.update(speed=MAIN_MENU_BUTTON_CLICK_SPEED)
        pygame.display.flip()
    
    def button_click(self, click_pos: tuple[int, int]):
        """
        Нажатие на кнопку и получение следующего события после него
        """
        for but in self._buttons:
            if but.rect.collidepoint(click_pos):
                but.click()
                self._next_event = but.func
                self._is_any_button_clicked = True
    
    def do(self) -> Event:
        """
        Возврат события после нажатия на кнопку (если нажата)
        """

        if self._is_any_button_clicked and self._are_all_animations_ended:
            pygame.time.wait(MAIN_MENU_BUTTON_WAIT_AFTER_CLICK) # микро пауза (можно отключить)
            temp = self._next_event
            self._next_event = None
            return temp


class GameMenu:
    """
    Шаблон меню, отображающегося во время игры
    """

    def __init__(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._background_image: gif_pygame.GIFPygame = gif_pygame.load(BACKGROUND["path"])
        gif_pygame.transform.scale(self._background_image, RESOLUTION)
        self._background_image_pos: tuple[int, int] = BACKGROUND["coords"]
        self._char_cell: Image = Image(*CHAR_CELL_COORDS, CHAR_CELL_PATH, CHAR_CELL_TRANSFORM_RESOLUTION)
        self._stats_cell: Image = Image(*STATS_CELL_COORDS, STATS_CELL_PATH, STATS_CELL_TRANSFORM_RESOLUTION)
        self._x_ind = MATCH_CELL_START_COORDS[0]
        self._y_ind = MATCH_CELL_START_COORDS[1]
        self._clicked_match = None
        self.move = None
        self._game_board: list[list[Image]] = []
        self._game_board_colors: list[list[Image]] = []
        for _ in range(MATCH3_ROWS):
            temp = []
            temp2 = []
            for _ in range(MATCH3_COLS):
                temp.append(Image(*(self._x_ind, self._y_ind), MATCH_CELL_PATH, MATCH_CELL_TRANSFORM_RESOLUTION))
                temp2.append(Image(*(self._x_ind, self._y_ind), f"core/view/assets/game/matches/0.png", MATCH_CELL_TRANSFORM_RESOLUTION))
                self._x_ind += MATCH_CELL_W_INC
            self._game_board.append(temp)
            self._game_board_colors.append(temp2)
            self._y_ind += MATCH_CELL_H_INC
            self._x_ind = MATCH_CELL_START_COORDS[0]
        self._stats_font = pygame.font.Font(FONT, 64)
        self._game_over_font = pygame.font.Font(FONT, 150)
        self._game_over = Image(0, 0, "core/view/assets/game/game_end3.png", RESOLUTION)

    
    def draw(self, where: pygame.Surface, board: list[list[int]], score: int, timer: str, is_game_over: bool, record: int):
        """
        Визуальное отображение всех компонентов
        """
        
        self._background_image.render(where, self._background_image_pos)
        self._char_cell.draw(where)
        self._stats_cell.draw(where)
        for y in range(MATCH3_ROWS):
            for x in range(MATCH3_COLS):
                if self._clicked_match == (y, x):
                    self._game_board_colors[y][x].update(f"core/view/assets/game/matches/{board[y][x]}_clicked.png")
                else:
                    self._game_board_colors[y][x].update(f"core/view/assets/game/matches/{board[y][x]}.png")
        for i in range(len(self._game_board)):
            for j in range(len(self._game_board[0])):
                self._game_board[i][j].draw(where)
                self._game_board_colors[i][j].draw(where)
        record_text = self._stats_font.render("{:,}".format(record).replace(",", "."), False, (0, 0, 0))
        record_text_rect = record_text.get_rect(center=(self._stats_cell.get_rect().centerx,
                                                        self._char_cell.get_rect().top + CHAR_CELL_TRANSFORM_RESOLUTION[1] // 8))
        score_text = self._stats_font.render("{:,}".format(score).replace(",", "."), False, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(self._stats_cell.get_rect().centerx, 
                                                    self._stats_cell.get_rect().bottom - STATS_CELL_TRANSFORM_RESOLUTION[1] // 3))
        timer_text = self._stats_font.render(f"Время: {timer}", False, (0, 0, 0))
        timer_text_rect = timer_text.get_rect(center=(self._stats_cell.get_rect().centerx, 
                                                    self._stats_cell.get_rect().top + STATS_CELL_TRANSFORM_RESOLUTION[1] // 3))
        where.blit(record_text, record_text_rect)
        where.blit(score_text, score_text_rect)
        where.blit(timer_text, timer_text_rect)
        if is_game_over:
            score2_text = self._game_over_font.render("{:,}".format(score).replace(",", "."), False, (0, 0, 0))
            score2_text_rect = score2_text.get_rect(center=(960, 527))
            back_text = self._stats_font.render("ESC - назад", False, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=(960, 775))
            self._game_over.draw(where)
            where.blit(score2_text, score2_text_rect)
            where.blit(back_text, back_text_rect)
        pygame.display.flip()
    
    def match_click(self, click_pos: tuple[int, int]):
        for y in range(MATCH3_ROWS):
            for x in range(MATCH3_COLS):
                if self._game_board_colors[y][x].rect.collidepoint(click_pos):
                    if self._clicked_match == (y, x):
                        self._clicked_match = None
                    elif self._clicked_match is not None:
                        self.move = (*self._clicked_match, y, x)
                        self._clicked_match = None
                    else:
                        self._clicked_match = (y, x)
    
    def do(self):
        if self.move is not None:
            return self.move


