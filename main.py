"""
4 in a Row Game
author: Daniel Ringler

works with pyhton3.7"""

import pygame


class PgView:
    
    def __init__(self, width=800, height=800):
        pygame.init() 
        pygame.font.init()
        pygame.display.set_caption("4 in a Row")
        self.white = (255,255,255)
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
            token = Tokens((255,0,0), (location))
        else:
            token = Tokens((255,255,0), (location))
            
        token.blit(self.game_surface)
    
    def draw_whitespace(self):
        surface = pygame.Surface((800,150))
        surface.fill((255,255,255))
        surface = surface.convert()
        self.game_surface.blit(surface, (0,0))     
        
    def draw_font(self, text):
        font = pygame.font.SysFont('Arial', 30)
        textsurface = font.render(text, False, (0, 0, 0))
        self.game_surface.blit(textsurface, (0,0))
    
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
                            if event.key == pygame.K_RIGHT:
                                if x < 600:
                                    x += 100
                            if event.key == pygame.K_LEFT:
                                if x > 100:
                                    x -= 100
                            if event.key == pygame.K_DOWN:
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
                            
                    self.draw_whitespace()
                    self.draw_token(counter, (x,y))
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
                                    
                    if win != False:
                        print(str(win) + " has won!")
                        print("Enter 1 to start a new round.")
                        print("Enter 2 to quit playing")
                        choice = int(input()) 

                        while choice > 2 or choice < 1:
                            print(str(choice) + " is not allowed.")
                            print("Enter 1 to start a new round.")
                            print("Enter 2 to quit playing.")
                            choice = int(input())
                            
                        if choice == 1:
                            counter = 0
                            token_array = []
                            win = False
                        if choice == 2:
                            counter = 43
                            running = False
                
            
            if running == False:
                print("game stopped")
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
        for _ in range(3):
            if current_x_y[0] < 650:
                current_x_y[0] += 100
            else:
                break
            for i in array:
                if current_x_y[1] == i[1]:
                    if current_x_y == i:
                        h_counter+= 1
            
        current_x_y = [self.x, self.y, token]
            
        # check to the left
        for _ in range(3):
            if current_x_y[0] > 50:
                current_x_y[0] -= 100
            else:
                break
            for i in array:
                if current_x_y[1] == i[1]:
                    if current_x_y == i:
                        h_counter += 1
            
        if h_counter >= 3:
            win = True
    
        # check for diagonal win
        # check for right diagonal
        # check right down
        current_x_y = [self.x, self.y, token]
        
        for _ in range(3):
            current_x_y[0] += 100
            current_x_y[1] += 100
            for i in array:
                if current_x_y == i:
                    d_right_counter += 1
                    break
    
        # check left up
        current_x_y = [self.x, self.y, token]
        
        for _ in range(3):
            current_x_y[0] -= 100
            current_x_y[1] -= 100
            for i in array:
                if i == current_x_y:
                    d_right_counter += 1
                    break
        
        if d_right_counter >= 3:
            win = True
        
        # check for left diagonal
        # check right up
        current_x_y = [self.x, self.y, token]
        
        for _ in range(3):
            current_x_y[0] += 100
            current_x_y[1] -= 100 
            for i in array:
                if i == current_x_y:
                    d_left_counter += 1
                    break
                
        # check left down
        current_x_y = [self.x, self.y, token]
        
        for _ in range(3):
            current_x_y[0] -= 100
            current_x_y[1] += 100
            for i in array:
                if i == current_x_y:
                    d_left_counter += 1
                    break
        
        if d_left_counter >= 3:
            win = True

        if win == True:
            return colour
        else:
            return False
        
         
PgView().run()                                                                                                                                      