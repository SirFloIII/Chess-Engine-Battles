# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:18:14 2020

@author: Flo
"""

import chess

name = "Milli Engine"
author = "Flo'"
description = """
Does minimax with a
depth of two halfturns,
then counts pieces.
en memoriam
"""

piece_values = {"p": 1,
                "P": -1,
                "r": 8,
                "R": -8,
                "n": 3,
                "N": -3,
                "b": 4,
                "B": -4,
                "q": 12,
                "Q": -12,
                "k": 0,
                "K": 0,
                }

def pick_move(board, time_left_on_clock):
    """
    takes in a chess.Board
    as well as time_left_on_clock in seconds
    returns a chess.Move
    """
    
    return max(evaluate(board, 2).items(), key = lambda x:x[1])[0]

def evaluate(board, depth):
    """
    does minimax on board with depth many half moves
    returns dict of legal_moves -> evals
    """
    evaluation = dict()
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            evaluation[move] = 1000
        elif board.is_game_over():
            evaluation[move] = 0
        else:
            if depth == 0:
                x = sum([piece_values[p.symbol()] for p in board.piece_map().values()])
                evaluation[move] = x if board.turn else -x
            else:
                d = evaluate(board, depth - 1)
                evaluation[move] = - max(d.values())
        board.pop()
    return evaluation
        
            
if __name__ == "__main__":
    b = chess.Board()
    
    while not b.is_checkmate():
        move = pick_move(b, 0)
        b.push(move)
    