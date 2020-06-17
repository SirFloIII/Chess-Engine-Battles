# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:59:38 2020

@author: Flo
"""

import chess
import random
import time

name = "Smart Monkey"
author = "Flo'"
description = """
Builds on Angry Monkey.
Checkmates if possible,
else behaves like
a Angry Monkey.
"""


def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    moves = list(board.legal_moves)
    for m in moves:
        board.push(m)
        if board.is_checkmate():
            return m
        else:
            board.pop()
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
    