# Poker.py
import sys
sys.path.append('./CardandDeck')
from CardandDeck import *
from PokerFunctionality import *
from PokerChipFunctionality import *

def play():
    # Initialize Game State. User will be prompted to load existing game or start a new one
    game = GameState()
    play = 'yes'

    # Initialize poker chips
    chips = PokerChipHandler()

    # Continue playing until user wants to quit
    while (play != 'no'):
        print("Game Started")
        # Evaluate next game step
        play = game.NextGameStep()

    # After user selects to quit playing, prompt user to save game
    game.SaveGame()
    chips.SaveChips()
    
play()