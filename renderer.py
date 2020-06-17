# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:37:28 2020

@author: Flo
"""

import pygame
import itertools

B = False
W = True

# COLOR SCHEMES:
# jolly:
#cWhiteBG = pygame.Color(240, 240, 200)
#cBlackBG = pygame.Color(183, 69, 122)
#cWhiteP = cWhiteBG
#cBlackP = pygame.Color(81, 20, 48)
# icy blue:
cWhiteBG = pygame.Color(240, 240, 200)
cBlackBG = pygame.Color(69, 122, 183)
cWhiteP = pygame.Color(220, 220, 220)
cBlackP = pygame.Color(10, 30, 70)

font_r = "robotoslab"
font_b = "robotoslabregular"

#font_r = "robotomono"
#font_b = "robotomonomedium"


class Renderer:
    
    def __init__(self, state, fs):
        self.state = state
        self.fs = fs
        
        self.size = (fs*8 + 4*fs, fs*8)


    def init_render(self):
        icons = pygame.image.load("icons.png")
        self.icons = pygame.transform.scale(icons, (6*self.fs, 2*self.fs))
        self.icons.convert_alpha()
        # convert black and white image to color scheme:
        cDiff = cWhiteP - cBlackP
        self.icons.fill(cDiff, None, pygame.BLEND_MULT)
        self.icons.fill(cBlackP, None, pygame.BLEND_ADD)
        
        self.icon_coords = {"K": (0 * self.fs, 0, self.fs, self.fs),
                            "k": (0 * self.fs, self.fs, self.fs, self.fs),
                            "Q": (1 * self.fs, 0, self.fs, self.fs),
                            "q": (1 * self.fs, self.fs, self.fs, self.fs),
                            "B": (2 * self.fs, 0, self.fs, self.fs),
                            "b": (2 * self.fs, self.fs, self.fs, self.fs),
                            "N": (3 * self.fs, 0, self.fs, self.fs),
                            "n": (3 * self.fs, self.fs, self.fs, self.fs),
                            "R": (4 * self.fs, 0, self.fs, self.fs),
                            "r": (4 * self.fs, self.fs, self.fs, self.fs),
                            "P": (5 * self.fs, 0, self.fs, self.fs),
                            "p": (5 * self.fs, self.fs, self.fs, self.fs)}
        
    def render(self, screen):
        # fill bg with green
        screen.fill((0,255,0))
    
        # draw board and pieces
        for i, j in itertools.product(range(8), repeat = 2):
            pygame.draw.rect(screen, cBlackBG if (i+j)%2 else cWhiteBG, (i*self.fs, j*self.fs, self.fs, self.fs))
            
            piece = self.state.board.piece_at((7-j)*8 + i)
            if piece is not None:
                screen.blit(self.icons, (i*self.fs,j*self.fs), area = self.icon_coords[piece.symbol()])
        
        # draw sideboard
        pygame.draw.rect(screen, cBlackP, (8*self.fs, 0, self.fs//2, 8*self.fs))
        pygame.draw.rect(screen, cWhiteP, (8*self.fs + self.fs//2, 0, 7*self.fs//2, 8*self.fs))
        
        # draw text
        def write(text, x, y, color = cBlackP, centerx = False, centery = True):
            w, h = font.size(text)
            screen.blit(font.render(text, True, color), (x * self.fs - centerx * w//2, y * self.fs - centery * h//2))
        
        # engine info
        font = pygame.font.SysFont(font_r, 48 * self.fs//128)
        write(self.state.engines[B].name, 8.8, 0.4)
        write(self.state.engines[W].name, 8.8, 6.4)
        
        font = pygame.font.SysFont(font_b, 24 * self.fs//128)
        write("by: " + self.state.engines[B].author, 9, 0.8)
        write("by: " + self.state.engines[W].author, 9, 6.8)
        
        font = pygame.font.SysFont(font_r, 20 * self.fs//128)
        for i, line in enumerate(self.state.engines[B].description.strip().split("\n")):
            write(line, 8.9, 1.1 + 0.2*i)
        for i, line in enumerate(self.state.engines[W].description.strip().split("\n")):
            write(line, 8.9, 7.1 + 0.2*i)
        
        # draw clock
        font = pygame.font.SysFont(font_r, 96 * self.fs//128)
        write(time_format(self.state.chess_clock[B]), 10.25, 2.5, centerx = True)
        write(time_format(self.state.chess_clock[W]), 10.25, 5.5, centerx = True)
    
        write("vs", 10.25, 4, centerx = True)
        
        
        # draw game over screen
        if self.state.game_over:
            if self.state.board.is_checkmate():
                text = "Checkmate"
                subtext = "Black wins!" if self.state.board.turn else "White wins!"
            elif self.state.board.is_stalemate():
                text = "Draw"
                subtext = "White" if self.state.board.turn else "Black"
                subtext += " has no legal moves!"
            elif self.state.board.is_insufficient_material():
                text = "Draw"
                subtext = "Insufficient Material!"
            elif self.state.forfeit_by_error:
                text = "Forfeit"
                subtext = "White" if self.state.board.turn else "Black"
                subtext += " has forfeit the game!"
            elif self.state.forfeit_by_clock:
                text = "Forfeit"
                subtext = "White" if self.state.board.turn else "Black"
                subtext += "'s Clock has run out!"
            else:
                text = "Draw"
                subtext = "Unknown"
                
            font = pygame.font.SysFont(font_b, 128 * self.fs//128)
            #write(text, 4.04, 4.04, centerx = True, color = cWhiteP)
            write(text, 4.02, 4.02, centerx = True, color = cWhiteP)
            write(text, 4, 4, centerx = True)
    
            font = pygame.font.SysFont(font_b, 48 * self.fs//128)
            #write(subtext, 4.04, 5.54, centerx = True, color = cWhiteP)
            write(subtext, 4.02, 5.52, centerx = True, color = cWhiteP)
            write(subtext, 4, 5.5, centerx = True)
            

def time_format(t):
    #t in seconds
    minutes = int(t/60)
    seconds = int(t%60)
    milliseconds = int(t*100%100)
    return f"{minutes:2}:{seconds:2}:{milliseconds:2}".replace(" ", "0")
        
            
if __name__ == "__main__":
    import duel
    import pygametemplateOOP
    
    state = duel.State(2*60)
    renderer = Renderer(state, 128)
    
    game = pygametemplateOOP.Game("Engine Battles", renderer.size,
                                  state.init_logic, lambda x:None,
                                  renderer.init_render, renderer.render)
    game.start()
