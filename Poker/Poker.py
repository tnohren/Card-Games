# Poker.py
from PokerFunctionality import *

class Poker:
    def __init__(self, window, playerName):
        game = GameState(window)
        play = 'Yes'
        while (play != 'No'):
            play = game.NextGameStep(window)
        game.SaveGame(window)