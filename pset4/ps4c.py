# Problem Set 4C
# Name: Ujjwal Tamhankar
# Collaborators: None
# Time Spent: a while (long time, not a while loop)
import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...");
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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

# Create a helper function that helps determine the key in a dictionary that has the maximum value
# associated with it. This function takes in a input dictionary and outputs the key-value pair that
# cooresponds to the maximum value and the associated key.
def maximum_keys(dic):
    maximum = max(dic.values())
    keys = filter(lambda x:dic[x] == maximum,dic.keys())
    return keys,maximum

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
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
        words = self.valid_words
        return words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # Initialize lists and variables holding the permutations of upper and lowercase letters 
        # that are passed into the function.
        vowels_permutation_upper = vowels_permutation.upper()
        vowels_permutations_list_lowercase = list(vowels_permutation)
        vowels_permutations_list_uppercase = list(vowels_permutation_upper)
        vowels_lowercase = list(VOWELS_LOWER)
        vowels_uppercase = list(VOWELS_UPPER)

        # Initialize empty dictionaries that will hold the permuted dictionaries of the vowels.
        uppercase_vowels_dict = {}
        lowercase_vowels_dict = {}

        # Iterate through the lowercase vowels and create dictionaries remaping the upper and lower
        # case vowels by the permutation that is passed in.
        for i, j, k, l in zip(vowels_lowercase, range(0, len(vowels_permutations_list_lowercase)),
            vowels_uppercase, range(0, len(vowels_permutations_list_uppercase)) ):
            lowercase_vowels_dict[i] = vowels_permutations_list_lowercase[j]
            uppercase_vowels_dict[k] = vowels_permutations_list_uppercase[l]

        # Combine the permuted dictionaries of the lowercase and uppercase vowels into one 
        # dictionary.
        permuted_dict = {**lowercase_vowels_dict, **uppercase_vowels_dict}    

        return permuted_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        # Getter method for the message text. Split message into words and initialize empty
        # list for the letters of the encrypted word.
        text = self.get_message_text()
        words = text.split()
        enc_word = []

        # Iterate over the length of "words" and compare the letters of "words" to the appropriate
        # key within transpose_dict. Replace that letter with the appropriate letter value in trans
        # pose_dict
        for k in range(0, len(words)):
            new_word = list(words[k])
            for i in range(0, len(words[k])):
                if words[k][i] in transpose_dict.keys():
                    new_word[i] = transpose_dict[words[k][i]]
            ''.join(new_word)
            enc_word.append(new_word)
        output_string = ''

        # Output the encrypted word by joining the elements in the list with a space.
        for element in enc_word:
            output_string +=' '+''.join(element)
        return output_string


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        # Load the list of all available words and use the function from part A to generate an array
        # of all of the possible permutations of the string 'aeiou'
        wordlist = load_words(WORDLIST_FILENAME)
        permutation_list = get_permutations('aeiou')

        # Initialize list of zeros that will be filled with the number of valid words that are 
        # generated by decrypting the encrypted word with a transpose_dict created from a 
        # particular instance of an 'aeiou' permutation. 
        number_real_words = [0] * len(permutation_list)

        # Initialize an empty dict to hold the 
        # permutation - real word value pairs.
        best_valid_word_permuters = {}

        # Iterate over the length of the permuation list and build transpose dictionaries according
        # to that permutation.
        for permutation, k in zip(permutation_list, range(0, len(permutation_list))):
            transpose_dict = SubMessage.build_transpose_dict(self, permutation)
            decrypted_text = SubMessage.apply_transpose(self, transpose_dict).split()
            word_counter = 0

            # Test that permutation dictionary decryption be looking at how many real words the 
            # decrypted test consists of. Save that value in number_real_words[k]
            for j in decrypted_text:
                if is_word(wordlist, j):
                    word_counter += 1
                    number_real_words[k] = (word_counter)
        
        # Create a dictionary to hold the permutation and the number of real words generated from 
        # the decryption generated from the dictionary created from that permutation.    
        for key, real_word_count in zip(permutation_list, number_real_words):
            best_valid_word_permuters[key] = real_word_count
        
        # Get the maximum key-value pair (if any) and return the word associated with it.
        maximum = maximum_keys(best_valid_word_permuters)
        
        # If no maximum is found, return the original text.
        if maximum[1] == 0:
            return SubMessage.get_message_text(self)
        else:
            # If a maximum is found, return the best transcribed message.
            decryption_dict = SubMessage.build_transpose_dict(self, ''.join(list(maximum[0])[0]))
            return SubMessage.apply_transpose(self, decryption_dict)


if __name__ == '__main__':

    #TODO: WRITE YOUR TEST CASES HERE
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    print('--------------------------------------------')
    message = SubMessage("Hello World!")
    permutation = "aeiou"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hello World!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    print('--------------------------------------------')
    message = SubMessage("Jacob's Ladder")
    permutation = "aieou"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Jacob's Laddir!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    print('--------------------------------------------')
    message = EncryptedSubMessage("Jacob's Laddir!")
    print('Original encrypted message', message.get_message_text())
    print('Expected Decrypted Message: Jacob\'s Ladder!')
    dec_message = message.decrypt_message()
    print('Actual Decrypted Message:', dec_message)
    
    print('--------------------------------------------')
    message = EncryptedSubMessage("intorost ruto")
    print('Original encrypted message', message.get_message_text())
    print('Expected Decrypted Message: interest rate or interest rote')
    dec_message = message.decrypt_message()
    print('Actual Decrypted Message:', dec_message)