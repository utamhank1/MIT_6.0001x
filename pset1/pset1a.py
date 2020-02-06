# Part A: how many months will it take to save for the dream house?
def main():
        
    # Wait for user input as to the user's annual salary.
    annual_salary = float(input('Enter your annual salary: '))


    portion_saved = float(input('Enter the percentage of your salary that you want to save,'
                                'as a decimal: '))
    
    # Wait for user input as to the value of the house in dollars.
    total_cost = float(input('Enter the total cost of your dream home: '))

    # Wait for user input as to the percentage of the annual salary that the user desires
    # to save.

    # Pre set parameters for calculation.
    # The percentage of the the house's value that is the downpayment.
    portion_down_payment = .25
    
    # The amount of money that the user currently has saved.
    current_savings = 0
    
    # The rate of return on the money that the user has saved.
    r = .04

    # Initialize values for the number of months that the user would need to save.
    num_months = 0
    
    # Condition for while loop termination, when current savings equal the amount of the 
    # downpayment.
    while current_savings < (total_cost*portion_down_payment):
        
        # Calculate the monthly savings and add them to the current savings, iterate the number
        # of months and the iteration variables by 1.
        monthly_saving = current_savings*(r/12) + (annual_salary/12)*portion_saved
        num_months += 1
        current_savings = current_savings + monthly_saving
    
    # Print summary values for after the loop has terminated and a solution has been found.
    print(f'Number of months: {num_months}')
        
if __name__ == '__main__':
    main()