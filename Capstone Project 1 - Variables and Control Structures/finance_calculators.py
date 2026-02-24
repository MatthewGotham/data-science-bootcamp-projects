# import math
# I don't need this ^.

# A while loop is used so that the user will continue to be asked the opening
# question if he/she does not give an appropriate response to it.
while True:

    user_selection = input(
'''Choose either 'investment' or 'bond' from the menu below to proceed:
    
investment  -  to calculate the amount of interest you'll earn on your 
 investment
bond        -  to calculate the amount you'll have to pay on a home loan

''')

    if (user_selection == "investment" 
    or user_selection == "Investment" 
    or user_selection == "INVESTMENT"):

        # We ask the user for the particulars of his/her investment.
        deposit = float(input("How much money are you depositing (£)?\n"))
        interest_rate = float(input("What is the rate of interest (%)?\n"))
        term =  float(input("For how many years will you be investing?\n"))
        interest_type = int(input(
'''Please enter 1 for simple interest, or 2 for compound interest.\n'''))

        if interest_type == 1:
            # This calculates simple interest.
            final_amount = round(deposit + (deposit * (interest_rate / 100) 
            * term), 2)
            print (
f'''The total amount once interest has been applied is £{final_amount}.''')

        elif interest_type == 2:
            # This calculates compound interest.
            final_amount = round(deposit * (1 + interest_rate / 100) ** term
            , 2)
            print (
f'''The total amount once interest has been applied is £{final_amount}.''')

        else:
            print("I don't recognise that selection.\n")
            # We start the whole process again if we don't get a satisfactory 
            # input.
            continue

        # We now exit the loop, having produced a final output for the user.
        break

    elif (user_selection == "bond" 
    or user_selection == "Bond" 
    or user_selection == "BOND"):

        # We ask the user for the particulars of his/her loan.
        principal = float(input(
'''What is the present value of the house (£)?\n'''))
        interest_rate = float(input("What is the interest rate (%)?\n"))
        term = float(input("Over how many months will repayment be made?\n"))
        monthly_rate = (interest_rate / 100) / 12
        payment = round((monthly_rate * principal) 
        / (1 - (1 + monthly_rate) ** (1 - term)), 2)
        print(f"Your montly payment is £{payment}.")

        # We now exit the loop, having produced a final output for the user.
        break

    else:
        # If the selection is not recognise, the loop will repeat.
        print ("I don't recognise that selection.\n")