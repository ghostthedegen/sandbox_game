class BankAccount:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []
        self.loan.balance = 0

    def deposit(self, player, amount):

        if amount <= 0:
            print("Amount must be above 0")

        elif player.money >= amount:
            player.money -= amount
            self.balance += amount
            self.transactions.append(f"Deposit: £{amount}")

            print(f"Deposited £{amount}")
            print(f"Cash: £{player.money}")
            print(f"Bank balance: £{self.balance}")

        else:
            print("Not enough cash")

    def withdraw(self, player, amount):

        if amount <= 0:
            print("Amount must be above 0")

        elif self.balance >= amount:
            self.balance -= amount
            player.money += amount
            self.transactions.append(f"Withdraw: £{amount}")

            print(f"Withdrew £{amount}")
            print(f"Cash: £{player.money}")
            print(f"Bank balance: £{self.balance}")

        else:
            print("Not enough money in the bank")

    def transfer(self, other_account, amount):

        if amount <= 0:
            print("Amount must be above 0")

        elif self.balance >= amount:
            self.balance -= amount
            other_account.balance += amount

            print(
                f"{self.name} transferred £{amount} "
                f"to {other_account.name}"
            )

        else:
            print("Transfer was not successful")

    def show_transaction(self):

        print("BANK TRANSACTION HISTORY")
        print(f"Balance: £{self.balance}")

        if not self.transactions:
            print("No transactions found")
            return

        for item in self.transactions:
            print(item)

        depo = len(self.transactions)

        print(f"Total transactions: {depo}")

    def borrow_money(self, player, amount):

        interest = int(amount * 0.1)

        if amount <= 0:
            print("Loan amount must be greater than 0")
            return
        
        elif amount > 50000:
            print("Amount is to high to loan")
            return

        elif self.loan_balance > 0:
            print("You already have an outstanding loan")
            return

        else:
            print(f"You've been approved for: £{amount}")
            total_repayment = amount + interest

            player.money += amount
            self.loan_balance = total_repayment
            print(f"Total repayment:{amount}")
            self.transactions.append(f"Borrowed: £{amount} | Total repayment: £{total_repayment}")
        
        return 


    def repay_loan(self, player, amount):

        if self.loan_balance <= 0:
            print("You have no outstanding loan")
            return

        if amount <= 0:
            print("Amount must be above 0")
            return

        if amount > self.loan_balance:
            print(f"You only owe £{self.loan_balance}")
            return

        if player.money < amount:
            print("Not enough cash")
            return

        player.money -= amount
        self.loan_balance -= amount
        self.transactions.append(f"Loan repaid: £{amount}")

        print(f"Paid £{amount}")
        print(f"Remaining loan: £{self.loan_balance}")
        print(f"Cash: £{player.money}")

        if self.loan_balance == 0:
            print("Loan fully repaid!")




        


        


