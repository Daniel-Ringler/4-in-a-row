"""
4 in a Row Game
author: Daniel Ringler

works with pyhton3.7"""

import pygame
from pygame import display


class PgView:
    
    def __init__(self, width=800, height=800):
        pygame.init() 
        pygame.font.init()
        pygame.display.set_caption("4 in a Row")
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.yellow = (252,240,10)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.game_surface = pygame.Surface(self.screen.get_size()).convert()
        self.game_surface.fill((self.white))
        self.menu_surface = pygame.Surface(self.screen.get_size()).convert()
        self.menu_surface.fill(self.white)
    
    def draw_gameboard(self):
        x = 50
        y = 650
        
        # generate the typical 4 in a row form 
        for _ in range (0,42):
            mysegment = GameBoard_Segment((x,y))
            mysegment.blit(self.game_surface)
            
            x += 100
            
            if x == 750:
                x = 50
                y -= 100
    
    def draw_token(self, counter, location):
        if counter % 2 == 0:
            token = Tokens((self.red), (location))
        else:
            token = Tokens((self.yellow), (location))
            
        token.blit(self.game_surface)
    
    def draw_whitespace(self):
        surface = pygame.Surface((800,150))
        surface.fill((self.white))
        surface = surface.convert()
        self.game_surface.blit(surface, (0,0))     
        
    def create_font(self, text, color, size):
        font = pygame.font.SysFont('Arial', size)
        textsurface = font.render(text, False, (color))
        return textsurface
        
    def draw_menu(self):
        textsurface_menu_header = self.create_font("4 in  a Row", (self.red), 50)
        textsurface_menu_text = self.create_font("Press SPACE to start playing !", (self.yellow), 40)
        textsurfaces_menu = [textsurface_menu_header, textsurface_menu_text]
        
        counter = 0
        
        for textsurface in textsurfaces_menu:
            x_centered = self.text_centered_x(textsurface)
            width, height = textsurface.get_size()
            if counter == 0:
                y_centered = (800/2-100)-height
            else:
                y_centered = (800/2-100)+height
            counter += 1
            self.menu_surface.blit(textsurface, (x_centered, y_centered))
    
    def draw_game(self, counter, x, y, token_array, win):
        self.draw_whitespace()
        if win == False: self.draw_token(counter, (x,y))
        self.draw_gameboard()
        
        # draw tokens on the gameboard
        for i in token_array:
            position = i
            if len(position) == 3:
                token_color = position[2]
                position.pop()
            self.draw_token(token_color, position)
            position.append(token_color)

        self.screen.blit(self.game_surface, (0,0))
        pygame.display.update()
        
    def draw_endgame(self, win):
        if win == "Red": color = self.red
        else: color = self.yellow
        
        textsurface_won = self.create_font(str(win) + " has won !", color, 40)
        textsurface_newround = self.create_font("press SPACE to start a new round", color, 30)
        textsurface_quit = self.create_font("press ESC to quit playing", color, 30)
        
        textsurfaces_endgame = [textsurface_won, textsurface_newround, textsurface_quit]
        y = 5
        
        for textsurface in textsurfaces_endgame:
            centered_x = self.text_centered_x(textsurface)
            self.game_surface.blit(textsurface, (centered_x, y))
            _, height = textsurface.get_size()
            y = y + height + 5
        
    def handle_win(self, win):
        self.draw_endgame(win)
        self.screen.blit(self.game_surface, (0,0))
        display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 2
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 1
                    if event.key == pygame.K_ESCAPE:
                        return 2

    
    def text_centered_x(self, textsurface):
        width, height = textsurface.get_size() # get the size of the textsurface
        centered_x = (800/2)-(width/2) # calculates the x value for a x centered textsurface
        return centered_x
        

    def run(self):
        
        running = True
        win = False
        counter = 0
        token_array = [] # array of lists containing X-Coordinate, Y-Coordinate and the Token (0 -> Red or 1 -> Yellow)
        current_surface = "menu" # decides if the menu or the game is displayed
        
        x = 350
        y = 0
        
        while running:
            counter = 0
            token_array = []
            win = False
            
            if current_surface == "menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_SPACE:
                            current_surface = "game"
                
                self.draw_whitespace()
                self.draw_menu()
                self.screen.blit(self.menu_surface, (0,0))
                pygame.display.update()
                
            if current_surface == "game":
                while counter < 42:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            counter = 43
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                current_surface = "menu"
                                counter = 43
                            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                if x < 600:
                                    x += 100
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if x > 100:
                                    x -= 100
                            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                y += 650
                                a = Game_Logic(x, y, counter)
                                token_check = a.compare_token_to_array(token_array)
                                for _ in range(6):
                                    if token_check == True:
                                        y -= 100
                                        a = Game_Logic(x, y, counter)
                                        token_check = a.compare_token_to_array(token_array)    
                                if y > 100:
                                    token_array = a.append_to_token_array(token_array)
                                    win = a.check_win(token_array)
                                        
                                    counter += 1
                                x = 350
                                y = 0
                            if event.key == pygame.K_ESCAPE:                            
                                running = False
                                counter = 43
                     
                    self.draw_game(counter, x, y, token_array, win)
                    
                    if win != False:
                        choice = self.handle_win(win)
            
                        if choice == 1:
                            counter = 0
                            token_array = []
                            win = False
                        if choice == 2:
                            counter = 43
                            running = False
            
            if running == False:
                pygame.quit()        
                    
        
