# Problem Set 4A
# Name: Ujjwal Tamhankar
# Collaborators: none
# Time Spent: ~ 5hrs

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Base case, if the sequence length = 1, return that value.
    if len(sequence) == 1:
        return[sequence]
    # If the sequence length is greater than 1, enumerate the sequence and iterate over each piece.
    # call the get_permutations() on each piece and iteratively compose the 'permutations' list.
    # return the final permuations list.
    else:
        permutations = []
        for i, counter in enumerate(sequence):
            for j in get_permutations(sequence[:i] + sequence[i + 1:]):
                permutations = permutations + [counter + j]
            
        return permutations
            

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # Test case 1:
    sequence = 'a'
    output = get_permutations(sequence)
    expected_output = ['a']
    print(f'Input = {sequence}, Output = {output} ')
    print(f'Expected Output: {expected_output}')
    if output == expected_output:
        print('\nSingle Letter Permutation Test Passed!\n')
    else: 
        print('\nSingle Letter Permutation Test Failed!')

    # Test case 2:
    sequence = 'ab'
    output = get_permutations(sequence)
    expected_output = ['ab', 'ba']
    print(f'Input = {sequence}, Output = {output} ')
    print(f'Expected Output: {expected_output}')
    if output == expected_output:
        print('\nDouble Letter Permutation Test Passed!\n')
    else: 
        print('\nDouble Letter Permutation Test Failed!\n')

    # Test case 3:
    sequence = '123'
    output = get_permutations(sequence)
    expected_output = ['123', '132', '213', '231', '312', '321']
    print(f'Input = {sequence}, Output = {output} ')
    print(f'Expected Output: {expected_output}')
    if output == expected_output:
        print('\nTriple Number Permutation Test Passed!\n')
    else: 
        print('\nTriple Number Permutation Test Failed!\n')