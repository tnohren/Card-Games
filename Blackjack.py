# Blackjack.py
from CardandDeck import *

# This is a simple text-based blackjack game
# In its current state, it does not handle splitting

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

def play():
    play = 'yes'
    while(play != 'no'):
        print("NEW GAME STARTED")

        # Initializing the deck to play with
        deck = Deck()
        deck.shuffle()

        # Initializing the player's and dealer's hand
        playerHand = Hand(2, deck)
        dealerHand = Hand(2, deck)

        # Display the player's hand to the player
        # Also display all but the dealer's first card
        playerShow(playerHand)
        dealerShow(dealerHand)

        # Initialize player and dealer scores
        playerScore = calcPlayerScore(playerHand)
        dealerScore = calcDealerScore(dealerHand)

        # Initializing boolean for bust
        playerBust = dealerBust = False

        # Ask the player if they'd like to hit or stay. We will continue in the while loop
        # until the player is satisfied with their current hand or until they bust
        hit = input("would you like to hit or stay? (Type 'hit' or 'stay') ")
        print("\n")
        while (hit != 'hit' and hit != 'stay'):
               hit = input("Invalid input. Please type 'hit' or 'stay': ")

        while (hit != 'stay'):
               # If the player decided to hit, then deal them a new card
               playerHand.hd.append(deck.draw())
               playerShow(playerHand)

               # Re-calculate the player's score
               playerScore = calcPlayerScore(playerHand)

               # If the player ended with a value greater
               hit, playerBust = bustChecker(playerScore)

               # If they did not bust, then ask them if they would like to hit or stay
               if (not playerBust):
                   print("Your current score is: %d" % (playerScore))
                   hit = input("Would you like to hit or stay? (Type 'hit' or 'stay') ")
                   print("\n")

        # They dealer should continue to draw as long as he has a total score less than 16
        # or as long as dealer hasn't already beaten the player
        while ((dealerScore < 16) and (playerBust == False) and (dealerScore <= playerScore)):
               # Give the dealer a new card
               dealerHand.hd.append(deck.draw())

               # Print the dealer's current hand with the exception of first card
               dealerShow(dealerHand)

               # Calculate dealer's score
               dealerScore = calcDealerScore(dealerHand)
               temp, dealerBust = bustChecker(dealerHand)

        # Show both the player's and dealer's full hands
        print("\nPlayer's Final Hand")
        playerShow(playerHand)
        print("\nDealer's Final Hand")
        dealerShow(dealerHand, 1)

        # Print out the final scoreboard for the player to see
        print("\nDealer Score: %d      Player Score: %d\n" % (dealerScore, playerScore))

        # Determine who lost and print the result
        if (playerBust):
               print("Player lost -- Busted :(")
        elif (dealerBust):
                print("You win -- Dealer Busted :D")
        else:
               if (playerScore > dealerScore):
                   print("You win! -- Higher Score :D")
               elif (playerScore == dealerScore):
                   print("Tie! -- Same Score")
               else:
                   print("Dealer won -- Higher Score :(")

        # Ask if the player would like to play a new hand
        play = input("Would you like to continue playing? (yes or no) ")


play()

               
