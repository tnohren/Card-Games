# Poker.py
import sys
sys.path.append('./CardandDeck')
sys.path.append('./PrimaryWindow')
from CardandDeck import *
from PrimaryWindow import *
from PokerFunctionality import *
from PokerChipFunctionality import *
from PokerWindow import *

def play():
    # Start New Window
    window = Window()

    # Initialize poker chips
    chips = PokerChipHandler()

    # Initialize Game State. User will be prompted to load existing game or start a new one
    game = GameState(window)

    # Continue playing until user wants to quit
    play = 'Yes'
    while (play != 'No'):
        print("Game Started")
        # Evaluate next game step
        play = game.NextGameStep(window)

    # After user selects to quit playing, prompt user to save game
    game.SaveGame(window)
    chips.SaveChips()
    window.Quit()
    
play()
quit()