# CurrencyManagement.py
import math

# Basic Chip
class Chip:
    def __init__(self, value):
        self.value = value

# Basic Chip Pile
class ChipPile():
    def __init__(self, num1, num5, num10, num25):
        # Initialize Chips
        self.num1 = num1
        self.num5 = num5
        self.num10 = num10
        self.num25 = num25
        self.BuildChips()

    def __str__(self):
        return str(self.num1) + ',' + str(self.num5) + ',' + str(self.num10) + ',' + str(self.num25)

    # Build Chip List
    def BuildChips(self):
        self.chips = []
        self.AddChips(self.num1, 1)
        self.AddChips(self.num5, 5)
        self.AddChips(self.num10, 10)
        self.AddChips(self.num25, 25)
        self.CalcTotalValue()

    # Add Chips
    def AddChips(self, num, value):
        for i in range(num):
            self.chips.append(Chip(value))

    # Calculate Total Value of All Chips in Game
    def CalcTotalValue(self):
        self.totalValue = 0
        for chip in self.chips:
            self.totalValue += chip.value
        return self.totalValue

# Set of All Game Chips
class GameChips(ChipPile):
    def __init__(self, num1, num5, num10, num25):
        super().__init__(num1, num5, num10, num25)

    # Verify Integrity of Total Chips in Play
    def VerifyIntegrity(self, listOfChipPiles):
        tempValue = 0
        for chipPile in listOfChipPiles:
            tempValue += chipPile.CalcTotalValue()
        return tempValue == self.CalcTotalValue()

    def InitializePurses(self, numPlayers):
        purseList = []
        for i in range(numPlayers):
            purseList.append(Purse(math.floor(self.num1 / numPlayers), math.floor(self.num5 / numPlayers), math.floor(self.num10 / numPlayers), math.floor(self.num25 / numPlayers)))
        return purseList

# Chip Piles in Play (Player's Chip Piles and the Pot)
class ActivePile(ChipPile):
    def __init__(self, num1, num5, num10, num25):
        super().__init__(num1, num5, num10, num25)

    # Remove Chips from Chip List
    def RemoveChips(self, num1, num5, num10, num25):
        if (self.num1 < num1 or self.num5 < num5 or self.num10 < num10 or self.num25 < num25):
            print("Invalid Removal Amount")
            return
        self.num1 -= num1
        self.num5 -= num5
        self.num10 -= num10
        self.num25 -= num25
        self.BuildChips()

    # Add Chips When Player Has Won
    def Won(self, num1, num5, num10, num25):
        self.num1 += num1
        self.num5 += num5
        self.num10 += num10
        self.num25 += num25
        self.BuildChips()

    # Remove All Chips From Pile
    def Clear(self):
        self.num1 = self.num5 = self.num10 = self.num25 = 0
        self.chips = []
        self.totalValue = 0

# A Player's Set of Chips
class Purse(ActivePile):
    def __init__(self, num1, num5, num10, num25):
        super().__init__(num1, num5, num10, num25)

# Betting Pot
class Pot(ActivePile):
    def __init__(self, num1, num5, num10, num25):
        super().__init__(num1, num5, num10, num25)