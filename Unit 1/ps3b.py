from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    perm_list = []
    for n in range(1, HAND_SIZE+1):
        temp_list = get_perms(hand, n)
        perm_list.extend(temp_list)

    perm_list.sort(key=len, reverse = True)
    for word in perm_list:
        if word in word_list:
            return word
    return "."
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    total_score = 0
    
    while(calculate_handlen(hand) > 0): 
        # Display hand
        print "Current Hand:", 
        display_hand(hand)
        word = comp_choose_word(hand, word_list)
        if word == '.':
            print "Computer couldn't find a word for current hand!"
            print display_score(total_score)
            return None
            
        if is_valid_word(word, hand, word_list):
            score = get_word_score(word, HAND_SIZE)
            total_score += score
            hand = update_hand(hand, word)
            print '"' + word + '" earned ' + str(score) + ' points. ', display_score(total_score)
        else:
            print "Invalid word, please try again." 
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hand = deal_hand(HAND_SIZE)
    while(True):
        choice = raw_input("Enter 'n' for new game, 'r' to restart last game or 'e' to exit: ")
        if choice == 'e':
            break
        player = raw_input("Enter 'u' for user and 'c' for computer player: ")
        if player == 'u':
            if choice == 'n':
                hand = deal_hand(HAND_SIZE)
                play_hand(hand, word_list)
            if choice == 'r':
                play_hand(hand, word_list)
        if player == 'c':
            if choice == 'n':
                hand = deal_hand(HAND_SIZE)
                comp_play_hand(hand, word_list)
            if choice == 'r':
                comp_play_hand(hand, word_list)

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
