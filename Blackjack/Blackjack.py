# Blackjack.py
import sys
sys.path.append('./CardandDeck')
sys.path.append('./Currency')
sys.path.append('./PrimaryWindow')
from CardandDeck import *
from CurrencyManagement import * # unused - will use later
from PrimaryWindow import *
from BlackjackFunctionality import *

def play2():
    # Start New Window
    window = Window()

    # Initialize Chips
    # TODO

    # Initialize Game State. User will be prompted to load existing game or start a new one
    game = GameState(window)

    # Continue playing until user wants to quit
    play = 'Yes'
    while (play != 'No'):
        print ("Game Started")
        # Evaluate next game step
        play = game.GameFlow(window)

play2()