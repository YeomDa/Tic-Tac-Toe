import pygame, sys
from pygame.locals import *
from tkinter import *
import numpy as np
import firebase_admin
from firebase_admin import firestore
import winsound
import time
import threading
import lobbyScreen

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

fps = 60
fps_clock = pygame.time.Clock()
current_game=False

class User_Info():
    def __init__(self, user):
        self.user = user
        self.nickname = self.user.display_name
        self.uid = self.user.uid
        
        db = firestore.client()
        db_ref = db.collection(u'user_info').document(self.uid)
        doc = db_ref.get()
        if(doc.exists):
            data_list = doc.to_dict()
            self.total = data_list.get('play_game_count')
            self.win = data_list.get('win_count')
            self.defeat = data_list.get('defeat_count')
            self.tie = data_list.get('tie_count')
        else :
            self.total = 0
            self.win = 0
            self.defeat = 0
            self.tie = 0

def main():
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("N-mok game")
    surface.fill(bg_color)

    play_game = Tic_Tac_Toe(surface)
    #
    menu = Menu(surface)
    while True:
        run_game(surface, play_game, menu)
        menu.is_continue(play_game)
    
def main(title, user):
    user_info = User_Info(user)
    network_game_title = title
    #선공은 방장에게 우선 줍니다
    if(user_info.nickname == title) :
        network_my_turn = True
    else :
        network_my_turn = False

    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(user_info.nickname+"님의 N-mok game")
    surface.fill(bg_color)
    
    play_game = Tic_Tac_Toe(surface, network_game_title, network_my_turn, user_info)

    if(network_game_title != None) :
        menu = Network_Menu(surface,user)
    else:
        menu = Menu(surface)

    while True:
        run_game(surface, play_game, menu)

def main2(title, user):
    user_info = User_Info(user)
    network_game_title = title
    #선공은 방장에게 우선 줍니다
    if(user_info.nickname == title) :
        network_my_turn = True
    else :
        network_my_turn = False

    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(user_info.nickname+"님의 N-mok game")
    surface.fill(bg_color)

    #play_game = Tic_Tac_Toe(surface, network_game_title, network_my_turn, user_info)
    play_game = Omok(surface,surface)

    if(network_game_title != None) :
        menu = Network_Menu(surface)
    else:
        menu = Menu(surface)

    while True:
        run_game(surface, play_game, menu)

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
    return Cha_game(current_game)

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

