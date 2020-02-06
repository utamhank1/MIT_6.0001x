

# Import necessary libraries 
import math

def main():

    # Obtain user inputs for values of x and y and parse to appropriate type.
    x = float(input('Enter number x: '))
    y = float(input('Enter number y: '))
    
    # Calculate x to the y power.
    x_to_the_y = x**y

    # Calculate the log base 2 of x.
    log_base_2_x = math.log(x, 2)
    
    # Print the results of both calculations.
    print(f'X**y = {x_to_the_y}')
    print(f'log(x) = {log_base_2_x}')
    
if __name__ == '__main__':
    main()





