import random
import time

# I did look up how to handle the array structures on google.
# I did look up what's the most optimal hand for a dealer when given aces. Google said at casinos, if they start with two aces they count both of them as one 11 and one 1 instead of two 1's. User picks besides when given 21.

worth_ten = ["10", "K", "Q", "J"]
first_time = True

# Here's a helpful function to help you get started.
def create_deck():
    """Create a standard 52-card deck"""
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

# You can use this to draw a face-down card 
def face_down_card():
  return "▓"

def is_blackjack(cards):        # Checks for Blackjack
  ranks = [r for r, _ in cards]
  return ('A' in ranks) and any(r in worth_ten for r in ranks)

def card_value(card):           # This reads the int value of all cards BESIDES aces, I did aces manually
  if(card[0] in worth_ten):
    return 10
  else:
    return int(card[0])

def play_again(pref):           # Helper function to ask the user if they desire to keep playing
  answer = input(f"Would you like to play again {pref}? (y/n)\n")
  if(answer == "y"):
    print("\n\n\n\n")
    print("Awesome, let's go again.\n")
    main(pref)
  else:
    print(f"Have a great day {pref}.\n")
    exit()

def main(pref=None):    
  player_tot = 0        # Hand sum totals
  dealer_tot = 0
  global first_time     # Keeps track of they have been at the table already or not
  if first_time:        # Asks for prefered name
      pref = input("Would you prefer to be called sir, ma’am or your name?\n")
      if (pref == "name"):
        pref = input("What is your name?\n")
      print("Awesome, let's start playing.\n")
      first_time = False

  deck = create_deck()  # Creates deck and shuffles it
  random.shuffle(deck)

  dealer_cards = [deck.pop(), deck.pop()]   # Grabs two cards for each person
  player_cards = [deck.pop(), deck.pop()]

  time.sleep(1)   # Introduces cards with desired delay
  print(f"My first card is a {dealer_cards[0]} and my other card is face down {face_down_card()}.\n") 
  time.sleep(1)
  print(f"Your cards are {player_cards[0]} and {player_cards[1]}.\n")
  time.sleep(1)

  # dealer_bj = is_blackjack(dealer_cards)    # Prof doesn't want us to check to blackjack from the dealer initially :(
  player_bj = is_blackjack(player_cards)    # Checks player for blackjack
  # if dealer_bj or player_bj:
  #     print(f"My face-down card was {dealer_cards[1]}.")
  #     if dealer_bj and player_bj:
  #         print("We both have Blackjack! It's a push.\n")
  #     elif dealer_bj:
  #         print(f"I have a Blackjack and I win, {pref}!\n")
  #     else:
  #         print("You have a Blackjack! You win!\n")
  #     return play_again(pref)
  if player_bj:   
    print("You have a Blackjack! You win!\n")
    return play_again(pref)

  if(player_cards[0][0] == "A" and player_cards[1][0] == "A"):    # Asks user what they want to do with their aces. User has all the freedom
    num_elev = int(input("You have two aces, how many of them do you want to to be an eleven instead of ones? (0, 1 or 2)\n"))
    non_elev = 2 - num_elev
    player_tot += ((num_elev*11) + non_elev)
  elif(player_cards[0][0] == "A" and player_cards[1][0] != "A"):
    num_elev = int(input(f"Would you like your ace to be an eleven or one {pref}? (11/1)\n"))
    player_tot += (int(num_elev) + card_value(player_cards[1]))
  elif(player_cards[1][0] != "A" and player_cards[0][0] == "A"):
    num_elev = int(input(f"Would you like your ace to be an eleven or one {pref}? (11/1)\n"))
    player_tot += (int(num_elev) + card_value(player_cards[0]))
  else:
    player_tot += card_value(player_cards[0]) + card_value(player_cards[1])

  print(f"Your hand sum is {player_tot}.\n")    # Informs hand sum, not necessary but extremely helpful

  hitting = input(f"Would you like to hit {pref}? (y/n)\n")   # Gives uer freedom to hit besides on 21
  hit_pos = 1
  while(hitting == "y" and player_tot < 21):
    hit_pos += 1
    player_cards.append(deck.pop())
    time.sleep(1)                   # Desired wait time
    print(f"Your new card is {player_cards[hit_pos]} {pref}.\n")
    time.sleep(1)
    if(player_cards[hit_pos] == "A"):   # Again gives user freedom to pick ace value
      num_elev = int(input(f"Would you like your ace to be an eleven or one {pref}? (11 or 1)\n"))
      player_tot += num_elev
    else:
      player_tot += card_value(player_cards[hit_pos])
    if(player_tot > 21):
      print(f"You have busted and therefore lost {pref}.\n")
      play_again(pref)
    print(f"Your new hand sum is {player_tot}.\n")
    if(player_tot != 21):
      hitting = input(f"Would you like to hit again {pref} (y/n)?\n")
  
  print("Okay it's my turn now.\n")
  if({dealer_cards[0][0]} == "A" and {dealer_cards[1][0]} == "A"):
    dealer_tot = 12                             # This is most optimal in gambling
  elif(dealer_cards[0][0] == "A"):
    dealer_tot = 11 + card_value(dealer_cards[1])
  elif(dealer_cards[1][0] == "A"):
    dealer_tot = 11 + card_value(dealer_cards[0])
  else:
    dealer_tot = card_value(dealer_cards[0]) + card_value(dealer_cards[1])
  print(f"I have a {dealer_cards[0]} and a {dealer_cards[1]}. Which means I have a current score of {dealer_tot}.\n")

  dealer_hit_pos = 1
  while dealer_tot < 17:        # Assuming we're playing hard 17
    dealer_hit_pos += 1
    dealer_cards.append(deck.pop())
    print(f"My next card is {dealer_cards[dealer_hit_pos][0]}.\n")
    if dealer_cards[dealer_hit_pos][0] == "A":
      dealer_tot += 1
    else:
      dealer_tot += card_value(dealer_cards[dealer_hit_pos])
    print(f"My current hand value is {dealer_tot}.\n")
    if dealer_tot > 21:
      print("Ah, I have busted. You win!\n")
      play_again(pref) 

  if(dealer_tot > player_tot):
    print("I have a larger sum! You lose!\n")
    play_again(pref)
  elif(dealer_tot < player_tot):
    print("You have a larger sum! You win!\n")
    play_again(pref)
  else:
    print("We tied! No one wins.\n")
    play_again(pref)

      
if __name__ == "__main__":
  main()