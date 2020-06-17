# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:59:38 2020

@author: Flo
"""

import chess
import random
import time

name = "Angry Monkey"
author = "Flo'"
description = """
Performs a random capturing move.
If there are none, performs
a other random move.
"""

def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    moves = list(board.legal_moves)
    capturing_moves = [m for m in moves if board.is_capture(m)]
    if capturing_moves:
        return random.choice(capturing_moves)
    else:
        return random.choice(moves)



if __name__ == "__main__":
    b = chess.Board()
    
    while not b.is_checkmate():
        move = pick_move(b, 0)
        b.push(move)
    