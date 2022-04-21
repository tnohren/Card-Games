# Poker.py
from PokerFunctionality import *

class Poker:
    def __init__(self, window, database, playerName):
        game = GameState(window, database, playerName)
        play = 'Yes'
        while (play != 'No'):
            play = game.NextGameStep(window, database)
        game.SaveGame(database)