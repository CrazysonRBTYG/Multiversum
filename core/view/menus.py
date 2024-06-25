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
        BACKGROUND_IMAGE.render(where, BACKGROUND_IMAGE_COORDS)
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
            temp = self._next_event
            self._next_event = None
            return temp


class GameMenu:
    """
    Шаблон меню, отображающегося во время игры
    """

    def __init__(self, chosen_char: int):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._char_cell: Image = Image(*CHAR_CELL_COORDS, CHARACTERS[chosen_char]["path"], CHAR_CELL_TRANSFORM_RESOLUTION)
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
        self._stats_font = pygame.font.Font(FONT, RESOLUTION[0] * 64 // 1920)
        self._game_over_font = pygame.font.Font(FONT, RESOLUTION[0] * 150 // 1920)
        self._game_over = Image(0, 0, "core/view/assets/game/game_end.png", RESOLUTION)

    
    def draw(self, where: pygame.Surface, board: list[list[int]], score: int, timer: str, is_game_over: bool, record: int,
             ability_status: int, ability_cd):
        """
        Визуальное отображение всех компонентов
        """
        
        BACKGROUND_IMAGE.render(where, BACKGROUND_IMAGE_COORDS)
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
        if ability_cd == None:
            ability_text = self._stats_font.render("Нет :(", False, RED)
        else:
            if ability_status == ABILITY_READY:
                ability_text = self._stats_font.render("Готова!", False, GREEN)
            elif ability_status == ABILITY_ACTIVE:
                ability_text = self._stats_font.render("Активно", False, GREEN)
            elif ability_status == ABILITY_ON_CD:
                ability_text = self._stats_font.render(str(ability_cd), False, RED)
        ability_text_rect = ability_text.get_rect(center=(self._char_cell.get_rect().centerx,
                                                          self._char_cell.get_rect().top + CHAR_CELL_TRANSFORM_RESOLUTION[1] // 4))
        record_text = self._stats_font.render("{:,}".format(record).replace(",", "."), False, (0, 0, 0))
        record_text_rect = record_text.get_rect(center=(self._char_cell.get_rect().centerx,
                                                        self._char_cell.get_rect().top + CHAR_CELL_TRANSFORM_RESOLUTION[1] // 8))
        score_text = self._stats_font.render("{:,}".format(score).replace(",", "."), False, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(self._stats_cell.get_rect().centerx, 
                                                    self._stats_cell.get_rect().bottom - STATS_CELL_TRANSFORM_RESOLUTION[1] // 3))
        timer_text = self._stats_font.render(f"Время: {timer}", False, (0, 0, 0))
        timer_text_rect = timer_text.get_rect(center=(self._stats_cell.get_rect().centerx, 
                                                    self._stats_cell.get_rect().top + STATS_CELL_TRANSFORM_RESOLUTION[1] // 3))
        where.blit(ability_text, ability_text_rect)
        where.blit(record_text, record_text_rect)
        where.blit(score_text, score_text_rect)
        where.blit(timer_text, timer_text_rect)
        if is_game_over:
            score2_text = self._game_over_font.render("{:,}".format(score).replace(",", "."), False, (0, 0, 0))
            score2_text_rect = score2_text.get_rect(center=(RESOLUTION[0] * 960 // 1920, RESOLUTION[1] * 527 // 1080))
            back_text = self._stats_font.render("ESC - назад", False, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=(RESOLUTION[0] * 960 // 1920, RESOLUTION[1] * 775 // 1080))
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


class CollectionMenu:
    def __init__(self, available_characters: list[int], chosen_character: int):
        self._available_characters: list[int] = available_characters
        self._characters_images: list[Image] = [Image(*CHARACTER_IMAGE_COORDS, CHARACTERS[char]["path"],
                                                      CHARACTER_IMAGE_TRANSFORM_RESOLUTION)
                                                      for char in available_characters]
        self._characters_names: list[str] = [CHARACTERS[char]["name"] for char in available_characters]
        for i in range(len(self._available_characters)):
            if self._available_characters[i] == chosen_character:
                self._pointer: int = i
        self._font: pygame.font.Font = pygame.font.Font(FONT, RESOLUTION[0] * 64 // 1920)
        self._text_rect = (self._characters_images[0].get_rect().centerx, 
                           self._characters_images[0].get_rect().top + CHAR_CELL_TRANSFORM_RESOLUTION[1] // 8)
        self._choose_button_on: Button = Button(CHOOSE_BUTTON_FUNC, *CHOOSE_BUTTON_ON_COORDS,
                                                CHOOSE_BUTTON_ON_PATH, CHOOSE_BUTTON_TRANSFORM_RESOLUTION)
        self._choose_button_on_animations: pygame.sprite.Group = pygame.sprite.Group(self._choose_button_on)
        self._choose_button_off: Image = Image(*CHOOSE_BUTTON_OFF_COORDS, CHOOSE_BUTTON_OFF_PATH, 
                                               CHOOSE_BUTTON_TRANSFORM_RESOLUTION)
        self._left_button_on: Button = Button(LEFT_BUTTON_FUNC, *LEFT_BUTTON_ON_COORDS,
                                              LEFT_BUTTON_ON_PATH, MOVE_BUTTONS_TRANSFORM_RESOLUTION)
        self._left_button_on_animations: pygame.sprite.Group = pygame.sprite.Group(self._left_button_on)
        self._left_button_off: Image = Image(*LEFT_BUTTON_OFF_COORDS, LEFT_BUTTON_OFF_PATH,
                                             MOVE_BUTTONS_TRANSFORM_RESOLUTION)
        self._right_button_on: Button = Button(RIGHT_BUTTON_FUNC, *RIGHT_BUTTON_ON_COORDS,
                                               RIGHT_BUTTON_ON_PATH, MOVE_BUTTONS_TRANSFORM_RESOLUTION)
        self._right_button_on_animations: pygame.sprite.Group = pygame.sprite.Group(self._right_button_on)
        self._right_button_off: Image = Image(*RIGHT_BUTTON_OFF_COORDS, RIGHT_BUTTON_OFF_PATH, 
                                              MOVE_BUTTONS_TRANSFORM_RESOLUTION)
        self._buttons: list[Button] = [self._choose_button_on, self._left_button_on, self._right_button_on]
        self._are_all_animations_ended: bool = False
        self._is_choose_button_clicked: bool = False
        self._next_event = None

    def draw(self, where: pygame.Surface, chosen_character: int):
        """
        Визуальное отображение всех компонентов
        """

        BACKGROUND_IMAGE.render(where, BACKGROUND_IMAGE_COORDS)
        color = BLACK
        if self._available_characters[self._pointer] == chosen_character:
            self._choose_button_off.draw(where)
            self._choose_button_on.disabled = True
            color = GREEN
        else:
            self._choose_button_on.disabled = False
            self._choose_button_on_animations.draw(where)
            self._choose_button_on_animations.update(speed=COLLECTION_MENU_BUTTON_CLICK_SPEED)
        if self._pointer == 0:
            self._left_button_off.draw(where)
            self._left_button_on.disabled = True
        else:
            self._left_button_on.disabled = False
            self._left_button_on_animations.draw(where)
            self._left_button_on_animations.update(speed=COLLECTION_MENU_BUTTON_CLICK_SPEED)
        if self._pointer == len(self._available_characters) - 1:
            self._right_button_off.draw(where)
            self._right_button_on.disabled = True
        else:
            self._right_button_on.disabled = False
            self._right_button_on_animations.draw(where)
            self._right_button_on_animations.update(speed=COLLECTION_MENU_BUTTON_CLICK_SPEED)
        is_cursor_on_button: bool = False
        is_any_button_animating: bool = True
        for but in self._buttons:
            if but.rect.collidepoint(pygame.mouse.get_pos()) and but.disabled == False:
                is_cursor_on_button = True
            if but.is_animating:
                is_any_button_animating = False
        self._are_all_animations_ended = is_any_button_animating
        if is_cursor_on_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._characters_images[self._pointer].draw(where)
        character_name_text = self._font.render(self._characters_names[self._pointer], False, color)
        character_name_text_rect = character_name_text.get_rect(center=self._text_rect)
        where.blit(character_name_text, character_name_text_rect)
        pygame.display.flip()
    
    def button_click(self, click_pos: tuple[int, int]):
        """
        Нажатие на кнопку и получение следующего события после него
        """
        if self._choose_button_on.rect.collidepoint(click_pos):
            if self._choose_button_on.disabled == False:
                self._choose_button_on.click()
                self._is_choose_button_clicked = True
                self._next_event = self._choose_button_on.func(self._pointer, self._available_characters)
        for but in [self._left_button_on, self._right_button_on]:
            if but.rect.collidepoint(click_pos):
                if but.disabled == False:
                    but.click()
                    self._is_choose_button_clicked = True
                    self._next_event = but.func(self._pointer)
    
    def do(self):
        """
        Возврат события после нажатия на кнопку (если нажата)
        """

        if self._is_choose_button_clicked and self._are_all_animations_ended:
            self._is_choose_button_clicked = False
            temp = self._next_event
            self._next_event = None
            if type(temp) == int:
                self._pointer = temp
            return temp


class Shop:
    def __init__(self):
        self._banner = Image(RESOLUTION[0] * 496 // 1920, RESOLUTION[1] * 141 // 1080,
                             CHARACTERS[CURRENT_BANNER_CHAR]["banner-path"], (RESOLUTION[0] * 928 // 1920, RESOLUTION[1] * 600 // 1080))
        self._spin_button_on = Button(SPIN_BUTTON_FUNC, *SPIN_BUTTON_ON_COORDS, 
                                      SPIN_BUTTON_ON_PATH, SPIN_BUTTON_TRANSFORM_RESOLUTION)
        self._spin_button_off = Image(*SPIN_BUTTON_OFF_COORDS, SPIN_BUTTON_OFF_PATH, SPIN_BUTTON_TRANSFORM_RESOLUTION)
        self._font = pygame.font.Font(FONT, RESOLUTION[0] * 29 // 1920)
        self._font_rect = (RESOLUTION[0] * 585 // 1920, RESOLUTION[1] * 684 // 1080)
        self._stats_font = pygame.font.Font(FONT, RESOLUTION[0] * 96 // 1920)
        self._money_font_rect = (RESOLUTION[0] * 12 // 1920, RESOLUTION[1] * 1075 // 1080)
        self._percents_font_rect = (RESOLUTION[0] * 12 // 1920, RESOLUTION[1] * 1000 // 1080)
        self._animations: pygame.sprite.Group = pygame.sprite.Group(self._spin_button_on)
        self._is_spin_button_clicked: bool = False
        self._all_animations_ended: bool = False
    
    def draw(self, where: pygame.Surface, money_value: int, available_characters: list[int], chance):
        BACKGROUND_IMAGE.render(where, BACKGROUND_IMAGE_COORDS)
        is_but_animating: bool = False
        self._banner.draw(where)
        self._price_text = self._font.render("{:,}".format(SPIN_COST).replace(",", "."), False, BLACK)
        self._price_text_rect = self._price_text.get_rect(center=self._font_rect)
        self._money_text = self._stats_font.render("{:,}".format(money_value).replace(",", "."), False, WHITE)
        self._money_text_rect = self._money_text.get_rect(bottomleft=self._money_font_rect)
        if chance <= 0.3:
            percents_color = RED
        elif chance <= 0.7:
            percents_color = YELLOW
        else:
            percents_color = GREEN
        self._percents_text = self._stats_font.render('{:.2%}'.format(chance), False, percents_color)
        self._percents_text_rect = self._percents_text.get_rect(bottomleft=self._percents_font_rect)
        where.blit(self._money_text, self._money_text_rect)
        where.blit(self._price_text, self._price_text_rect)
        if CURRENT_BANNER_CHAR in available_characters:
            self._spin_button_off.draw(where)
            self._spin_button_on.disabled = True
        else:
            where.blit(self._percents_text, self._percents_text_rect)
            self._animations.draw(where)
            self._animations.update(speed=SHOP_MENU_BUTTON_CLICK_SPEED)
        if self._spin_button_on.rect.collidepoint(pygame.mouse.get_pos()) and self._spin_button_on.disabled == False:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self._spin_button_on.is_animating:
            is_but_animating = True
        self._all_animations_ended = is_but_animating
        pygame.display.flip()
    
    def button_click(self, click_pos: tuple[int, int]):
        """
        Нажатие на кнопку и получение следующего события после него
        """
        if self._spin_button_on.rect.collidepoint(click_pos):
            if self._spin_button_on.disabled == False:
                self._spin_button_on.click()
                self._is_spin_button_clicked = True
                self._next_event = self._spin_button_on.func
        
    def do(self):
        if self._is_spin_button_clicked and self._all_animations_ended:
            self._is_any_button_clicked = False
            temp = self._next_event
            self._next_event = None
            return temp