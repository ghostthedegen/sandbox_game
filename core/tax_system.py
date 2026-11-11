def calculate_tax(income, tax_rate):
    
    if income <= 0:
        return 0
    
    if not (0 <= tax_rate <= 1):
        return 0

    tax = int(income*tax_rate)

    return tax

def collect_tax(money, income, tax_rate):

    

    tax = calculate_tax(income, tax_rate)

    if money < tax:
        unpaid_tax = tax
        print("Not enough money to pay tax")
        return money, unpaid_tax
    
    money -= tax
    
    print(f"Paid {tax} in tax. remaning balance: {money}")

    unpaid_tax = 0

    return money, unpaid_tax
