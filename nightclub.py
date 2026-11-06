nightclubs = {
    "Downtown Club": 50000,
    "Neon Palace": 75000,
    "VIP Lounge": 120000
}

nightclub_income = {
    "Downtown Club": 1500,
    "Neon Palace": 3000,
    "VIP Lounge": 5000
}

nightclub_popularity = {
    "Downtown Club": 50,
    "Neon Palace": 70,
    "VIP Lounge": 90
}

owned_nightclubs = []


def buy_nightclub(money, owned_nightclubs, nightclubs):

    for place, price in nightclubs.items():
        print(f"{place}:{price}")

    question = input("Which club do you want to buy ? ")

    if question not in nightclubs:
        print("This nightclub does not exist")
        return money, owned_nightclubs

    price = nightclubs[question]

    if question in owned_nightclubs:
        print("You already own this club")
        return money, owned_nightclubs

    
    print(f"{question} is for sale")

    if money >= price:
        print(f"The club cost: ${price}")
        money -= price
        owned_nightclubs.append(question)
        print(f"Balance: ${money}")
    
    else:
        print("You don't have enough money")
        return money, owned_nightclubs     
    
    return money, owned_nightclubs

def collect_nightclub_income(owned_nightclubs, money, nightclub_income):

    if not owned_nightclubs:
        print("You don't own any nightclubs")
        return money

    else:

        total_income = 0

        for clubs in owned_nightclubs:
            if clubs in nightclub_income:
                income = nightclub_income[clubs]
                total_income += income
            
            else:
                print(f"No income configured for {clubs}")
                

        money += total_income
        print(f"Total nightclub income: ${total_income:,}")
        print(f"New balance: ${money:,}")

    return money







                


