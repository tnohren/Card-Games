# CardandDeck.py

import random
import itertools

# Card class --- handles the suit and value of the card
# as well as the names associated with each
# There is a method used to print out the card
class Card:
    snames = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
    vnames = ['Ace', '2', '3', '4', '5', '6', '7', '8',
              '9', '10', 'Jack', 'Queen', 'King']
    def __init__(self, st, val):
        self.suit = st
        self.value = val

    def __str__(self):
        return('%s of %s' % (self.vnames[self.value], self.snames[self.suit]))

# Deck class --- initializes a full deck of 52 cards
# Each card is different (no duplicates)
# Includes a shuffle method, as well as a draw method
class Deck:
    def __init__(self):
        self.dk = []
        for val, st in itertools.product(range(0,13), range(0,4)):
            self.dk.append(Card(st, val))

    def shuffle(self):
        random.shuffle(self.dk)

    def draw(self):
        return self.dk.pop(-1)

# Hand class --- holds a certain number of cards based on the type of game played
# Its __init__ will draw the appropriate amount of cards from the deck given
# Includes a method for printing the entire hand
class Hand:
    def __init__(self, number_of_cards, deck):
        self.hd = []
        for i in range(number_of_cards):
            self.hd.append(deck.draw())

    def __str__(self):
        printhand = []
        for card in self.hd:
            printhand.append(str(card))
        return '\n'.join(printhand)

        
