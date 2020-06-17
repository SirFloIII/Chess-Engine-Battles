# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 00:39:20 2018

@author: Flo
"""

import pygame
from collections import defaultdict

class Game:
    
    def __init__(self, title, screensize, init_logic, logic, init_render, render):
        
        self.screensize = screensize
        
        pygame.init()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        self.done = False
        
        self.logic = logic
        self.init_render = init_render
        self.render = render
        self.keydown_callbacks = defaultdict(lambda : lambda:None)
        self.keyup_callbacks = defaultdict(lambda : lambda:None)
        
        init_logic()
        
    def start(self):

        self.screen = pygame.display.set_mode(self.screensize)
        try:
            self.init_render()
        except Exception as e:
            pygame.quit()
            raise e
                
        while (not self.done):
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    else:
                        self.keydown_callbacks[event.key]()
                elif event.type == pygame.KEYUP:
                    self.keyup_callbacks[event.key]()
            
            
            try:
                self.logic(self.clock.get_time())
            except Exception as e:
                pygame.quit()
                raise e
                
            try:
                self.render(self.screen)
            except Exception as e:
                pygame.quit()
                raise e
            
            pygame.display.flip()
            
            self.clock.tick(60)
            
        pygame.quit()


if __name__ == "__main__":
    g = Game("test", (640, 640),
             lambda:None,
             lambda x:None,
             lambda:None,
             lambda x:None)
    g.start()