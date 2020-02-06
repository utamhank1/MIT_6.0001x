# Problem Set 2, hangman.py
# Name: Ujjwal Tamhankar
# Collaborators: None
# Time spent: ~28 hrs

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import sys

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # Initialize a list holding booleans for whether each letter in secret_word has been guessed
    # or not. Later on we update this list based on if letters_guessed are in secret word.
    is_a_match = [False] * len(secret_word)

    # Initilize a for loop that iterates from 0 to length of secret_word. Inside, initialize a 
    # Nested for loop with the goal of comparing every letter in secret_word to ever letter of 
    # letters_guessed.
    for index in range(0, len(secret_word)):

        # Nested for loop that iterates over the length of the list letters_guessed, which are the
        # letters that the user has guessed.
        for index2 in range(0, len(letters_guessed)):

            # If statement to determine if the letter in secret_word matches the letter in 
            # letters_guessed.
            if secret_word[index] == letters_guessed[index2]:
                # If the letter does match, update the is_a_match boolean list for that index to say
                # 'True' to indicate that a match has been found for that letter and break the 
                # inner loop.
                is_a_match[index] = (True)
                break
            
            # If the letter in letters_guessed for that particular index of secret_word does not 
            # find a match, continue the loop to check the letters until a match is found.
            elif secret_word[index] != letters_guessed[index2]:
                continue

            # If a match is not found, exit the inner loop and set the is_a_match value for that 
            # index of secret_word to False.     
            else:
                is_a_match[index] = (False)

    # After both nested loops run, analyze the is_a_match matrix to see if all of the values within
    # it are True, if so, return True, if there is even one False value, that means the word has 
    # not been guessed yet so return False.                        
    return all(is_a_match)

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # Create an empty list with '_ ' entries that is the length of secret_word.
    guessed_word = ['_ '] * len(secret_word)

    # Initialize a list holding booleans for whether each letter in secret_word has been guessed
    # or not. Later on we update this list based on if letters_guessed are in secret word. 
    is_a_match = [False] * len(secret_word)
    
    # Initilize a for loop that iterates from 0 to length of secret_word. Inside, initialize a 
    # Nested for loop with the goal of comparing every letter in secret_word to ever letter of 
    # letters_guessed.
    for index in range(0, len(secret_word)):

        # Nested for loop that iterates over the length of the list letters_guessed, which are the
        # letters that the user has guessed.
        for index2 in range(0, len(letters_guessed)):

            # If statement to determine if the letter in secret_word matches the letter in 
            # letters_guessed.
            if secret_word[index]==letters_guessed[index2]:
                is_a_match[index] = (True)

                # Set the '_ ' list value within guessed_word to the value of the letter that was 
                # guessed that matches a letter in secret_word. 
                guessed_word[index] = letters_guessed[index2]
            
            # If the letter in letters_guessed for that particular index of secret_word does not 
            # find a match, continue the loop to check the letters until a match is found.
            elif secret_word[index]!=letters_guessed[index2]:
                continue
            
            # If a match is not found, exit the inner loop and set the is_a_match value for that 
            # index of secret_word to False. 
            else:
                is_a_match[index] = (False)

    # Remove the spaces between the letters and underdashes in guessed_word and return that joined
    # guessed_word.            
    return ''.join(guessed_word)

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # Create a list of all of the possible lowercase letters. 
    letters = string.ascii_lowercase
    # Create an empty list of letters remaining.
    letters_remaining = []
    # Iterate of the list of all lowercase letters and if a is not detected, append that 
    # particular letter to the list of letters_remaining.
    for i in range(0, len(letters)):
        if not letters[i] in letters_guessed:
            letters_remaining.append(letters[i])
    # Return a string of all of the letters remaining.
    return ''.join(letters_remaining)
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Create a variable that holds the number of unique letters in the secret_word.
    num_unique_letters = len(set(secret_word))

    # Print welcome messages at game initialization.
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')

    # Create a variable to hold the amount of guesses available to the player.
    guesses = 6

    # Initialize an empty list to hold the letters that the user guesses.
    letters_guessed = []

    # Initialize a variable to hold the amount of 'Warnings' available to the user.
    warnings = 3;

    # Create a string to hold all of the available vowels.
    vowels = 'aeiou'

    # This "while loop" terminates when the user guesses enough letters to complete the word and/or 
    # the user runs out of guesses.
    while is_word_guessed(secret_word, letters_guessed) == False and guesses > 0:

        # Print new line to separate instances of user guesses and warnings.
        print('------------')

        # Boolean variable telling you if the guess that the user made is a valid guess that is in 
        # the alphabet.
        guess_in_alphabet = False
        
        # Print statement that indicates to the user how many guesses they have left before they 
        # make their guess.
        print(f'You have {guesses} guesses left.')

        # Create a 'state variable' that holds the length of the letters_guessed list from the last 
        # iteration before the user makes another guess.
        available_letters = get_available_letters(letters_guessed)
        number_prev_avail_letters = len(available_letters)

        # Print the number of available letters of the alphabet to guess.
        print('Available letters:', available_letters)
        
        # If the user has guesses available, prompt them to guess a letter and convert that letter 
        # to a lowercase letter. If the user is out of guesses, print that.    
        if guesses > 0:
            user_guess = input('Please guess a letter: ')
            user_guess = user_guess.lower()
        else: 
            print('Out of Guesses')
        
        # Check for if the guess that the user guessed is a valid character in the alphabet by 
        # comparing it to string.ascii_lowercase
        if len(user_guess) > 0:
            guess_in_alphabet = user_guess[0] in string.ascii_lowercase
        else:
            pass
            

        # Once the user guess has been determined to be in the alphabet, execute the following 
        # logic.        
        if guess_in_alphabet:

            # Add the user's guess to the list of all letters guessed.
            letters_guessed.append(user_guess)

            # Retrieve the guessed word using the list of letters guessed.
            get_guessed_word(secret_word, letters_guessed)

            # If the user's guess matched a new letter in the word, execute the following logic.
            if len(get_available_letters(letters_guessed)) < number_prev_avail_letters:
                
                # Retrieve the guessed word and store it as testString to test loop logic against.  
                testString = get_guessed_word(secret_word, letters_guessed)

                # Initialize default value for match_found indicating if the user's guess matches
                # a letter in the secret word.
                match_found = False

                # Initialize default value for vowel_match_found which is the boolean indicator 
                # that tells you whether the letter the user guessed is a vowel.
                vowel_match_found = False

                # Iterate over the testString aka guessed_word and determine if the letter the user
                # guessed matches any letters in the guessed_word. 
                for index in range(len(testString)):

                    # If the user guess matches a letter in the guessed_word. Set the match_found 
                    # boolean to True.
                    if user_guess == testString[index]:
                        match_found = True

                # Check to see if the user guess is a vowel by iterating over the vowel string and 
                # looking for matches.
                for index in range(len(vowels)):
                    if user_guess == vowels[index]:

                        # If a match is found, set the value of vowel_match_founc to True.
                        vowel_match_found = True
                
                # If the user guess matches a value in secret_word, print out a statement 
                # indicating so and update the value of get_guessed word.            
                if match_found:
                    print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
                
                # If the user guess does not match any of the letters in secret_word, indicate so 
                # and subtract the appropriate amount of guesses based on whether or not the guess 
                # was a vowel or a consonant.
                else:
                    print('Oops! That letter is not in my word: ', 
                          get_guessed_word(secret_word, letters_guessed))
                    
                    # If the wrong guess was a vowel, subtract two guesses.
                    if vowel_match_found:
                        guesses -= 2
                    
                    # If the vowel guess was a consonant, subtract one guess.
                    else: 
                        guesses -= 1
            
            # Check if the letter the user guessed is a letter that was guessed already by 
            # comparing it to the list of previously available letters. If the output of 
            # get_available_letters is the same as the number of previously available letters,
            # assume that the user made a double guess and subtract a warning.
            elif warnings > 0 and len(get_available_letters(letters_guessed)) == number_prev_avail_letters:
                warnings -= 1
                print(f'Oops! You already guessed that letter. You now have {warnings} warnings: ',
                      get_guessed_word(secret_word, letters_guessed) )
            elif warnings <= 0 and len(get_available_letters(letters_guessed)) == number_prev_avail_letters:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You now have no warnings '
                       'left so you lose one guess', get_guessed_word(secret_word, letters_guessed))
            else:
                pass

        # This block gives the code to run in case the user does not enter a valid letter in the 
        # 26 letter alphabet        
        else: 
            if warnings > 0:
                warnings -= 1
                print(f'Oops! That is not a valid letter. You now have {warnings} warnings: ')
            
            else:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You now have no warnings '
                       'left so you lose one guess', get_guessed_word(secret_word, letters_guessed))

    # If the user guesses every letter in the secret_word within the number of guesses, print out 
    # messages indicating a victory along with the calculation of the score.
    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!')
        print('Your total score for this game is: ', guesses * num_unique_letters)
    
    # If the user runs out of guesses before guessing the word, indicate so and print the 
    # secret_word.
    else:
        print('------------')
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.' )
        
    
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    ''' 
    This function takes in two words to compare, my_word and other_word. my_word is an instance of
    a guessed word which may have '_ ''s to indicate a letter that is not yet guessed. other_word is
    a normal english word. This function outputs True if all of the guessed letters (non '_') match 
    the letters of other_word. Returns False if the two words are different lengths or if a guessed
    letter in my_word does not match the cooresponding character in other_word.
    '''
    # Condense my_word by removing all spaces between the '_ ''s.
    my_word = my_word.replace(' ', '')

    # Create a string of all of the unique letters in my_word and remove all of the spaces.
    unique_letters = ''.join(set(my_word))

    # Remove the underscores in the string of all unique letters of my_word. 
    unique_letters = unique_letters.replace('_','')
    
    # Initialize a list holding booleans for whether each letter in secret_word has been guessed
    # or not. Later on we update this list based on if letters_guessed are in secret word.
    is_a_match = [False] * len(my_word)

    # Check to see if the two words being compared match in length.    
    if len(my_word) == len(other_word):

        # Iterate over the length of my_word and determine inf letters match.
        for index in range(len(my_word)):

            # Check if there is an underscore in the index position of my_word in question and 
            # execute the following logic.
            if my_word[index] == '_':

                # check if that underscore is supposed to be a unique letter of other_word by 
                # iterating over the unique letters in my_word and checking the cooresponding index
                # of other_word.
                for i in range (len(unique_letters)):

                    # If the there is a unique letter of my_word in the cooresponding index of 
                    # other_word, set the is_a_match index of that current position to False and 
                    # break the loop (this may seem counterintuitive to the purpose of is_a_match
                    # but in this context it makes sense because we are trying to avoid
                    # that when a letter is guessed, your code reveals all the positions at which
                    # that letter occurs in the secret word. Therefore, the hidden letter (_ ) 
                    # cannot be one of the letters in the word that has already been revealed.)
                    if other_word[index] == unique_letters[i]:
                        is_a_match[index] = False
                        return False

                    # If the above is not the case, set the is_a_match for that index to True.
                    else: 
                        is_a_match[index] = True
             
            # Check to see if a non-underscore index in other_word matches that of my_word. If
            # it does, set the is_a_match value for that index to True, else, set it to False.    
            elif my_word[index] == other_word[index]:
                is_a_match[index] = True
            else:
                is_a_match[index] = False
                return False
        
        # Check to see if all of the entries in the boolean is_a_match list are True, if so, return
        # True, if not, return False.
        return all(is_a_match)
    
    # Return False if my_word and other_word don't match in length        
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # Initialize an empty matrix of matches to populate with matches once they are found.
    matches = []

    # Iterate over the wordlist to look at every word and see if its a match with my_word.
    for word in wordlist:

        # Call the match_with_gaps function on my_word and the particular word in word_list,
        # if the function call returns True, add that word in wordlist the matches[] list.
        if match_with_gaps(my_word, word) == True:
            matches.append(word)
        else:
            pass
    
    # If after iterating through the entire wordlist no matches are found, print a statement 
    # saying so. Else, print the list of matches.
    if matches == []:
        print('No matches found')
    else:
        print(matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Create a variable that holds the number of unique letters in the secret_word. This variable 
    # will be very important later.
    num_unique_letters = len(''.join(set(secret_word)))

    # Print welcome messages at game initialization.
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    
    # Create a variable to hold the amount of guesses available to the player.
    guesses = 6

    # Initialize an empty list to hold the letters that the user guesses.
    letters_guessed = []

    # Initialize a variable to hold the amount of 'Warnings' available to the user.
    warnings = 3;

    # Create a string to hold all of the available vowels.
    vowels = 'aeiou'
    
    # While loop that terminates when the user guesses enough letters to complete the word and/or 
    # the user runs out of guesses.
    while is_word_guessed(secret_word, letters_guessed) == False and guesses > 0:
        
        # Print new line to separate instances of user guesses and warnings.
        print('------------')
        
        # Boolean variable telling you if the guess that the user made is a valid guess that is in 
        # the alphabet.
        guess_in_alphabet = False
        
        # Print statement that indicates to the user how many guesses they have left before they 
        # make their guess.
        print(f'You have {guesses} guesses left.')
        
        # Create a 'state variable' that holds the length of the letters_guessed list from the last 
        # iteration before the user makes another guess.
        letters_available = get_available_letters(letters_guessed)
        number_prev_avail_letters = len(letters_available)

        # Print the available letters of the alphabet to guess.
        print('Available letters:', letters_available)
        
        # If the user has guesses available, prompt them to guess a letter and convert that letter 
        # to a lowercase letter. If the user is out of guesses, print that.    
        if guesses > 0:
            user_guess = input('Please guess a letter: ')
            user_guess = user_guess.lower()
            
            # Special input case if the user enters '*', this forces the guess_in_alphabet boolean
            # to be set to True so as to not prompt an invalid character reaction from the program.
            # This action by the user also calles the show_possible_matches function to show 
            # possible matching words from the word_list.
            if user_guess == '*':
                guess_in_alphabet = True
                if len(letters_guessed) == 0:
                    print('Guess a letter first!')
                else:
                    show_possible_matches(get_guessed_word(secret_word, letters_guessed))

        else: 
            print('Out of Guesses')
        
        # Check for if the guess that the user guessed is a valid character in the alphabet by 
        # comparing it to string.ascii_lowercase
        if len(user_guess) > 0 and user_guess != '*':
            guess_in_alphabet = user_guess[0] in string.ascii_lowercase
        else:
            pass

        # Once the user guess has been determined to be in the alphabet, execute the following 
        # logic.
        if guess_in_alphabet:

            # Add the user's guess to the list of all letters guessed.
            letters_guessed.append(user_guess)

            # Retrieve the guessed word using the list of letters guessed.
            get_guessed_word(secret_word, letters_guessed)

            # If the user's guess matched a new letter in the word, execute the following logic.
            if len(get_available_letters(letters_guessed)) < number_prev_avail_letters:
                
                # Retrieve the guessed word and store it as testString to test loop logic against.  
                testString = get_guessed_word(secret_word, letters_guessed)

                # Initialize default value for match_found indicating if the user's guess matches
                # a letter in the secret word.
                match_found = False

                # Initialize default value for vowel_match_found which is the boolean indicator 
                # that tells you whether the letter the user guessed is a vowel.
                vowel_match_found = False

                # Iterate over the testString aka guessed_word and determine if the letter the user
                # guessed matches any letters in the guessed_word. 
                for index in range(len(testString)):

                    # If the user guess matches a letter in the guessed_word. Set the match_found 
                    # boolean to True.
                    if user_guess == testString[index]:
                        match_found = True

                # Check to see if the user guess is a vowel by iterating over the vowel string and 
                # looking for matches.
                for index in range(len(vowels)):
                    if user_guess == vowels[index]:

                        # If a match is found, set the value of vowel_match_founc to True.
                        vowel_match_found = True
                
                # If the user guess matches a value in secret_word, print out a statement 
                # indicating so and update the value of get_guessed word.            
                if match_found:
                    print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
                
                # If the user guess does not match any of the letters in secret_word, indicate so 
                # and subtract the appropriate amount of guesses based on whether or not the guess 
                # was a vowel or a consonant.
                else:
                    print('Oops! That letter is not in my word: ', 
                          get_guessed_word(secret_word, letters_guessed))
                    
                    # If the wrong guess was a vowel, subtract two guesses.
                    if vowel_match_found:
                        guesses -= 2
                    
                    # If the vowel guess was a consonant, subtract one guess.
                    else: 
                        guesses -= 1
            
            # Check if the letter the user guessed is a letter that was guessed already by 
            # comparing it to the list of previously available letters. If the output of 
            # get_available_letters is the same as the number of previously available letters,
            # assume that the user made a double guess and subtract a warning.
            elif warnings > 0 and len(get_available_letters(letters_guessed)) == number_prev_avail_letters and user_guess != '*':
                warnings -= 1
                print(f'Oops! You already guessed that letter. You now have {warnings} warnings: ',
                      get_guessed_word(secret_word, letters_guessed) )
            elif warnings <= 0 and len(get_available_letters(letters_guessed)) == number_prev_avail_letters:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You now have no warnings '
                       'left so you lose one guess', get_guessed_word(secret_word, letters_guessed))
            else:
                pass
        # This block gives the code to run in case the user does not enter a valid letter in the 
        # 26 letter alphabet        
        else:
            if warnings > 0:
                    warnings -= 1
                    print(f'Oops! That is not a valid letter. You now have {warnings} warnings: ')
                # If the user has between 1 and 3 warnings, subtract a warning and indiacte so, continue
                # the loop. 
            else:
                guesses -= 1
                print(f'Oops! That is not a valid letter. You now have no warnings '
                       'left so you lose one guess', get_guessed_word(secret_word, letters_guessed))

                

    # If the user guesses every letter in the secret_word within the number of guesses, print out 
    # messages indicating a victory along with the calculation of the score.
    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!')
        print('Your total score for this game is: ', guesses * num_unique_letters)
    
    # If the user runs out of guesses before guessing the word, indicate so and print the 
    # secret_word.
    else:
        print('------------')
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.' )



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    
    if len(sys.argv) == 1: 
        secret_word = choose_word(wordlist)
        hangman(secret_word)
    
    else: 
        secret_word = choose_word(wordlist)
        hangman_with_hints(secret_word)
