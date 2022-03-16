from CardandDeck.CardandDeck import *
from PokerFunctionality import *

def play():
    ongoing = True
    while (ongoing):
        print("New Game Started")

        # Initializing the deck to play with
        deck = Deck()
        deck.shuffle()

        # Deal Hands
        playerHand = Hand(2, deck)
        opponent1Hand = Hand(2, deck)
        opponent2Hand = Hand(2, deck)
        opponent3Hand = Hand(2, deck)

        # Burn

