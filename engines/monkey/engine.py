# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:59:38 2020

@author: Flo
"""

import chess
import random
import time

name = "Monkey Engine"
author = "Flo'"
description = """
Performs random legal moves.
"""

def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    #time.sleep(1)
    return random.choice(list(board.legal_moves))



if __name__ == "__main__":
    b = chess.Board()
    
    while not b.is_checkmate():
        move = pick_move(b, 0)
        b.push(move)
    