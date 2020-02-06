# Part C: Finding the right amount to save away

# Create a function that takes in the monthly salary and the percentage increase of the salary
# (rate) and return a new monthly salary that is reflection of the raise that was given.
def apply_raise(annual_salary, rate):
    annual_salary = annual_salary*(1+rate)
    return annual_salary

# This function takes in the user's current savings, monthly salary, a value for the portion that
# the user shuld save away (percentage), the number of months that you want to calculate the 
# savings after, the rate of increase given by the semi_annual_raise and the return on investment
# of the savings amount and returns the amount of savings.
def calc_current_savings(monthly_salary, portion_saved, month, semi_annual_raise, 
                         return_on_investment):
    
    # Run the current_savings 
    current_savings = 0
    for months in range(0, month + 1):
        
        # If the current value of months is a multiple of 6, apply a raise to the monthly salary.
        if (months % 6 == 1) and (months > 1):
            monthly_salary = apply_raise(monthly_salary,semi_annual_raise)
        
        # Calculate the current savings by adding the current savings and the portion of the 
        # monthly salary saved.
        current_savings = current_savings + monthly_salary*portion_saved
    
    # Calculate the final value of current savings by multiplying the current savings by the 
    # return_on_investment.
    current_savings = current_savings * (1+return_on_investment)
    
    # Return the value of the current savings.
    return current_savings

def main():
    # Wait for user input as to the user's annual salary.
    print('Enter your starting annual salary in dollars: ')
    annual_salary = float(input())

    # Set the value of the user's starting salary to the current annual salary.
    starting_salary = annual_salary
    
    # Set the value of the user's starting monthly salary.
    monthly_salary = starting_salary/12
    
    # Enter the total cost of the house in dollars.
    total_cost = 1000000.0
    
    # Percentage of the houses value that will be the downpayment.
    portion_down_payment = .25
    
    # Value for the semi annual raise that the user expects on his/her salary.
    semi_annual_raise = .07
    
    # Average return percentage on the current savings that the user has.
    return_on_investment = 0.04
    
    # User's current savings.
    current_savings = 0.0
    
    # High bound on the value that we want to 'guess' for the portion of his/her income that the 
    # user should save.
    high_bound = 10000
    
    # Low bound on the value that we want to 'guess' for the portion of his/her income that the 
    # user should save.
    low_bound = 0
    
    # Amount of downpayment that the house requires.
    down_payment = total_cost * portion_down_payment
    
    # Calculation of the 'guess' for the binary search method that we are using to figure out 
    # the ideal value for the portion that the user should save.
    midpoint_portion_saved = (high_bound+low_bound)/2
    
    # Set the portion saved value to the midpoint value to set up the binary search.
    portion_saved = midpoint_portion_saved
    
    # Set the tolerance value for "how close" our current savings as a result of the portion saved
    # value should get us to the actual value of the downpayment.
    tolerance = 100
    
    # Step counter to keep track of the number of times the binary search has to iterate to get
    # to the ideal value of portion_saved.
    steps = 0

    # Wait for user input as to amount of his/her starting salary.
    print(f'Enter the starting salary: {starting_salary}')
    
    # Set the condition for termination of the loop equal to when the current_savings value is 
    # within 100 dollars (tolerance) of the actual down_payment needed.  
    while abs(current_savings - down_payment) >= tolerance:
        
        # Calculate the current savings after 36 months based on the value for "portion saved"
        # that we guess and normalize.
        current_savings = calc_current_savings( monthly_salary = monthly_salary,
                                                portion_saved = (int(portion_saved)/10000), 
                                                month = 36, 
                                                semi_annual_raise = semi_annual_raise, 
                                                return_on_investment = return_on_investment)
        # Check if the current savings is less than the down payment, if so, set the lower bound of
        # our "guess" to the portion_saved and reset the current_savings back to 0.
        if current_savings < down_payment:
            low_bound = portion_saved
            current_savings = 0.
        
        # Check if the current savings are greater than the down_payment plus the tolerance, if so
        # set the high_bound of our guess to the portion_saved and reset the current_savings value
        # back to 0.
        elif current_savings > down_payment + tolerance:
            high_bound = portion_saved
            current_savings = 0.
        
        # If the binary search algorithm has to iterate more than 100 times, this means that a 
        # solution will not be found for that value of starting income, so print out an error
        # message.
        if steps > 100:
            print('It is not possible to pay the down payment in three years.')
            break
        
        # Set the 'guess' (portion_saved) value to the midpoint of the low and high bounds.
        portion_saved = (low_bound+high_bound)/2
        
        # Increment the steps (iteration count) by 1.
        steps += 1
    
    # If a solution is found (steps are less than 100), print the best savings rate and the number
    # of steps needed to reach that value in the bisection search.
    if steps < 100:
        print(f'Best savings rate: {int(portion_saved)/10000} ')
        print(f'Steps in bisection search: {steps}')

if __name__ == '__main__':
    main()