# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

# Added a scrabble letter value of '0' for the '*' as as entering this value is not supposed 
# to impact scoring. -U.T 11/15/19
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
    

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.
    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 
    The score for a word is the product of two components:
    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.
    word: string
    n: int >= 0
    returns: int >= 0
    """
    # Validate the word input to make sure that it is lowercase. -U.T 11/15/19
    word_lowercase = str.lower(word)
    word_length = len(word_lowercase)
    letter_score = []
    
    # Calculate the score based on refering to the scoring dictionary SCRABBLE_LETTER_VALUES, length
    # of the word and how many letters are remaining. -U.T 11/15/19
    if word_length > 0:
        words_separated = list(word_lowercase)
        for i in range(0, len(words_separated)):
            letter_score.append(SCRABBLE_LETTER_VALUES[words_separated[i]])
        score = sum(letter_score) * max(1, 7*word_length - 3*(n - word_length))
    else:
        score = 0
    
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.
    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.
    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.
    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    # This loop calculates values that will be in the user's hand when the hand is dealt.
    # Makes sure there are a certain number of vowels, consonants, and one '*'. -U.T 11/15/19
   
    for i in range(num_vowels):
        if i == num_vowels - 1 :
            x = '*'
            hand[x] = hand.get(x, 0) + 1
        else:    
            x = random.choice(VOWELS)
            hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    Has no side effects: does not modify hand.
    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # Create a copy of the hand since we DON'T want to modify the user's actual hand. -U.T 11/15/19
    hand_copy = hand.copy()
    random_word = word
    # Make sure the word entered is lowercase -U.T 11/15/19
    lower_random_word = str.lower(random_word)

    # Check if any letters in the word the user guessed match the letters in the hand, if so,
    # subtract 1 from that particular letter in the copy of the user's hand. Return the hand once 
    # all letters have been checked and subtracted. -U.T 11/15/19
    frequencies_random = get_frequency_dict(lower_random_word)
    for i in range (0, len(lower_random_word)):
        for letter2 in hand.keys():
            if lower_random_word[i] == letter2:
                hand_copy[lower_random_word[i]] = hand_copy[letter2] - 1
                if hand_copy[lower_random_word[i]] == 0:
                    del hand_copy[lower_random_word[i]]
                else:
                    continue
            else:
                continue
    return hand_copy

def update_hand_negatives(hand, word):
    """
    Similar to update_hand expect it returns a hand with possible negative values for 
    letter items based on what is used to create the word instead of simply removing 
    the letter key from the list.
    Has no side effects: does not modify hand.
    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_copy = hand.copy()
    random_word = word
    lower_random_word = str.lower(random_word)

    # Same nested for loop as in update_hand() but allows dictionary values for certain items to
    # go negative if the word uses more letters than are available in the hand. -U.T 11/15/19
    frequencies_random = get_frequency_dict(lower_random_word)
    for i in range (0, len(lower_random_word)):
        for letter2 in hand.keys():
            if lower_random_word[i] == letter2:
                hand_copy[lower_random_word[i]] = hand_copy[letter2] - 1
            else:
                continue
    return hand_copy


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower()
    wordlist = word_list

    # Initialize certain booleans telling you validity status of the word the user entered 
    # (and if the word is in the wordlist). -U.T 11/15/19
    is_in_hand = False
    is_in_list = False
    letter_in_word_in_hand = [False] * len(word_lower)
    all_letters_in_word_hand = False
    is_valid_word = False

    # If the word entered contains a star, check and see if that '*' can be replaced by any vowel
    # and create a valid word. -U.T 11/15/19
    if '*' in word_lower:
        star_index = word.find('*')
        for i in range(len(VOWELS)):
            test_word = list(word_lower)
            # test_word is a possible word that is created when the '*' in the word entered is 
            # replaced by a vowel.- U.T 11/15/19
            test_word[star_index] = VOWELS[i]
            if str(''.join(test_word)) in wordlist:
                # If a word can be be formed, set the appropriate boolean indicator to True. 
                # -U.T 11/15/19
                is_valid_word = True
                break

    # If the word entered does not contain a '*' check and see if every letter in the word
    # is present in the hand. -U.T 11/15/19    
    else:
        for char in range(0,len(word_lower)):
            for letter in hand.keys():
                if word_lower[char] == letter:
                    letter_in_word_in_hand[char] = True
                    break
                else:
                    continue
        all_letters_in_word_hand = all(letter_in_word_in_hand)

        # Check and see if the word entered is present in the dictionary of all of the words.
        # -U.T 11/15/19
        for index in range (len(wordlist)):
            if wordlist[index] == word_lower:
                is_in_list = True
            else:
                continue

            # Check and see if the hand contains all of the letters needed to make the word in the
            # correct amounts by checking if the update_hand_negatives function will go negative.
            # -U.T 11/15/19
            hand = update_hand_negatives(hand, wordlist[index])
            for letter in hand.keys():
                if hand[letter] < 0:
                    return False
                    break
                else:
                    is_in_hand = True
        # Return whether or not all boolean criteria are satisfied for input validation. 
        # -U.T 11/15/19   
        is_valid_word = is_in_list and is_in_hand and all_letters_in_word_hand

    return is_valid_word


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    num_list = []
    for key in hand.keys():
        num_list.append(hand[key])
    
    return sum(num_list)

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:
    * The hand is displayed.
    
    * The user may input a word.
    * When any word is entered (valid or invalid), it uses up letters
      from the hand.
    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.
      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0
    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
    
        # Display the hand
        print('Current Hand: ', end = '')
        display_hand(hand)
        
        
        # Ask user for input
        word = str(input('Enter word, or \"!!\" to indicate that you are finished: '))
        
        # If the input is two exclamation points:
        if word == '!!':
        
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:

            # If the word is valid:
            if is_valid_word(word, hand, word_list):

                # Tell the user how many points the word earned,
                # and the updated total score
                score = get_word_score(word, calculate_handlen(hand))
                total_score = total_score + score
                print(f'\"{word}\" earned {score} points. Total: {total_score} points')

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('That is not a valid word. Please choose another word.')
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print(f'Ran out of letters. Total score: {total_score} points')

    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 
