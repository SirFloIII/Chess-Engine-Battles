# -*- coding: utf-8 -*-
"""
Created on Tue May 26 03:28:27 2020

@author: Flo
"""

import multiprocessing
import chess
import pygametemplateOOP
from renderer import Renderer
import importlib

class Engine:
    def __init__(self, name):
        module = importlib.import_module(f"engines.{name}.engine")
        
        self.pick_move = module.pick_move
        self.name = module.name
        self.author = module.author
        self.description = module.description
        
        self.elo = 500
        self.wins = 1
        self.losses = 2
        self.draws = 10

class State:

    def __init__(self, default_clock = 60, default_restart_clock = 5):
        self.default_clock = default_clock  #seconds
        self.default_restart_clock = default_restart_clock #seconds

    def engine_asker(self, conn):
        while True:
            try:
                board, time_left = conn.recv()
            except EOFError:
                return
            try:
                conn.send(self.engines[board.turn].pick_move(board, time_left))
            except Exception as e:
                conn.send(e)
    
    def init_logic(self):
        
        self.engines = (Engine("milli"), Engine("smart_monkey"))
        self.board = chess.Board()
        
        self.chess_clock = [self.default_clock] * 2
        self.restart_clock = self.default_restart_clock
        
        self.conn, target_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target = self.engine_asker, args = (target_conn, ))
        self.p.start()
        self.process_running = False
        
        self.game_over = False
        self.forfeit_by_error = False
        self.forfeit_by_clock = False
    
    def logic(self, dt):
        if self.game_over:
            self.restart_clock -= dt/1000
            if self.restart_clock < 0:
                self.init_logic()
        else:
            if self.process_running:
                if not self.conn.poll():
                    self.chess_clock[self.board.turn] -= dt/1000
                    if self.chess_clock[self.board.turn] <= 0:
                        self.chess_clock[self.board.turn] = 0
                        self.game_over = True
                        self.forfeit_by_clock = True
                        self.p.terminate()
                        self.process_running = False
                else:
                    move = self.conn.recv()
                    self.process_running = False
                    if isinstance(move, Exception):
                        self.game_over = True
                        self.forfeit_by_error = True
                        print(move)
                    elif isinstance(move, chess.Move) and move in self.board.legal_moves:
                        self.board.push(move)
                        if self.board.is_game_over():
                            self.game_over = True
                    else:
                        self.game_over = True
                        self.forfeit_by_error = True
                        print("illegal move")
            else:
                self.conn.send((self.board.copy(), self.chess_clock[self.board.turn]))
                self.process_running = True


if __name__ == "__main__":
    
    state = State(20*60)
    renderer = Renderer(state, 128)
    
    game = pygametemplateOOP.Game("Engine Battles", renderer.size,
                                  state.init_logic, state.logic,
                                  renderer.init_render, renderer.render)
    game.start()



















