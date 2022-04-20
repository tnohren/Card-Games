"""
LIST OF DYNAMIC TABLES
dtabProfile - All User Profiles
dtabProfileChips - Holds Each Profile's Chip Amounts
dtabProfileGame - Holds Each Profile's Games, Complete and In Progress
dtabProfileHand - Holds Each Game's Hands
dtabCompleteGame - Holds Each Profile's Complete Games
dtabInProgressGames - Holds Each Profile's In Progress Games
"""
class DynamicTables:
	# CREATE TABLE SCRIPTS
	createProfileTable = """
		CREATE TABLE IF NOT EXISTS dtabProfile (
			profileName TEXT NOT NULL,
			PRIMARY KEY (profileName)
		);
	"""
	createProfileChipTable = """
		CREATE TABLE IF NOT EXISTS dtabProfileChips (
			profileName TEXT NOT NULL,
			chipValue INTEGER NOT NULL,
			chipAmount INTEGER NOT NULL,
			FOREIGN KEY (profileName) REFERENCES dtabProfile(profileName),
			PRIMARY KEY (profileName, chipValue)
		);
	"""
	createProfileGameTable = """
		CREATE TABLE IF NOT EXISTS dtabProfileGame (
			profileName TEXT NOT NULL,
			gameType TEXT NOT NULL,
			gameNumber INTEGER NOT NULL,
			gameOutcome BOOLEAN,
			FOREIGN KEY (profileName) REFERENCES dtabProfile(profileName),
			FOREIGN KEY (gameType) REFERENCES ctabGameType(gameType),
			PRIMARY KEY(profileName, gameType, gameNumber)
		)
	"""
	createProfileHandTable = """
		CREATE TABLE IF NOT EXISTS dtabProfileHand (
			profileName TEXT NOT NULL,
			gameType TEXT NOT NULL,
			gameNumber INTEGER NOT NULL,
			gamePlayer TEXT NOT NULL,
			cardSuit INTEGER NOT NULL,
			cardValue INTEGER NOT NULL,
			FOREIGN KEY (profileName) REFERENCES dtabProfile(profileName),
			FOREIGN KEY (gameType) REFERENCES ctabGameType(gameType),
			FOREIGN KEY (gameNumber) REFERENCES ctabGameProfileGame(gameNumber),
			PRIMARY KEY (profileName, gameType, gameNumber, gamePlayer, cardSuit, cardValue)
		);
	"""
	createCompleteGameTable = """
		CREATE TABLE IF NOT EXISTS dtabCompleteGames (
			profileName TEXT NOT NULL,
			gameType TEXT NOT NULL,
			gameNumber INTEGER NOT NULL,
			FOREIGN KEY (profileName) REFERENCES dtabProfile(profileName),
			FOREIGN KEY (gameType) REFERENCES ctabGameType(gameType),
			FOREIGN KEY (gameNumber) REFERENCES dtabProfileGame(gameNumber),
			PRIMARY KEY (profileName, gameType, gameNumber)
		);
	"""
	createInProgressGameTable = """
		CREATE TABLE IF NOT EXISTS dtabInProgressGames (
			profileName TEXT NOT NULL,
			gameType TEXT NOT NULL,
			gameNumber INTEGER NOT NULL,
			gameStatus TEXT NOT NULL,
			FOREIGN KEY (profileName) REFERENCES tabProfile(profileName),
			FOREIGN KEY (gameType) REFERENCES ctabGameType(gameType),
			FOREIGN KEY (gameNumber) REFERENCES dtabProfileGame(gameNumber),
			PRIMARY KEY (profileName, gameType, gameNumber)
		);
	"""

	# INSERT SCRIPTS
	saveProfile = "INSERT INTO dtabProfile (profileName) VALUES (?)"
	saveProfileChips = "INSERT INTO dtabProfileChips (profileName, chipValue, chipAmount) VALUES (?, ?, ?)"
	saveProfileGame = "INSERT INTO dtabProfileGame (profileName, gameType, gameNumber, gameOutcome) VALUES (?, ?, ?, ?)"
	saveProfileHand = "INSERT INTO dtabProfileHand (profileName, gameType, gameNumber, gamePlayer, cardSuit, cardValue) VALUES (?, ?, ?, ?, ?, ?)"
	saveCompleteGame = "INSERT INTO dtabCompleteGames (profileName, gameType, gameNumber) VALUES (?, ?, ?)"
	saveInProgressGame = "INSERT INTO dtabInProgressGames (profileName, gameType, gameNumber, gameStatus) VALUES (?, ?, ?, ?)"

	# UPDATE SCRIPTS
	updateProfileChips = "UPDATE dtabProfileChips SET chipAmount = ? WHERE profileName = ? AND chipValue = ?"
	updateProfileGame = "UPDATE dtabProfileGames SET gameOutcome = ? WHERE profileName = ? AND gameType = ? AND gameNumber = ?"
	updateInProgressGames = "UPDATE dtabInProgressGames SET gameStatus = ? WHERE profileName = ? AND gameType = ? AND gameNumber = ?"

	def __init__(self):
		self.createScripts = [self.createProfileTable, self.createProfileChipTable, self.createProfileGameTable, self.createProfileHandTable, self.createCompleteGameTable, self.createInProgressGameTable]

	# SELECT SCRIPTS
	def SelectProfile(self, profileName=""):
		script = "SELECT profileName FROM dtabProfile"
		if profileName != "":
			script += (" WHERE profileName = ?")
		return script

	def SelectProfileChips(self, chipValue = -1):
		script = "SELECT profileName, chipValue, chipAmount FROM dtabProfileChips WHERE profileName = ?"
		if (chipValue != -1):
			script += (" AND chipValue = ?")
		return script

	def SelectProfileGames(self, gameNumber = -1):
		script = "SELECT profileName, gameType, gameNumber, gameOutcome FROM dtabProfileGame WHERE profileName = ? AND gameType = ?"
		if gameNumber != -1:
			script += (" AND gameNumber = ?")
		return script

	def SelectProfileHand(self, gamePlayer = ""):
		script = "SELECT profileName, gameType, gameNumber, gamePlayer, cardSuit, cardValue FROM dtabProfileHand WHERE profileName = ? AND gameType = ? AND gameNumber = ?"
		if gamePlayer != "":
			script += " AND gamePlayer = ?"
		return script

	def SelectCompleteGames(self, gameNumber = -1):
		script = "SELECT profileName, gameType, gameNumber FROM dtabCompleteGames WHERE profileName = ? AND gameType = ?"
		if (gameNumber != -1):
			script += (" AND gameNumber = ?")
		return script

	def SelectInProgressGames(self, gameNumber = -1):
		script = "SELECT profileName, gameType, gameNumber, gameStatus FROM dtabInProgressGames WHERE profileName = ? AND gameType = ?"
		if (gameNumber != -1):
			script += (" AND gameNumber = ?")
		return script

	# DELETE SCRIPTS
	def DeleteProfileHand(self, gamePlayer = -1, cardSuit = -1, cardValue = -1):
		script = "DELETE FROM dtabProfileHand WHERE profileName = ? AND gameType = ? AND gameNumber = ?"
		if (gamePlayer != -1):
			script += (" AND gamePlayer = ?")
			if (cardSuit != -1 and cardValue != -1):
				script += (" AND cardSuit = ? AND cardValue = ?")
		return script

	def DeleteInProgressGame(self):
		return "DELETE FROM dtabInProgressGames WHERE profileName = ? AND gameType = ? AND gameNumber = ?"