def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    If user provide a letter not in the hand, the hand should be the same.
    Has no side effects: does not mutate hand.
    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # Create certain variables that hold key information from code execution. -U.T 11/15/19
    hand_length = len(hand)

    # Hold the index of the letter needing to be replaced. -U.T 11/15/19
    number_letter = hand[letter]
    hand_copy = hand.copy()

    # Generate a random letter from the set of all lowercase letters. -U.T 11/15/19
    random_letter = random.choice(string.ascii_lowercase)
    letter_list = []
    
    # Create a list of letters that is already in the user's hand. -U.T 11/15/19
    for letter1 in hand.keys():
        for j in range(hand[letter1]):
            letter_list.append(letter1)
        letter_string = ''.join(letter_list)

    # Run this loop while the random letter generated is not a letter in the string of letters that 
    # is in the hand or if the random letter is not equal to the letter the user selected.
    # -U.T 11/15/19    
    while random_letter in letter_string or random_letter == letter:
        random_letter = random.choice(string.ascii_lowercase)
        letter_list = []
        for letter1 in hand.keys():
            for j in range(hand[letter1]):
                letter_list.append(letter1)
        letter_string = ''.join(letter_list)
    del hand_copy[letter]

    # Delete all instances of that letter the user selected from his/her hand. -U.T 11/15/19
    hand_copy.update({random_letter:number_letter})

    # Replace that letter with the validated random_letter in the hand. -U.T 11/15/19
    return hand_copy
    
def play_game(word_list):
    """
    Allow the user to play a series of hands
    * Asks the user to input a total number of hands
    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.
    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.
            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands
    word_list: list of lowercase strings
    """
    # Prompt user input and initialize the value of the score. -U.T 11/15/19
    num_hands = int(input('Enter total number of hands: '))
    total_score_all_hands = 0
    
    while num_hands > 0:
        # Initialize certain booleans for loop execution and display the user's current hand.
        # -U.T 11/15/19
        replay_hand = True
        hand = deal_hand(HAND_SIZE)
        print('Current Hand: ', end = '')
        display_hand(hand)
        choice_made = False
        decision_replay_hand = False

        # Prompt the user to substitute a letter. If the user says yes, substitute that letter
        # into the hand. -U.T 11/15/19
        while choice_made == False:
        
            substitute = str(input('Would you like to substitute a letter? '))
            if substitute.lower() == 'yes' or substitute.lower() == 'y':
                letter = str(input('Which letter would you like to replace: '))
                hand = substitute_hand(hand, letter)
                choice_made = True
            elif substitute.lower() == 'no' or substitute.lower() == 'n':
                break
            else:
                print('Please indicate \'yes\' or \'no\'')

        # Play hands if the user chooses to replay the hand. -U.T 11/15/19
        while replay_hand == True:
            hand_score = play_hand(hand, word_list)
            print(f'Total score for this hand: {hand_score}')
            decision_replay_hand = False
            print('----------')
            
            # Prompt the user to enter whether to replay the hand or not. If so, set the appropriate
            # boolean (replay_hand) to True and replay the hand. (DO NOT generate a new hand). 
            # -U.T 11/15/19
            while not decision_replay_hand: 
                replay_choice = str(input('Would you like to replay the hand? '))
                if replay_choice == 'yes' or replay_choice == 'y':
                    replay_hand = True
                    decision_replay_hand = True
                elif replay_choice == 'no' or replay_choice == 'n':
                    replay_hand = False
                    num_hands -= 1
                    total_score_all_hands = total_score_all_hands + hand_score
                    decision_replay_hand = True
                else:
                    print("Please indicate 'yes' or 'no'")
                    decision_replay_hand = False

    # Return the score of all of the hands played. -U.T 11/15/19
    return total_score_all_hands
    
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    total_score_all_hands = play_game(word_list)
    print('----------')
    # Print the user's score. -U.T 11/15/19
    print(f'Total score for all hands: {total_score_all_hands}')    