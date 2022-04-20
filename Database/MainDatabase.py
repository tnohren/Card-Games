import sqlite3
import itertools
from sqlite3 import Error
from ConstantTables import *
from DynamicTables import *

class MainDatabase:
	def __init__(self, dbDir):
		# CREATE DB CONNECTION
		self.connection = self.CreateConnection(dbDir)
		self.constantTables = ConstantTables()
		self.dynamicTables = DynamicTables()
		
		# RUN CREATE TABLE SCRIPTS
		for script in self.constantTables.createScripts:
			self.ExecuteCreateQuery(script)
		for script in self.dynamicTables.createScripts:
			self.ExecuteCreateQuery(script)

		# POPULATE CONSTANT TABLES
		for gameType in ['Blackjack', 'Poker']:
			if self.ExecuteSelectQuery(self.constantTables.SelectGameType(gameType), [gameType]) == []:
				self.ExecuteUpdateDeleteOrInsertQuery(self.constantTables.insertGameType, [gameType])
		if len(self.ExecuteSelectQuery(self.constantTables.SelectCard())) != 52:
			snames = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
			vnames = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
			for val, st in itertools.product(range(0,13), range(0,4)):
				if self.ExecuteSelectQuery(self.constantTables.SelectCard(st, val), [st, val]) == []:
					self.ExecuteUpdateDeleteOrInsertQuery(self.constantTables.insertCard, [st, val, snames[st], vnames[val]])
		
	# EXECUTE CREATE TABLE SCRIPT
	def ExecuteCreateQuery(self, script):
		cursor = self.connection.cursor()
		try:
			cursor.execute(script)
			self.connection.commit()
		except Error as e:
			self.connection.rollback()
			print(f"Error: {e}")
			print(script)

	# EXECUTE SELECT SCRIPT - OPTIONALLY TAKE PARAMETERS
	def ExecuteSelectQuery(self, script, parameters=[]):
		cursor = self.connection.cursor()
		try:
			result = []
			if len(parameters) != 0:
				result = cursor.execute(script, parameters).fetchall()
			else:
				result = cursor.execute(script).fetchall()
		except Error as e:
			print(f"Error: {e}")
			print(script)
		return result

	# EXECUTE UPDATE, DELETE, OR INSERT SCRIPT - OPTIONALLY TAKE PARAMETERS
	def ExecuteUpdateDeleteOrInsertQuery(self, script, parameters=[]):
		cursor = self.connection.cursor()
		try:
			if len(parameters) != 0:
				cursor.execute(script, parameters)
			else:
				cursor.execute(script)
			self.connection.commit()
		except Error as e:
			self.connection.rollback()
			print(f"Error: {e}")
			print(script)
			print(parameters)

	# CREATE NEW DB CONNECTION
	def CreateConnection(self, dbDir):
		connection = None
		try:
			connection = sqlite3.connect(dbDir)
		except Error as e:
			print(f"Error: {e}")
			print(script)
		return connection

	# CLOSE DB CONNECTION
	def CloseConnection(self):
		self.connection.close()

	# LOAD LIST OF GAMES
	def LoadGamesList(self, profileName, gameType, complete):
		if complete:
			return [game[2] for game in self.ExecuteSelectQuery(self.dynamicTables.SelectCompleteGames(), [profileName, gameType])]
		else:
			return [game[2] for game in self.ExecuteSelectQuery(self.dynamicTables.SelectInProgressGames(), [profileName, gameType])]

	# LOAD ENTIRE GAME STATE
	def LoadGame(self, profileName, gameType, gameNumber):
		# Retrieve In Progress Game Info
		game = self.ExecuteSelectQuery(self.dynamicTables.SelectInProgressGames(gameNumber), [profileName, gameType, gameNumber])
		if len(game) == 0:
			return None
		gameStatus = game[0][3]

		# Retrieve Hands and Deck from Current Deck
		gameHands = [[hand[3], hand[4], hand[5]] for hand in self.ExecuteSelectQuery(self.dynamicTables.SelectProfileHand(), [profileName, gameType, gameNumber])]

		# Return Game State
		return [gameStatus, gameHands]


	# SAVE ENTIRE GAME STATE
	def SaveGame(self, profileName, gameType, gameState, hands, deck, gameNumber = 0):
		if (gameNumber == 0):
			# New Game, so Generate New Game Number and Insert Into Game Tables
			games = self.ExecuteSelectQuery(self.dynamicTables.SelectProfileGames(), [profileName, gameType])
			if len(games) == 0:
				gameNumber = 1
			else:
				gameNumber = max([game[2] for game in games]) + 1
			self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.saveProfileGame, [profileName, gameType, gameNumber, False])
			self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.saveInProgressGame, [profileName, gameType, gameNumber, gameState])
		else:
			if (gameState != "Complete"):
				# Still In Progress Game Update
				self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.updateInProgressGames, [gameState, profileName, gameType, gameNumber])
			else:
				# Remove In Progress Game Record
				self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.DeleteInProgressGame(), [profileName, gameType, gameNumber])

				# Update Profile Game Table to Mark Complete
				self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.updateProfileGame, [True, profileName, gameType, gameNumber])

				# Insert Complete Game Record if Not Exists
				if len(self.ExecuteSelectQuery(self.dynamicTables.SelectCompleteGames(gameNumber), [profileName, gameType, gameNumber])) == 0:
					self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.saveCompleteGame, [profileName, gameType, gameNumber])

		# Save Hand Info
		print(hands)
		self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.DeleteProfileHand(), [profileName, gameType, gameNumber])
		for i in range(0, len(hands)):
			player = ""
			if i == 0:
				player = "Player"
			else:
				player = "Opponent" + str(i)
			
			for card in hands[i].hd:
				self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.saveProfileHand, [profileName, gameType, gameNumber, player, card.suit, card.value])

		# Save Deck Info
		for card in deck.dk:
			self.ExecuteUpdateDeleteOrInsertQuery(self.dynamicTables.saveProfileHand, [profileName, gameType, gameNumber, "Dealer", card.suit, card.value])

		# Return Game Number - Useful in the Case of Newly Generated Game
		return gameNumber