# class for generating a Gameboard Segment
class GameBoard_Segment:
    
    def __init__(self, position):
        self.position = position
        self.surface = pygame.Surface((100,100))
        self.surface.fill((0,51,204))
        pygame.draw.circle(self.surface, (255,255,255), (50,50),45)
        self.surface = self.surface.convert()
        
    def blit(self, game_surface):
        game_surface.blit(self.surface, (self.position))
    

# class that generates the player tokens
class Tokens:
    
    def __init__(self, color, position):
        self.position = position
        self.color = color
        self.surface = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        pygame.draw.circle(self.surface, (color), (50,50),45)
    
    def blit(self, game_surface):
        game_surface.blit(self.surface, (self.position))
        
class Game_Logic:
    
    def __init__(self, x, y, token):
        self.x = x 
        self.y = y 
        self.token = token
        
    def create_token_array(self):
        token_array = []
        return token_array
    
    def append_to_token_array(self, array):
        token = self.token % 2
        array.append([])
        array[self.token].append(self.x)
        array[self.token].append(self.y)
        array[self.token].append(token)
        
        return array
    
    def compare_token_to_array(self, array):
        current_x_y = [self.x, self.y]
        
        for _ in array:
            position = _
            if len(position) == 3:
                token = position[2]
                position.pop()
            if position == current_x_y:
                position.append(token)
                return True
            else:
                position.append(token)
 
    def check_win(self, array):
        token = self.token % 2
        current_x_y = [self.x, self.y, token]
        win = False
        h_counter = 0 # horizontal token counter
        v_counter = 0 # vertical token counter
        d_right_counter = 0 # diagonal to the right token counter
        d_left_counter = 0 # diagonal to the left token counter
        
        if token == 0:
            colour = "Red"
        else:
            colour = "Yellow"
        
        for _ in range(3):
            # check for vertical win
            if current_x_y[1] < 650:
                current_x_y[1] += 100
                for i in array:
                    if current_x_y[0] == i[0]:
                        if current_x_y == i:
                            v_counter += 1
                            break
               
        if v_counter == 3:      
            win = True
                        
        # check for horizontal win   
        # reset current_x_y
        current_x_y = [self.x, self.y, token]
            
        # check to the right
        counter = 0
        for _ in range(3):
            if h_counter < counter:
                break
            if current_x_y[0] < 650:
                current_x_y[0] += 100
            else:
                break
            for i in array:
                if current_x_y[1] == i[1]:
                    if current_x_y == i:
                        h_counter+= 1
            counter += 1
            
        current_x_y = [self.x, self.y, token]
            
        # check to the left
        counter = 0
        for _ in range(3):
            if h_counter < counter:
                break
            if current_x_y[0] > 50:
                current_x_y[0] -= 100
            else:
                break
            for i in array:
                if current_x_y[1] == i[1]:
                    if current_x_y == i:
                        h_counter += 1
            counter += 1
            
        if h_counter >= 3:
            win = True
    
        # check for diagonal win
        # check for right diagonal
        # check right down
        current_x_y = [self.x, self.y, token]
        counter = 0
        d_right_up_counter = 0
        for _ in range(3):
            if d_right_up_counter < counter:
                break
            current_x_y[0] += 100
            current_x_y[1] += 100
            for i in array:
                if current_x_y == i:
                    d_right_up_counter += 1
                    break
            counter += 1
    
        # check left up
        current_x_y = [self.x, self.y, token]
        counter = 0
        d_right_down_counter = 0
        for _ in range(3):
            if d_right_up_counter < counter:
                break
            current_x_y[0] -= 100
            current_x_y[1] -= 100
            for i in array:
                if i == current_x_y:
                    d_right_down_counter += 1
                    break
            counter += 1
        
        d_right_counter = d_right_up_counter + d_right_down_counter
        if d_right_counter >= 3:
            win = True
        
        # check for left diagonal
        # check right up
        current_x_y = [self.x, self.y, token]
        counter = 0
        d_left_up_counter = 0
        for _ in range(3):
            if d_left_up_counter < counter:
                break
            current_x_y[0] += 100
            current_x_y[1] -= 100 
            for i in array:
                if i == current_x_y:
                    d_left_up_counter += 1
                    break
            counter += 1
                
        # check left down
        current_x_y = [self.x, self.y, token]
        counter = 0
        d_left_down_counter = 0
        for _ in range(3):
            if d_left_down_counter < counter:
                break
            current_x_y[0] -= 100
            current_x_y[1] += 100
            for i in array:
                if i == current_x_y:
                    d_left_down_counter += 1
                    break
            counter += 1
        
        d_left_counter = d_left_up_counter + d_left_down_counter
        
        if d_left_counter >= 3:
            win = True

        if win == True:
            return colour
        else:
            return False
        

PgView().run()                                                                                                                                      