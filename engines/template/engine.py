# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:59:38 2020

@author: Flo
"""

import chess

name = "Template Engine"
author = "Your Name here"
description = """
Write a short descrition here.
4 Lines max
"""


def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    
    raise NotImplementedError

if __name__ == "__main__":
    b = chess.Board()
    
    while not b.is_checkmate():
        move = pick_move(b, 0)
        b.push(move)
    