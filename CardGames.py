import sys
sys.path.append('./PrimaryWindow')
sys.path.append('./Blackjack')
sys.path.append('./Poker')
sys.path.append('./Currency')
sys.path.append('./Database')
from PrimaryWindow import *
from Poker import *
from Blackjack import *
from Currency import *
from MainDatabase import *

def play():
    # Initialize Chips
    # TODO

    # Start New Window
    window = Window()

    # Initialize Database
    database = MainDatabase("app_db.sqlite")

    # Retrieve List of Profiles
    profiles = database.ExecuteSelectQuery(database.dynamicTables.SelectProfile())

    # Create User Prompt
    promptChoices = []
    if profiles != []:
        promptChoices = [profile[0] for profile in profiles]
    promptChoices.append('New Profile')

    # Display User Prompt
    profileChoice = window.AddPrompt(["Which profile would you like to use?"], promptChoices)

    # Create a New Profile
    if profileChoice == 'New Profile':
        profileChoice = window.AddTextInput(["Please Input Your New Profile Name", "Press the Enter Key When Finished"])

        # Verify Profile Name's Uniqueness
        profiles = database.ExecuteSelectQuery(database.dynamicTables.SelectProfile(profileChoice), [profileChoice])

        while profiles != []:
            # Continue prompting the user until a unique profile name is chosen
            profileChoice = window.AddTextInput(["The Profile Name Chosen Has Already Been Used. Please Input a Different Profile Name.", "Press the Enter Key when Finished"])
            profiles = database.ExecuteSelectQuery(database.dynamicTables.SelectProfile(profileChoice), [profileChoice])

        # Insert New Profile Into Database
        database.ExecuteUpdateDeleteOrInsertQuery(database.dynamicTables.saveProfile, [profileChoice])      

    # Retrieve List of Available Game Types
    gameTypes = [gameType[0] for gameType in database.ExecuteSelectQuery(database.constantTables.SelectGameType())]

    # Ask User Which Game They Would Like to Play
    gameType = window.AddPrompt(["Which card game would you like to play?"], gameTypes)
    if gameType == 'Blackjack':
        game = Blackjack(window, database, profileChoice)
    elif gameType == 'Poker':
        game = Poker(window, database, profileChoice)
    else:
        print("Invalid input")

    window.Quit()
    quit()

play()