import pygame, sys
from pygame.locals import *
from tkinter import *
import numpy as np
import firebase_admin
from firebase_admin import credentials, auth, db
import winsound
import time

board_size = 15
empty = 0
black_stone = 1
white_stone = 2
last_b_stone = 3
last_a_stont = 4
tie = 100

bg_color = (128, 128, 128)
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

window_width = 800
window_height = 500
board_width = 500
grid_size = 30

size_of_board = 498
symbol_size=(window_width/3-window_height/8)/2-20
Green_color = '#7BC043'
symbol_recent = '#7df924'

board_size = 15
empty = 0
black_stone = 1
white_stone = 2
last_b_stone = 3
last_a_stont = 4
tie = 100
game=1
fps = 60
fps_clock = pygame.time.Clock()
game=False

def main():
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("N-mok game")
    surface.fill(bg_color)

    play_game = Tic_Tac_Toe(surface)

    menu = Menu(surface)
    while True:
        run_game(surface, play_game, menu)
        menu.is_continue(play_game)

def run_game(surface, game, menu):
    game.init_game()
    ##start_time= int(time.time())
    ##remain_time=0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                menu.terminate()
            elif event.type == MOUSEBUTTONUP:
                if not game.check_board(event.pos):
                    if menu.check_rect(event.pos, game):
                        game.init_game()
        
        if game.gameover:
            return
       ##remain_time=10-(int(time.time())-start_time)
        ##if remain_time<=0:
          ##  game.time_over()
            
        
        pygame.display.update()
        fps_clock.tick(fps)

def Get_game():
    game
    return Cha_game(game)

def Cha_game(game):
    game=not game
    return game

class Rule(object):
    def __init__(self, board):
        self.board = board

    def is_invalid(self, x, y):
        return (x < 0 or x >= board_size or y < 0 or y >= board_size)
    
    def is_gameover(self, x, y, stone):
        x1, y1 = x, y
        list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        list_dy = [0, 0, -1, 1, -1, 1, -1, 1]
        for i in range(0, len(list_dx), 2):
            cnt = 1
            for j in range(i, i + 2):
                dx, dy = list_dx[j], list_dy[j]
                x, y = x1, y1
                while True:
                    x, y = x + dx, y + dy
                    if self.is_invalid(x, y) or self.board[y][x] != stone:
                        break
                    else:
                        cnt += 1
            if cnt >= 5:
                return cnt
        return cnt


class Omok(object):
    def __init__(self, surface):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.set_image_font()
        self.is_show = True

    def init_game(self):
        self.turn  = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        self.init_board()
        self.coords = []
        self.redos = []
        self.id = 1
        self.gameover = False

    def set_image_font(self):
        black_img = pygame.image.load('image/black.png')
        white_img = pygame.image.load('image/white.png')
        self.last_w_img = pygame.image.load('image/white_a.png')
        self.last_b_img = pygame.image.load('image/black_a.png')
        self.board_img = pygame.image.load('image/board.png')
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
        self.white_img = pygame.transform.scale(white_img, (grid_size, grid_size))

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    def draw_image(self, img_index, x, y):
        img = [self.black_img, self.white_img, self.last_b_img, self.last_w_img]
        self.surface.blit(img[img_index], (x, y))

    def show_number(self, x, y, stone, number):
        colors = [white, black, red, red]
        color = colors[stone]
        self.menu.make_text(self.font, str(number), color, None, y + 15, x + 15, 1)

    def hide_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.draw_image(i % 2, x, y)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2 + 2, x, y)

    def show_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.show_number(x, y, i % 2, i + 1)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2, x, y)
            self.show_number(x, y, i % 2 + 2, i + 1)

    def draw_stone(self, coord, stone, increase):
        x, y = self.get_point(coord)
        self.board[y][x] = stone
        self.hide_numbers()
        if self.is_show:
            self.show_numbers()
        self.id += increase
        self.turn = 3 - self.turn
        
    def undo(self):
        if not self.coords:
            return            
        self.draw_board()
        coord = self.coords.pop()
        self.redos.append(coord)
        self.draw_stone(coord, empty, -1)

    def undo_all(self):
        if not self.coords:
            return
        self.id = 1
        self.turn  = black_stone
        while self.coords:
            coord = self.coords.pop()
            self.redos.append(coord)
        self.init_board()
        self.draw_board()

    def redo(self):
        if not self.redos:
            return
        coord = self.redos.pop()
        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)

    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size + 25, y * grid_size + 25))

    def get_coord(self, pos):
        for coord in self.pixel_coords:
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if rect.collidepoint(pos):
                return coord
        return None

    def get_point(self, coord):
        x, y = coord
        x = (x - 25) // grid_size
        y = (y - 25) // grid_size
        return x, y
                                 
    def check_board(self, pos):
        coord = self.get_coord(pos)
        if not coord:
            return False
        x, y = self.get_point(coord)
        if self.board[y][x] != empty:
            return True

        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)
        if self.check_gameover(coord, 3 - self.turn):
            self.gameover = True
        if len(self.redos):
            self.redos = []
        return True

    def check_gameover(self, coord, stone):
        x, y = self.get_point(coord)
        if self.id > board_size * board_size:
            self.show_winner_msg(stone)
            return True
        elif 5 <= self.rule.is_gameover(x, y, stone):
            self.show_winner_msg(stone)
            return True
        return False

    def show_winner_msg(self, stone):
        for i in range(3):
            self.menu.show_msg(stone)
            pygame.display.update()
            pygame.time.delay(200)
            self.menu.show_msg(empty)
            pygame.display.update()
            pygame.time.delay(200)
        self.menu.show_msg(stone)
        
