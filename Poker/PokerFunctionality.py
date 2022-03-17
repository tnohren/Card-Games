# PokerFunctionality.py
import os.path
import sys
sys.path.append('./CardandDeck')
from CardandDeck import *

# To Hold Game Status Definitions
class GameStruct:
    def __init__(self):
        self.begin = "Begin"
        self.burn1 = "Burn1"
        self.reveal1 = "Reveal1"
        self.burn2 = "Burn2"
        self.reveal2 = "Reveal2"
        self.burn3 = "Burn3"
        self.reveal3 = "Reveal3"
        self.end = "End"

class GameState:
    def __init__(self):
        self.gameStruct = GameStruct()
        cont = input("Would you like to continue a previously saved game? ('yes' or 'no') ")
        if (cont == 'yes'):
            self.LoadGame()
        elif (cont == 'no'):
            self.NewGame()
        else:
            print("Invalid input")

    def __str__(self):
        # Format string for saving
        # First line contains number of cards in the deck, number of cards that have been revealed, and the number of cards in the burn pile.
        # Each subsequent line is a unique card: first is the player's hand, then the opponents hands, then revealed cards, then burned cards, and finally cards remaining in the deck.
        saveString = str(len(self.deck)) + ',' + str(len(self.playedCards)) + ',' + str(len(self.burnPile)) + '\n'
        saveString += str(self.playerHand) + '\n' + str(self.opponent1Hand) + '\n' + str(self.opponent2Hand) + '\n' + str(self.opponent3Hand) + '\n' + str(self.playedCards) + '\n' + str(self.burnPile) + '\n' + str(self.deck)
        return saveString

    def LoadGame(self):
        # Read in Saved Game File
        readGame = open("saved_poker.txt", "r+")
        readLines = [line.rstrip().split(',') for line in readGame]
        currentDeckSize = int(readLines[0][0])
        currentPlayedSize = int(readLines[0][1])
        currentBurnSize = int(readLines[0][2])

        # Initialize Game Pieces
        self.playerHand = Hand()
        self.opponent1Hand = Hand()
        self.opponent2Hand = Hand()
        self.opponent3Hand = Hand()
        self.playedCards = Hand()
        self.burnPile = Hand()
        self.deck = Deck(False)

        # Read Saved Game Data
        for i in range(1, len(readLines)):
            # Player Hand Saved First
            if (i == 1 or i == 2):
                self.playerHand.addCard(Card(readLines[i][1], readLines[i][0]))
            # Opponent 1 Hand Saved Second
            elif (i == 3 or i == 4):
                self.opponent1Hand.addCard(Card(readLines[i][1], readLines[i][0]))
            # Opponent 2 Hand Saved Third
            elif (i == 5 or i == 6):
                self.opponent2Hand.addCard(Card(readLines[i][1], readLines[i][0]))
            # Opponent 3 Hand Saved Fourth
            elif (i == 7 or i == 8):
                self.opponent3Hand.addCard(Card(readLines[i][1], readLines[i][0]))
            # Played Cards Saved Fifth
            elif (i >= 9 and (i <= 8 + currentPlayedSize)):
                self.playedCards.addCard(Card(readLines[i][1], readLines[i][0]))
            # Burned Cards Saved Sixth
            elif ((i >= len(readLines) - currentDeckSize - currentBurnSize) and (i <= (len(readLines) - currentDeckSize - 1))):
                self.burnPile.addCard(Card(readLines[i][1], readLines[i][0]))
            # Deck Saved Last
            elif (currentDeckSize != 0 and i >= len(readLines) - currentDeckSize):
                self.deck.addCard(Card(readLines[i][1], readLines[i][0]))

        # Determine Game Status
        self.DetermineStatus()
        
    # Begin New Game
    def NewGame(self):
        # Initializing New Deck to Play With
        self.deck = Deck(True)
        self.deck.shuffle()

        # Deal Hands
        self.playerHand = Hand(2, self.deck)
        self.opponent1Hand = Hand(2, self.deck)
        self.opponent2Hand = Hand(2, self.deck)
        self.opponent3Hand = Hand(2, self.deck)

        # Initialize Other Card Piles
        self.burnPile = Hand()
        self.playedCards = Hand()
        
        # Set Game Status
        self.currentGameStatus = self.gameStruct.begin

    # Save In Progress Game
    def SaveGame(self):
        overwrite = 'yes'
        if (os.path.isfile('saved_poker.txt')):
            overwrite = input("Are you sure you would like to overwrite your previously saved game? ('yes' or 'no') ")  
        if (overwrite == 'yes'):
            with open('saved_poker.txt', 'w') as savefile:
                savefile.write(str(self))

    # Determine Game Status
    def DetermineStatus(self):
        # Game status is determined by the number of cards in the burn pile and the number of cards that have been revealed/played
        if (len(self.burnPile) == 0):
            self.currentGameStatus = self.gameStruct.begin
        elif (len(self.burnPile) == 1):
            if (len(self.playedCards) == 0):
                self.currentGameStatus = self.gameStruct.burn1
            else:
                self.currentGameStatus = self.gameStruct.reveal1
        elif (len(self.burnPile) == 2):
            if (len(self.playedCards) == 3):
                self.currentGameStatus = self.gameStruct.burn2
            else:
                self.currentGameStatus = self.gameStruct.reveal2
        else:
            if (len(self.playedCards) == 4):
                self.currentGameStatus = self.gameStruct.burn3
            else:
                self.currentGameStatus = self.gameStruct.reveal3

    # Execute Next Game Step
    def NextGameStep(self):
        finalReveal = False
        if (self.currentGameStatus == self.gameStruct.begin):
            # First Burn
            self.BurnCard()
            self.currentGameStatus = self.gameStruct.burn1
        elif (self.currentGameStatus == self.gameStruct.burn1):
            # First Reveal (3 cards)
            self.RevealCards(3)
            self.currentGameStatus = self.gameStruct.reveal1
        elif (self.currentGameStatus == self.gameStruct.reveal1):
            # Second Burn
            self.BurnCard()
            self.currentGameStatus = self.gameStruct.burn2
        elif (self.currentGameStatus == self.gameStruct.burn2):
            # Second Reveal (1 card)
            self.RevealCards(1)
            self.currentGameStatus = self.gameStruct.reveal2
        elif (self.currentGameStatus == self.gameStruct.reveal2):
            # Third Burn
            self.BurnCard()
            self.currentGameStatus = self.gameStruct.burn3
        elif (self.currentGameStatus == self.gameStruct.burn3):
            # Third Reveal (1 card)
            self.RevealCards(1)
            self.currentGameStatus = self.gameStruct.reveal3
        elif (self.currentGameStatus == self.gameStruct.reveal3):
            # End of Game
            finalReveal = True
            self.currentGameStatus = self.gameStruct.end
        elif (self.currentGameStatus == self.gameStruct.end):
            # Game Finished and Results Displayed. Ask To Begin New Game
            cont = input("Would you like to begin a new game? ('yes' or 'no') ")
            if (cont == 'yes'):
                self.NewGame()           
            return cont
        else:
            print("Exception Caught - Invalid Game Status")

        # End of Stage Output - Shows Players Hand and Revealed Cards
        print("New Stage " + self.currentGameStatus)
        self.PrintResult(finalReveal)
        cont = input("Would you like to continue playing? ('yes' or 'no') ")
        return cont

    # Burn a Card
    def BurnCard(self):
        self.burnPile.addCard(self.deck.draw())

    # Reveal a Card
    def RevealCards(self, num):
        for i in range(num):
            self.playedCards.addCard(self.deck.draw())

    # Display Final Results
    def PrintResult(self, finalReveal):
        print("REVEALED CARDS")
        print(self.playedCards.FormattedPrint())
        print("PLAYER HAND")
        print(self.playerHand.FormattedPrint())

    # Determine Winner
    # WIP
    def EvaluateResult(self):
        bestScore = self.EvaluateHand(self.playerHand)
        winner = "Player"
        opponentScores = [self.EvaluateHand(self.opponent1Hand), self.EvaluateHand(self.opponent2Hand), self.EvaluateHand(self.opponent3Hand)]
        for i in range(3):
            if opponentScores[i] > bestScore:
                bestScore = opponentScores[i]
                winner = "Opponent" + str(i)
        print("Winner: " + winner)

    # Evaluate Hand Against Revealed Cards
    # WIP
    def EvaluateHand(self, hand):
        return 0