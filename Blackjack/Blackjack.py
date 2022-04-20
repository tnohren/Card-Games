# Blackjack.py
from BlackjackFunctionality import *

class Blackjack:
    def __init__(self, window, database, playerName):
        game = GameState(window, database, playerName)
        play = 'Yes'
        while (play != 'No'):
            play = game.GameFlow(window, database)