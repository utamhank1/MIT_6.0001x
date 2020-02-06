# Problem Set 4B
# Name: Ujjwal Tamhankar
# Collaborators: None
# Time Spent: ~10hrs

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# Create a helper function that helps determine the key in a dictionary that has the maximum value
# associated with it. This function takes in a input dictionary and outputs the key-value pair that
# cooresponds to the maximum value and the associated key.
def maximum_keys(dic):
    maximum = max(dic.values())
    keys = filter(lambda x:dic[x] == maximum,dic.keys())
    return keys,maximum

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        ''' 
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text 

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words
        return valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        # Create strings of uppercase and lowercase letters.
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase

        # Create lists of the upper and lowercase characters and extend them.
        keys_lowercase = list(lowercase_letters)
        keys_uppercase = list(uppercase_letters)

        # Lists are extended to account for edge cases, when we shift the letters. (Don't want the
        # lists of the letters to go out of bounds.)
        keys_lowercase_extended = 3 * list(lowercase_letters)
        keys_uppercase_extended = 3 * list(uppercase_letters) 

        # Initialize empty dictionaries to hold values.
        lowercase_dict = {}
        uppercase_dict = {}

        # Loop that maps the "shift" between letter keys and builds two dictionaries the represent 
        # the letter shift.
        for i,j,k,l in zip(keys_lowercase, range(0, len(keys_lowercase_extended)), 
            keys_uppercase,range(0, len(keys_uppercase_extended)) ):
            lowercase_dict[i] = keys_lowercase_extended[j+shift]
            uppercase_dict[k] = keys_uppercase_extended[l+shift]

        # Append the lowercase shift dict and the uppercase shift dict together.
        complete_dict = {**lowercase_dict, **uppercase_dict}
        return complete_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        # Get the original message text using the getter() method.
        text = self.get_message_text()
        
        # Turn the text file into a list for mutability reasons.
        encrypted_word = list(text)

        # Call the build_shift_dict method and store the shifted dictionary variable in 
        # complete_dict.
        complete_dict = self.build_shift_dict(shift)

        # Iterate over the text file and if the letter in question is not a special character or 
        # space, replace it with the appropriately mapped key value from complete_dict. 
        for i,j in zip(text, range(0, len(text))):
            if i == ' ' or i == ',' or i == '!' or i == '.' or i == '\'' or i == '(' or i == ')':
                pass
            else:
                encrypted_word[j] = complete_dict[i]
        
        # Join the list back into a string and return it.      
        return ''.join(encrypted_word)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict = self.encryption_dict
        return encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
    
class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        Message.__init__(self, text)
        shift = 0
        PlaintextMessage.__init__(self, text, shift)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # Load the wordlist from the folder that hs the list of all valid names.
        wordlist = load_words(WORDLIST_FILENAME)

        # s_values describes the list of all of the possible shift numbers (numbers 1 through 26 
        # of the alphabet)
        s_values = list(range(0,26))

        # A list initialized to eventually hold the word counts of all of the real words that can 
        # be generated by the associated shift number on the reference dictionary.
        number_real_words = list(range(0,26))
        
        # Initiate an empty dictionary, that will eventually hold the values of each shift number 
        # 1 - 26 and the associated number of correct words generated when the dictionary generated 
        # with that shift number is used to decrypt the message. 
        best_valid_word_decrypter = {}

        # Getter method for the encrypted message.
        encrypted_text = PlaintextMessage.get_message_text_encrypted(self)

        # Iterate of the values of the alphabet and determine a alphabet shift array.
        for s in s_values:

            # For every iteration of the look change the dictionary shift number.
            PlaintextMessage.change_shift(self, 26-s)

            # Create separate arrays of each word returned from get_message_text_encrypted()
            split_words = PlaintextMessage.get_message_text_encrypted(self).split()
            
            # Initialize the word counter to zero. This variable holds the amount of real words 
            # detected with every iteration of the shift dictionary.
            word_counter = 0
            
            # Analyze how many real words are generated by that iteration of the text mapping 
            # generated by that shifted dictionary.
            for j in split_words:
                if is_word(wordlist, j):
                    word_counter += 1
            number_real_words[s] = word_counter

        # Store the number of valid words discovered per iteration of the shift number and store it
        # as key values in dict best_valid_word_decrypter()
        for key, real_word_count in zip(s_values, number_real_words):
            best_valid_word_decrypter[key] = real_word_count
        
        # Determine the maximum key-value pair in best_valid_word_decrypter that tells you the 
        # optimum shift value (key) that results in the maximum number of real words decrypted 
        # (value).
        maximum = maximum_keys(best_valid_word_decrypter)
        
        # Convert the maximum key-value pair into a tuple that returns the data in the appropriate 
        # format.
        a = list(maximum[0])[0];
        PlaintextMessage.change_shift(self, 26-a)   
        outputTuple = (a, PlaintextMessage.get_message_text_encrypted(self))
        return outputTuple
            

if __name__ == '__main__':


    #TODO: WRITE YOUR TEST CASES HERE
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    plaintext = PlaintextMessage('Hello, World!', 4)
    print('Expected Output: Lipps, Asvph!')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'), 'or', (2, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    ciphertext = CiphertextMessage('Lipps, Asvph!')
    print('Expected Output:', (4, 'Hello, World!'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: best shift value and unencrypted story 
    story = get_story_string()
    ciphered_story = CiphertextMessage(story)
    ciphered_story.decrypt_message()
