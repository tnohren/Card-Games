import os.path
import time
import sys
sys.path.append('./CardandDeck')
from CardandDeck import *

class GameStruct:
	def __init__(self):
		self.playerTurn = 'Player Turn'
		self.dealerTurn = 'Dealer Turn'

class GameState:
	def __init__(self, window):
		# Game Struct for keeping track of turn
		self.gameStruct = GameStruct()
		self.gameState = self.gameStruct.playerTurn

		# Ask player if they'd like to load an existing game or start a new game
		cont = window.AddPrompt(['Welcome to Blackjack'], ['Load Game', 'New Game', 'Options'])
		if (cont == 'Load Game'):
			self.LoadGame(window)
		elif (cont == 'New Game'):
			self.NewGame(window)
		elif (cont == 'Options'):
			print ("OPTIONS - FILL OUT")
		else:
			print("Invalid input")
			window.Quit()
			quit()

	# Format String for Saving
	def __str__(self):
		# To store whose turn it currently is
		turnDigit = '0'
		if self.gameState == self.gameStruct.dealerTurn:
			turnDigit = '1'

		# Format for saving
		# First line contains length of player hand, length of dealer hand, length of deck
		# Subsequent lines are in the order: cards in player's hand, cards in dealer's hand, cards in deck
		return str(len(self.playerHand)) + ',' + str(len(self.dealerHand)) + ',' + str(len(self.deck)) + ',' + turnDigit + '\n' + str(self.playerHand) + '\n' + str(self.dealerHand) + '\n' + str(self.deck)

	def SaveGame(self, window):
		# Save game
		overwrite = 'Yes'
		if (os.path.isfile('saved_blackjack.txt')):
			overwrite = window.AddPrompt(['Are you sure you would like to overwrite your previously saved game?'], ['Yes', 'No'])
		if (overwrite == 'Yes'):
			with open('saved_blackjack.txt', 'w') as savefile:
				savefile.write(str(self))

	def LoadGame(self, window):
		# Read in Saved Game File
		with open('saved_blackjack.txt.', 'r+') as readGame:
			readLines = [line.rstrip().split(',') for line in readGame]

			# Read Card Pile Sizes (Hands and Deck) From File
			currentPlayerSize = int(readLines[0][0])
			currentDealerSize = int(readLines[0][1])
			currentDeckSize = int(readLines[0][2])

			# Read Game State From File
			if (int(readLines[0][3]) == 1):
				self.gameState = self.gameStruct.playerTurn
			else:
				self.gameState = self.gameStruct.dealerTurn

			# Used For Determining How To Read Save File
			currentPlayerLines = range(1, currentPlayerSize + 1)
			currentDealerLines = range(currentPlayerSize + 1, currentPlayerSize + currentDealerSize + 2)
			currentDeckLines = range(currentPlayerSize + currentDealerSize + 2, currentPlayerSize + currentDealerSize + currentDeckSize + 3)

			# Initialize Game Pieces
			self.playerHand = Hand()
			self.dealerHand = Hand()
			self.deck = Deck(False)

			# Read Saved Game Data
			for i in range(1, len(readLines)):
				# Card in Player's Hand
				if i in currentPlayerLines:
					self.playerHand.AddCard(Card(int(readLines[i][1]), int(readLines[i][0])))
				# Card in Dealer's Hand
				elif i in currentDealerLines:
					self.dealerHand.AddCard(Card(int(readLines[i][1]), int(readLines[i][0])))
				# Card in Deck
				elif i in currentDeckLines:
					self.deck.AddCard(Card(int(readLines[i][1]), int(readLines[i][0])))

			# Initialize Scores
			self.playerScore = self.CalcPlayerScore(window)
			self.dealerScore = self.CalcDealerScore()

	def NewGame(self, window):
		# Initializing New Deck to Play With
		self.deck = Deck(True)
		self.deck.shuffle()

		# Deal Hands
		self.playerHand = Hand(2, self.deck)
		self.dealerHand = Hand(2, self.deck)

		# Initialize Scores
		self.playerScore = self.CalcPlayerScore(window)
		self.dealerScore = self.CalcDealerScore()

	def PlayerTurn(self, window):
		playerChoice = 'Hit'
		while playerChoice == 'Hit':
			# Give player option of getting new card
			if (self.CalcPlayerScore(window) < 21):
				playerChoice = window.AddPrompt(['Your Cards: ' + self.playerHand.FormattedPrint(), 'Dealer Cards: ' + self.dealerHand.FormattedPrint(), 'Would you like to hit or stay?'], ['Hit', 'Stay', 'Quit'])
				if playerChoice == 'Hit':
					# Give player a new card from the deck
					self.playerHand.AddCard(self.deck.draw())
				elif playerChoice == 'Quit':
					# Save Game and quit
					self.SaveGame(window)
					window.Quit()
					quit()
				else:
					# Return whether the player busted or not
					return (self.playerScore <= 21)
			else:
				# Player busted
				return False

	def DealerTurn(self, window):
		play = 'Yes'
		# Dealer keeps playing until their score is greater than 16 or the player decides to quit
		while (self.dealerScore < 16 and play == 'Yes'):
			self.dealerHand.AddCard(self.deck.draw())
			play = window.AddPrompt(['Your Cards: ' + self.playerHand.FormattedPrint(), 'Dealer Cards: ' + self.dealerHand.FormattedPrint(), 'Would you like to keep playing?'], ['Yes', 'No'])
			if play == 'No':
				# Save game and quit
				self.SaveGame(window)
				window.Quit()
				quit()
			# Give dealer new card
			self.dealerHand.AddCard(self.deck.draw())
			self.CalcDealerScore()
		# Return whether the dealer busted or not
		return (self.dealerScore <= 21)

	def GameFlow(self, window):
		# If it's the player's turn, conduct player turn
		if self.gameState == self.gameStruct.playerTurn:
			playerResult = self.PlayerTurn(window)
			if not playerResult:
				# Player Busted - Display result and ask if user would like to start a new game
				nextAction = window.AddPrompt(['Dealer wins. You busted :(', 'Would you like to start a new game or quit?'], ['New Game', 'Quit'])
				if nextAction == 'New Game':
					# Start new game
					self.NewGame(window)
					self.GameFlow(window)
				else:
					# Quit - no save, since at end of game
					window.Quit()
					quit()
				return

		# If it's the dealer's turn, conduct dealer turn
		self.gameState = self.gameStruct.dealerTurn
		resultMessage = ""
		if self.DealerTurn(window):
			if self.playerScore > self.dealerScore:
				resultMessage = "You win!"
			elif self.playerScore < self.dealerScore:
				resultMessage = "Dealer wins :("
			else:
				resultMessage = "Tie!"
		else:
			# Dealer busted
			resultMessage = "You win!"

		# Display result and ask if user would like to start a new game
		nextAction = window.AddPrompt([resultMessage, 'Your Score: ' + str(self.playerScore), 'Dealer Score: ' + str(self.dealerScore), 'Would you like to start a new game or quit?'], ['New Game', 'Quit'])
		if nextAction == 'New Game':
			# Start a new game
			self.NewGame(window)
			self.GameFlow(window)
		else:
			# Quit - no save, since at end of game
			window.Quit()
			quit()
		return

	def CalcPlayerScore(self, window):
		self.playerScore = 0
		for card in self.playerHand.hd:
			# If the player drew an ace, then ask them what they'd like it to count as
			if (int(card.value) == 0):
				self.playerScore += int(window.AddPrompt(['Your Cards: ' + self.playerHand.FormattedPrint(), 'Would you like your Ace to be 1 or 11?'], ['1', '11']))
			# If the player drew a 10, Jack, Queen, or King, then add 10 to their score
			elif (int(card.value) > 8):
				self.playerScore += 10
			# Otherwise, add the face value of the card
			else:
				self.playerScore += card.value + 1
		return self.playerScore

	def CalcDealerScore(self):
		# Hold the dealer's aces until the end so we can determine
		# the best course of action with their scoring
		self.dealerScore = 0
		aces = []

		# Determine the value of the dealer's hand
		for card in self.dealerHand.hd:
			# If we get an ace, we deal with it after all other cards are added into the value
			if (card.value == 0):
				aces.append(card)
			# Continue the valuation process as normal
			elif (card.value > 8):
				self.dealerScore += 10
			else:
				self.dealerScore += card.value + 1

		# We need to determine what value to give the aces
		# If the dealer has a score less than 11 - number of aces
		# Then we can give the current ace a value of 11
		# All following aces will be given a value of 1
		for card in aces:
			if (self.dealerScore < (11 - len(aces))):
				self.dealerScore += 11
			else:
				self.dealerScore += 1
		return self.dealerScore