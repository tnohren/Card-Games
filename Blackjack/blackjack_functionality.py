# Print the player's hand
def playerShow(playerHand):
    print("Player's hand: ")
    print(playerHand)
    print("\n")

# Print the dealer's hand, with the exception of the first card
def dealerShow(dealerHand, final = 0):
    print("Dealer's hand: ")
    for card in dealerHand.hd:
        if (final == 0):
            final += 1
        else:
            print(card)
    print("\n")

# Calculate the player's current score
def calcPlayerScore(hand):
    playerScore = 0
    for card in hand.hd:
        # If the player drew an ace, then ask them what they'd like it to count as
        if (card.value == 0):
            playerScore += int(input("Would you like your Ace to be 1 or 11? "))
            print("\n")
        # If the player drew a 10, Jack, Queen, or King, then add 10 to their score
        elif (card.value > 8):
            playerScore += 10
        # Otherwise, add the face value of the card
        else:
            playerScore += card.value + 1
    return playerScore

# Calculate the dealer's current score
def calcDealerScore(hand):
    # Hold the dealer's aces until the end so we can determine
    # the best course of action with their scoring
    dealerScore = 0
    aces = []

    # Determine the value of the dealer's hand
    for card in hand.hd:
        # If we get an ace, we deal with it after all other cards are added into the value
        if (card.value == 0):
            aces.append(card)
        # Continue the valuation process as normal
        elif (card.value > 8):
            dealerScore += 10
        else:
            dealerScore += card.value

    # We need to determine what value to give the aces
    # If the dealer has a score less than 11 - number of aces
    # Then we can give the current ace a value of 11
    # All following aces will be given a value of 1
    for card in aces:
        if (dealerScore < (11 - len(aces))):
            dealerScore += 11
        else:
            dealerScore += 1
    return dealerScore

# Check if a player busted
def bustChecker(score):
    if (score > 21):
        return ('stay', True)
    else:
        return ('hit', False)

# Checking if player wants to continue a previously saved game
def contGame():
    cont = input("Would you like to continue a saved game? (yes or no) ")
    if (cont):
        readGame = open("saved.txt", "r+")
        return readGame
    else:
        return 0
