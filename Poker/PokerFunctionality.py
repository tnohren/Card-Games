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
        self.end = "Complete"

# Handles General Game Flow and Stores Game State
class GameState:
    def __init__(self, window, database, playerName):
        self.playerName = playerName
        self.gameStruct = GameStruct()
        cont = window.AddPrompt(['Welcome to Poker'], ['Load Game', 'New Game', 'Options'])
        #cont = input("Would you like to continue a previously saved game? ('yes' or 'no') ")
        if (cont == 'Load Game'):
            self.LoadGame(window, database)
        elif (cont == 'New Game'):
            self.NewGame(window, database)
        else:
            print("Invalid input")
            window.Quit()
            quit()

    def __str__(self):
        # Format string for saving
        # First line contains number of cards in the deck, number of cards that have been revealed, and the number of cards in the burn pile.
        # Each subsequent line is a unique card: first is the player's hand, then the opponents' hands, then revealed cards, then burned cards, and finally cards remaining in the deck.
        saveString = str(len(self.deck)) + ',' + str(len(self.playedCards)) + ',' + str(len(self.burnPile)) + '\n'
        saveString += str(self.playerHand) + '\n' + str(self.opponent1Hand) + '\n' + str(self.opponent2Hand) + '\n' + str(self.opponent3Hand) + '\n' + str(self.playedCards) + '\n' + str(self.burnPile) + '\n' + str(self.deck)
        return saveString

    def LoadGame(self, window, database):
        savedGames = database.LoadGamesList(self.playerName, "Poker", False)

        if (len(savedGames) == 0):
            window.AddPrompt(["You have no saved games. Please start a new game."], ["New Game"])
            self.NewGame(window, database)
        else:
            # Ask user which game to continue playing
            self.gameNumber = int(window.AddPrompt(["Which save game would you like to continue playing?"], savedGames))
            game = database.LoadGame(self.playerName, "Poker", self.gameNumber)
			
            # Set Current Game Status
            self.currentGameStatus = game[0]

            # Initialize and build all card piles - hands, played cards, burn pile, deck
            cardPiles = game[1]
            self.playerHand = Hand()
            self.opponent1Hand = Hand()
            self.opponent2Hand = Hand()
            self.opponent3Hand = Hand()
            self.playedCards = Hand()
            self.burnPile = Hand()
            self.deck = Deck(False)
            for i in range(0, len(cardPiles)):
                if (cardPiles[i][0] == "Player"):
                    self.playerHand.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                elif (cardPiles[i][0] == "Opponent1"):
                    self.opponent1Hand.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                elif (cardPiles[i][0] == "Opponent2"):
                    self.opponent2Hand.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                elif (cardPiles[i][0] == "Opponent3"):
                    self.opponent3Hand.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                elif (cardPiles[i][0] == "Opponent4"):
                    self.burnPile.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                elif (cardPiles[i][0] == "Opponent5"):
                    self.playedCards.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))
                else:
                    self.deck.AddCard(Card(int(cardPiles[i][1]), int(cardPiles[i][2])))

            print("PARSED CARD PILES: ")
            print([self.playerHand, self.opponent1Hand, self.opponent2Hand, self.opponent3Hand, self.burnPile, self.playedCards])
        
    # Begin New Game
    def NewGame(self, window, database):
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
        self.gameNumber = int(database.SaveGame(self.playerName, "Poker", self.currentGameStatus, [self.playerHand, self.opponent1Hand, self.opponent2Hand, self.opponent3Hand, self.burnPile, self.playedCards], self.deck))

    # Save In Progress Game
    def SaveGame(self, database):
        database.SaveGame(self.playerName, "Poker", self.currentGameStatus, [self.playerHand, self.opponent1Hand, self.opponent2Hand, self.opponent3Hand, self.burnPile, self.playedCards], self.deck, self.gameNumber)

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
    def NextGameStep(self, window, database):
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
            cont = window.AddPrompt(["Would you like to begin a new game?"], ['Yes', 'No'])
            if (cont == 'Yes'):
                self.NewGame(window, database)           
            return cont
        else:
            print("Exception Caught - Invalid Game Status")

        # End of Stage Output - Shows Players Hand and Revealed Cards
        print("New Stage " + self.currentGameStatus)
        self.PrintResult(finalReveal)
        self.SaveGame(database)
        cont = window.AddPrompt(["Your Cards: " + self.playerHand.FormattedPrint(), "Revealed Cards: " + self.playedCards.FormattedPrint(), "Would you like to continue playing?"], ['Yes', 'No'])
        return cont

    # Burn a Card
    def BurnCard(self):
        self.burnPile.AddCard(self.deck.draw())

    # Reveal a Card
    def RevealCards(self, num):
        for i in range(num):
            self.playedCards.AddCard(self.deck.draw())

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