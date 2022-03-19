import os.path
import sys
sys.path.append('./Currency')
from CurrencyManagement import *

# Poker Chip State
class PokerChipHandler:
    def __init__(self):
        # Load chips if an existing save file exists, otherwise begin with a new set of chips
        if (os.path.isfile('saved_poker_chips.txt')):
            self.LoadChips()
        else:
            self.gameChips = GameChips(40, 20, 8, 4)
            self.playerChips, self.opponent1Chips, self.opponent2Chips, self.opponent3Chips = self.gameChips.InitializePurses(4)

        # Verify All Chips Add Up and Print Result
        if self.VerifyChipIntegrity():
            print("Your Chip Value: " + str(self.playerChips.totalValue))
        else:
            print("Failed Chip Initialization")

    # Formatted str
    def __str__(self):
        result = []
        for chipSet in [self.gameChips, self.playerChips, self.opponent1Chips, self.opponent2Chips, self.opponent3Chips]:
            result.append(str(chipSet))
        return '\n'.join(result)

    # Chip Verification Function
    def VerifyChipIntegrity(self):
        return self.gameChips.VerifyIntegrity([self.playerChips, self.opponent1Chips, self.opponent2Chips, self.opponent3Chips])

    # Save Chip State
    def SaveChips(self):
        with open('saved_poker_chips.txt', 'w') as savefile:
            savefile.write(str(self))

    # Load Chips from Saved Chip File
    def LoadChips(self):
        with open('saved_poker_chips.txt', 'r+') as readGame:
            readLines = [line.rstrip().split(',') for line in readGame]
            self.gameChips = GameChips(int(readLines[0][0]), int(readLines[0][1]), int(readLines[0][2]), int(readLines[0][3]))
            self.playerChips = Purse(int(readLines[1][0]), int(readLines[1][1]), int(readLines[1][2]), int(readLines[1][3]))
            self.opponent1Chips = Purse(int(readLines[2][0]), int(readLines[2][1]), int(readLines[2][2]), int(readLines[2][3]))
            self.opponent2Chips = Purse(int(readLines[3][0]), int(readLines[3][1]), int(readLines[3][2]), int(readLines[3][3]))
            self.opponent3Chips = Purse(int(readLines[4][0]), int(readLines[4][1]), int(readLines[4][2]), int(readLines[4][3]))

    # Handles Placing Bets
    def PlaceBets(self):
        self.PlayerBet()
        for opp in [self.opponent1Chips, self.opponent2Chips, self.opponent3Chips]:
            self.HandleOpponentBet(opp)

    # Allow Player to Place Bet
    def PlayerBet(self):
        return

    # Automatically Handle Opponent Bets
    def HandleOpponentBet(self):
        return