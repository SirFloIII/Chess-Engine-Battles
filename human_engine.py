# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:59:38 2020

@author: Flo
"""

import chess
import mouse
import pygetwindow as win

name = "Human Engine"
author = "Flo'"
description = """
Reads mouseposition relative
to pygame window and interprets
mouseclicks."""


def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    
    
    mouse_was_down = False
    
    while True:
        if win.getActiveWindowTitle() == "Engine Battles":
            window = win.getActiveWindow()
            if window is not None:
                fs = (window.height - 39)//8
                
                mx, my = mouse.get_position()
                wx, wy = window.left, window.top
                
                x = mx - wx - 8
                y = my - wy - 31
                
                file = x//fs
                rank = y//fs
                
                if mouse.is_pressed():
                    if not mouse_was_down:
                        if 0 <= rank < 8 and 0 <= file < 8:    
                            start = f"{'abcdefgh'[file]}{8-rank}"
#                            print("down:", start)
                        mouse_was_down = True
                else:
                    if mouse_was_down:
                        if 0 <= rank < 8 and 0 <= file < 8:
                            end = f"{'abcdefgh'[file]}{8-rank}"
#                            print("up:", end)
                            if start != end:
                                move = chess.Move.from_uci(start + end)
                                if board.is_legal(move):
                                    return move
                        mouse_was_down = False
            
if __name__ == "__main__":
    b = chess.Board()
    
    print(pick_move(b, 0))
    
#    while not b.is_checkmate():
#        move = pick_move(b, 0)
#        b.push(move)
#    