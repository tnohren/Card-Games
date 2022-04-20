"""
LIST OF CONSTANT TABLES
ctabGameType - Holds All Available Game Types
ctabCard - Holds All Available Cards
"""
class ConstantTables:
    # CREATE SCRIPTS
    createGameTypeTable = """
        CREATE TABLE IF NOT EXISTS ctabGameType (
            gameType TEXT NOT NULL,
            PRIMARY KEY (gameType)
        )
    """
    createCardTable = """
        CREATE TABLE IF NOT EXISTS ctabCard (
            cardSuit INTEGER NOT NULL,
            cardValue INTEGER NOT NULL,
            cardSuitDisplay TEXT NOT NULL,
            cardValueDisplay TEXT NOT NULL,
            PRIMARY KEY (cardSuit, cardValue)
        )
    """
    def __init__(self):
        self.createScripts = [self.createGameTypeTable, self.createCardTable]

    # INSERT SCRIPTS
    insertGameType = "INSERT INTO ctabGameType (gameType) VALUES (?)"
    insertCard = "INSERT INTO ctabCard (cardSuit, cardValue, cardSuitDisplay, cardValueDisplay) VALUES (?,?,?,?)"

    # SELECT SCRIPTS
    def SelectGameType(self, gameType = ""):
        script = "SELECT gameType FROM ctabGameType"
        if (gameType != ""):
            script += " WHERE gameType = ?"
        return script

    def SelectCard(self, cardSuit = -1, cardValue = -1):
        script = "SELECT cardSuit, cardValue, cardSuitDisplay, cardValueDisplay FROM ctabCard"
        if (cardSuit != -1 and cardValue != -1):
            script += " WHERE cardSuit = ? AND cardValue = ?"
        return script