class Menu(object):

    def __init__(self, surface):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.surface = surface
        self.draw_menu()
        
    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.Change_Game = self.make_text(self.font, 'Change Game', blue, None, top-180,left)
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 150, left)
        self.uall_rect = self.make_text(self.font, 'Undo All', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)
        self.show_rect = self.make_text(self.font, 'Hide Number  ', blue, None, top - 60, left)
        self.new_rect = self.make_text(self.font, 'New Game', blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', blue, None, top, left)
        
    def show_msg(self, msg_id):
        msg = {
            empty : '                                    ',
            black_stone: 'Black win!!!',
            white_stone: 'White win!!!',
            tie: 'Tie'
        }
        center_x = window_width - (window_width - board_width) // 2
        self.make_text(self.font, msg[msg_id], black, bg_color, 30, center_x, 1)

    def make_text(self, font, text, color, bgcolor, top, left, position = 0):
        surf = font.render(text, False, color, bgcolor)
        rect = surf.get_rect()
        if position:
            rect.center = (left, top)
        else:    
            rect.topleft = (left, top)
        self.surface.blit(surf, rect)
        return rect

    def show_hide(self, game):
        top, left = window_height - 90, window_width - 200
        if game.is_show:
            self.make_text(self.font, 'Show Number', blue, bg_color, top, left)
            game.hide_numbers()
            game.is_show = False
        else:
            self.make_text(self.font, 'Hide Number  ', blue, bg_color, top, left)
            game.show_numbers()
            game.is_show = True

    def check_rect(self, pos, game):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.show_rect.collidepoint(pos):
            self.show_hide(game)
        elif self.undo_rect.collidepoint(pos):
            game.undo()
        elif self.uall_rect.collidepoint(pos):
            game.undo_all()
        elif self.redo_rect.collidepoint(pos):
            game.redo()
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        elif self.Change_Game.collidepoint(pos):
            self.C_Game()
        return False
    
    def C_Game(self):
        surface = pygame.display.set_mode((window_width, window_height))
        if Get_game()==True:
            play_game=Omok(surface)
            menu = Menu(surface)

            run_game(surface,Omok(surface),Menu(surface))
            self.is_continue(play_game)
        else :
            play_game = Tic_Tac_Toe(surface)
            menu = Menu(surface)
 
            run_game(surface,play_game,Menu(surface))
            self.is_continue(play_game)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def is_continue(self, play_game):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                
                elif event.type == MOUSEBUTTONUP:
                    if (self.check_rect(event.pos, play_game)):
                        return
            
            pygame.display.update()
            fps_clock.tick(fps)    

class Tic_Tac_Toe(object):
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------

    def __init__(self, surface):
        #로그인 해서 불러온 플레이어 정보 출력 테스트\
        '''
        self.default_app = default_app
        print('\n게임이 실행되었습니다.')
        self.user = user
        print('유저 이메일 :', user.email)
        print('유저 UID :', user.uid)
        print('유저 닉네임 :', user.display_name)
        ref = db.reference(user.uid).child('play_game_count')
        self.play_game_count = ref.get()
        print('지금까지의 게임 플레이 수 :', self.play_game_count)
        '''

        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.set_image_font()
        self.is_show = True
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0
        self.draw_count = 0
        self.x_last_grid=0
        self.y_last_grid=0
        self.last_logical=0
        self.logical=0

    def init_game(self):
        self.turn  = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        ###self.init_board()
        ##self.coords = []
        ##self.redos = []
       
        self.gameover=False

    def draw_board(self):
        self.surface.blit(self.board_img,(0,0))
        self.initialize_board()

    def set_image_font(self):
        self.board_img=pygame.image.load('image/tic_background.png')
        self.white=pygame.image.load('image/tic_white.png')
        self.black=pygame.image.load('image/tic_black.png')
        self.l_black=pygame.image.load('image/tic_black_a.png')
        self.l_white=pygame.image.load('image/tic_white_a.png')
        self.small_board=pygame.image.load('image/tic_background_small.png')

    def initialize_board(self):
        for row in range(3):
            for col in range(3):
                self.surface.blit(self.small_board,(row*166,col*166))
                
        self.board_status = np.zeros(shape=(3, 3))
        self.draw_count = 0
        
    def save_grid(self, x_last, y_last):
        self.x_last_grid=x_last
        self.y_last_grid=y_last

    def give_x_grid(self):
        return self.x_last_grid

    def give_y_grid(self):
        return self.y_last_grid

    def save_logical(self, last_logical):
        self.last_logical=last_logical

    def give_logical(self):
        return self.last_logical

    def undo_all(self):
        self.draw_board()
        print(self.draw_count)
        self.player_X_turns=self.player_X_starts
        
            
    def undo(self):
        self.surface.blit(self.small_board,(self.give_x_grid(),self.give_y_grid()))
        self.player_X_turns= not self.player_X_turns
        logical_position=self.give_logical()
        #print(logical_position)
        self.board_status[logical_position[0]][logical_position[1]] = 0
        
        

    def redo(self):
        if self.player_X_turns==False:
            logical_position=self.give_logical()
            self.draw_O(logical_position)
            self.player_X_turns= not self.player_X_turns
            self.board_status[logical_position[0]][logical_position[1]] = -1
        else:
            logical_position=self.give_logical()
            self.draw_X(logical_position)
            self.player_X_turns= not self.player_X_turns
            self.board_status[logical_position[0]][logical_position[1]] = +1
            

    #def show_hide(self)
    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        

    def Count_draw(self):
        self.draw_count= self.draw_count+1

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        self.save_logical(logical_position)
        logical_position = np.array(logical_position)

        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
        self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        self.Count_draw()

    def draw_X(self, logical_position):
        self.save_logical(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
        self.Count_draw()

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            self.menu.show_msg(2)
            pygame.display.update()
            pygame.time.delay(1000)
            self.menu.show_msg(empty)
            ##color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            self.menu.show_msg(1)
            pygame.display.update()
            pygame.time.delay(1000)
            self.menu.show_msg(empty)
            ##color = symbol_O_color
        else:
            self.tie_score += 1
            self.menu.show_msg(tie)
            pygame.display.update()
            pygame.time.delay(1000)
            self.menu.show_msg(empty)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)

        self.reset_board = True

        score_text = 'Click to play again \n'


    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True


    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            #self.increase_user_score()
            print('X wins')
        if self.O_wins:
            #self.increase_user_score()
            print('O wins')
        if self.tie:
            #self.increase_user_score()
            print('Its a tie')

        return gameover

    '''
    def increase_user_score(self) :
        self.play_game_count += 1
        ref = db.reference(self.user.uid)
        ref.update({'play_game_count' : self.play_game_count})
    '''

    def time_over(self):
        if self.player_X_turns==True:
            self.O_Wins=True
            self.display_gameover()
        
        else:
            self.X_wins=True
            self.display_gameover()

    def check_board(self, event):
        x=event[0]
        y=event[1]
        grid_position = [event[0], event[1]]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        
        if(x<=500 and x>=0):
            if(y<=500 and y>=0):
                if self.player_X_turns:
                    if not self.is_grid_occupied(logical_position):
                        winsound.PlaySound("click.wav", winsound.SND_ASYNC)
                        self.draw_X(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = -1
                        self.player_X_turns = not self.player_X_turns
                else:
                    if not self.is_grid_occupied(logical_position):
                        winsound.PlaySound("click.wav", winsound.SND_ASYNC)
                        self.draw_O(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = 1
                        self.player_X_turns = not self.player_X_turns

                # Check if game is concluded
                if self.is_gameover():
                    self.gameover=self.is_gameover()
                    self.display_gameover()
                    # print('Done')

                else:
                    return False
            else:
                return False
        else:
            return False
                
if __name__ == '__main__':
    main()