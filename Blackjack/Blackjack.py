# Blackjack.py
from CardandDeck import *
from blackjack_functionality import *

# This is a simple text-based blackjack game
# In its current state, it does not handle splitting

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
               temp, dealerBust = bustChecker(dealerScore)

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

               