class Network_Menu(object): #네트워크 대전일때의 메뉴

    def __init__(self, surface,user):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.surface = surface
        self.user = user
        self.draw_menu()
        
    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 150, left)
        self.uall_rect = self.make_text(self.font, 'Undo All', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)
        self.show_rect = self.make_text(self.font, 'Hide Number  ', blue, None, top - 60, left)
        self.goto_rect = self.make_text(self.font, 'go Lobby', blue, None, top -30, left)
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
        #if self.new_rect.collidepoint(pos):
        #    return True

        if self.show_rect.collidepoint(pos):
            self.show_hide(game)
        elif self.undo_rect.collidepoint(pos):
            game.undo()
        elif self.uall_rect.collidepoint(pos):
            game.undo_all()
        elif self.redo_rect.collidepoint(pos):
            game.redo()
        elif self.goto_rect.collidepoint(pos):
            self.gotoLobby(self.user)
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        return False

    def gotoLobby(self,user):
        #self.user = user
        pygame.quit()
        
        lobby = lobbyScreen.Lobby(user)
        lobby.mainloop()

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

    def __init__(self, surface, network_game_title=None, network_my_turn=None, user_info=None):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        #self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.set_image_font()
        self.is_show = True
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.font = pygame.font.Font("freesansbold.ttf", 30)
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
        self.x_last_grid=[]
        self.y_last_grid=[]
        self.last_logical=0
        self.logical=0
        self.is_show=True
        self.logical_list=[]
        

        print('리스너 부착 진입 전')
        if(network_game_title != None) :
            self.menu = Network_Menu(surface,user=None)
        else:
            self.menu = Menu(surface)
    
        #네트워크 대전이라면,
        if(network_game_title != None) :
            self.isHost = network_my_turn #첫 시작하는 사람은 호스트입니다
            self.db = firestore.client()
            self.user_info = user_info
            self.network_my_turn = network_my_turn
            self.network_game_title = network_game_title
            print('리스너 부착 진입')
            callback_done = threading.Event()
            def on_snapshot(doc_snapshot, changes, read_time):
                #print('현재 내 턴은? ->', self.network_my_turn)
                
                for doc in doc_snapshot:
                    list = doc.to_dict()
                    turn = list.get('turn')
                    landing_position_x = list.get('landing_position_x')
                    landing_position_y = list.get('landing_position_y')
                    if(turn!=None and landing_position_x!=None and landing_position_y!=None) :
                        if(self.network_my_turn) :
                            self.network_my_turn = False
                            return
                        
                        logical_position = np.array([landing_position_x, landing_position_y], dtype=int)
                        if(turn == 'Black') :
                            self.landing_black(logical_position)
                        else :
                            self.landing_white(logical_position)
                        self.network_my_turn = True #상대방의 착수를 감지하고 적용하였으니, 이제 나의 턴입니다
                            
                callback_done.set()
                
            doc_ref = self.db.collection(u'game_server').document(u'sessions').collection(network_game_title).document(u'game_log')
            doc_watch = doc_ref.on_snapshot(on_snapshot) #이친구가 doc_ref경로의 데이터가 변경되면 on_snapshot 메서드를 실행합니다.
        
    def init_game(self):
        self.turn  = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        ###self.init_board()
        ##self.coords = []
        ##self.redos = []
        self.id = 1
        self.gameover=False

    def Count_draw(self):
        self.draw_count= self.draw_count+1

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
        self.x_last_grid.append(x_last)
        self.y_last_grid.append(y_last)

    def give_x_grid(self):
        return self.x_last_grid[self.draw_count-1]

    def give_y_grid(self):
        return self.y_last_grid[self.draw_count-1]

    def save_logical(self, last_logical):
        self.last_logical=last_logical

    def give_logical(self):
        return self.logical_list[self.draw_count-1]
    
    def save_logical_list(self, new_logical):
        self.logical_list.append(new_logical)    
        #print(self.logical_list)
    def undo_all(self):
        self.draw_board()            
        
    def undo(self):
        self.surface.blit(self.small_board,(self.give_x_grid(),self.give_y_grid()))
        self.player_X_turns= not self.player_X_turns
        logical_position=self.give_logical()
        #print(logical_position)
        self.board_status[logical_position[0]][logical_position[1]] = 0
        self.Minus_count()
        print(self.draw_count)

    def redo(self):
        i=len(self.logical_list)
        if self.draw_count<i:
            self.Count_draw()
            print(self.draw_count)
            if self.player_X_turns==False:
                logical_position=self.give_logical()
                winsound.PlaySound("click.wav", winsound.SND_ASYNC)
                logical_position = np.array(logical_position)
                # logical_position = grid value on the board
                # grid_position = actual pixel values of the center of the grid
                grid_position = self.convert_logical_to_grid_position(logical_position)
                self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
                if self.is_show:
                    self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    self.menu.make_text(self.font, str(self.draw_count), white, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)
                else:
                    if i==self.draw_count:
                        self.surface.blit(self.l_black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    else:
                       self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size)) 
                self.player_X_turns= not self.player_X_turns
                self.board_status[logical_position[0]][logical_position[1]] = -1
            else:
                logical_position=self.give_logical()
                winsound.PlaySound("click.wav", winsound.SND_ASYNC)
                logical_position = np.array(logical_position)
                # logical_position = grid value on the board
                # grid_position = actual pixel values of the center of the grid
                grid_position = self.convert_logical_to_grid_position(logical_position)
                self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
                if self.is_show:
                    self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    self.menu.make_text(self.font, str(self.draw_count), black, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)
                else:
                    if i==self.draw_count:
                        self.surface.blit(self.l_white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    else:
                       self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                self.player_X_turns= not self.player_X_turns
                self.board_status[logical_position[0]][logical_position[1]] = +1
        else:
            return

    def show_numbers(self):
        j=len(self.logical_list)
        for i in range(j):
            grid_position = self.convert_logical_to_grid_position(self.logical_list[i])
            if i==j-1:
                if(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==1):
                    self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                elif(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==-1):
                    self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))

            if(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==1):
                grid_position = self.convert_logical_to_grid_position(self.logical_list[i])
                self.menu.make_text(self.font, str(i+1), white, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)
            elif(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==-1):
                    grid_position = self.convert_logical_to_grid_position(self.logical_list[i])
                    self.menu.make_text(self.font, str(i+1), black, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)
                
    
    def show_number(self):
        logical=self.give_logical()
        if(self.board_status[logical[0]][logical[1]]==-1):
            grid_position = self.convert_logical_to_grid_position(logical)
            print(grid_position)
            self.menu.make_text(self.font, str(self.draw_count), black, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)
        elif(self.board_status[logical[0]][logical[1]]==1):
            grid_position = self.convert_logical_to_grid_position(logical)
            print(grid_position)
            self.menu.make_text(self.font, str(self.draw_count), white, None,grid_position[1] - symbol_size + 70, grid_position[0] - symbol_size + 70)

    def hide_numbers(self):
        j=len(self.logical_list)
        for i in range(j):
                grid_position = self.convert_logical_to_grid_position(self.logical_list[i])
                if i<j-1:
                    if(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==-1):
                        self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    elif(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==1):
                        self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                if i==j-1:
                    if(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==-1):
                        self.surface.blit(self.l_white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                    elif(self.board_status[self.logical_list[i][0],self.logical_list[i][1]]==1):
                        self.surface.blit(self.l_black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))

    def hide_number(self):
        if self.draw_count>=1:
            grid_position = self.convert_logical_to_grid_position(self.logical_list[self.draw_count-1])
            if self.player_X_turns==False:
                self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
            else:
                self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
                

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.save_last_start(self.player_X_starts)
        self.player_X_turns = self.player_X_starts

    def Minus_count(self):
        self.draw_count=self.draw_count-1
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        #self.save_logical_list(logical_position)    
        self.save_logical_list(logical_position)
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
        if self.is_show==False:
            if self.draw_count==0:
                self.surface.blit(self.l_black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
            else:
                self.hide_number()
                self.surface.blit(self.l_black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        else:
            self.surface.blit(self.black,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        print(grid_position)
        self.Count_draw()
        print(self.draw_count)

    def draw_X(self, logical_position):
        #self.save_logical_list(logical_position)
        self.save_logical_list(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        print(grid_position)
        if self.is_show==False:
            if self.draw_count==0:
                self.surface.blit(self.l_white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
            else:
                self.hide_number()
                self.surface.blit(self.l_white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        else:
            self.surface.blit(self.white,(grid_position[0] - symbol_size,grid_position[1] - symbol_size))
        self.save_grid(grid_position[0] - symbol_size,grid_position[1] - symbol_size)
        self.Count_draw()
        print(self.draw_count)

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
            print('X wins')
            self.host_win()
        elif self.O_wins:
            print('O wins')
            self.guest_win()
        elif self.tie:
            print('Its a tie')
            self.host_guest_tie()

        return gameover

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
                if self.draw_count!=len(self.logical_list):
                    self.logical_list.pop()
                if self.player_X_turns:
                    if not self.is_grid_occupied(logical_position):
                        #백돌 착수
                        self.landing_white(logical_position)
                else:
                    if not self.is_grid_occupied(logical_position):
                        #흑돌 착수
                        self.landing_black(logical_position)
                        
                # Check if game is concluded
                self.gameover = self.is_gameover()
                if (self.gameover):
                    self.display_gameover()
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def landing_white(self, logical_position) :
        print('백돌 착수')
        winsound.PlaySound("click.wav", winsound.SND_ASYNC)
        self.draw_X(logical_position)
        self.board_status[logical_position[0]][logical_position[1]] = -1
        if self.is_show==True:                   
            self.show_number()
        self.player_X_turns = not self.player_X_turns
        if(self.network_game_title != None) :
            self.network_landing_logging(False, logical_position)
            if(self.network_my_turn == False):
                self.gameover = self.is_gameover()
                if (self.gameover):
                    self.display_gameover()
        else :
            self.gameover = self.is_gameover()
            if (self.gameover):
                self.display_gameover()
             
    def landing_black(self,logical_position) :
        print('흑돌 착수')
        winsound.PlaySound("click.wav", winsound.SND_ASYNC)
        self.draw_O(logical_position)
        self.board_status[logical_position[0]][logical_position[1]] = 1
        if self.is_show==True:                   
            self.show_number()
        self.player_X_turns = not self.player_X_turns
        if(self.network_game_title != None) :
            self.network_landing_logging(True, logical_position)
            if(self.network_my_turn == False):
                self.gameover = self.is_gameover()
                if (self.gameover):
                    self.display_gameover()
        else :
            self.gameover = self.is_gameover()
            if (self.gameover):
                self.display_gameover()

    def network_landing_logging(self, isBlack, logical_position) :
        print('데이터베이스에 게임 로그 기록')
        if(isBlack) :
            turn = 'Black'
        else :
            turn = 'White'

        db_ref = self.db.collection(u'game_server').document(u'sessions').collection(self.network_game_title).document(u'game_log')
        db_ref.set({
            u'turn' : turn,
            u'landing_position_x' : int(logical_position[0]),
            u'landing_position_y' : int(logical_position[1])
        }, merge=True)

    def host_win(self):
        print('호스트가 이김. 전적을 반영합니다.')
        if(self.isHost):
            self.user_info.total += 1
            self.user_info.win += 1
            self.db.collection(u'user_info').document(self.user_info.uid).set({
                u'play_game_count' : self.user_info.total,
                u'win_count' : self.user_info.win
            }, merge=True)
        else:
            self.user_info.total += 1
            self.user_info.defeat += 1
            self.db.collection(u'user_info').document(self.user_info.uid).set({
                u'play_game_count' : self.user_info.total,
                u'defeat_count' : self.user_info.defeat
            }, merge=True)
    
    def guest_win(self):
        print('게스트가 이김. 전적을 반영합니다.')
        if(self.isHost):
            self.user_info.total += 1
            self.user_info.defeat += 1
            self.db.collection(u'user_info').document(self.user_info.uid).set({
                u'play_game_count' : self.user_info.total,
                u'defeat_count' : self.user_info.defeat
            }, merge=True)
        else:
            self.user_info.total += 1
            self.user_info.win += 1
            self.db.collection(u'user_info').document(self.user_info.uid).set({
                u'play_game_count' : self.user_info.total,
                u'win_count' : self.user_info.win
            }, merge=True)
    
    def host_guest_tie(self):
        print('무승부. 전적을 반영합니다.')
        self.user_info.total += 1
        self.user_info.tie += 1
        self.db.collection(u'user_info').document(self.user_info.uid).set({
            u'play_game_count' : self.user_info.total,
            u'win_count' : self.user_info.tie
        }, merge=True)

class Omok(object):
    def __init__(self, surface,network_game_title=None,network_my_turn=None,user_info=None):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        #self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.set_image_font()
        self.is_show = True
        
        if(network_game_title != None):
            self.menu = Network_Menu(surface)
        else:
            self.menu = Menu(surface)

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

if __name__ == '__main__':
    main() 