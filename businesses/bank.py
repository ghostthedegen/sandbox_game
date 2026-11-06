class BankAccount:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []

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