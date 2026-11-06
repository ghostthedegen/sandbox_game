from businesses.names import find_name

arcades = {
    "Pixel Palace": 15000,
    "Retro Haven": 30000,
    "Neon Empire": 60000
}

arcade_income = {
    "Pixel Palace": 500,
    "Retro Haven": 1200,
    "Neon Empire": 2500
}

def buy_arcade(money, owned_arcades, arcades):

    for place, price in arcades.items():
        print(f"{place}:{price}")

    question = find_name(input("What arcade would you like to buy ? "), arcades)

    if question is None:
        print("Arcade does not exist")
        return money, owned_arcades

    if question in owned_arcades:
        print("You already own this property")
        return money, owned_arcades
    
    price = arcades[question]

    if money >= price:
        print(f"{price}")
        money -= price
        owned_arcades.append(question)
        print(f"Balance: {money}")
    else:
        print("Not enough money")
    
    return money, owned_arcades

def collect_arcade_income(money, owned_arcades, arcade_income):

    if not owned_arcades:
        print("you don't own this property")
        return money

    total_income = 0

    for arcade in owned_arcades:

        income = arcade_income[arcade]

        total_income += income

    money += total_income

    print(f"Total daily income: {total_income}")
    print(f"Balance: {money}")

    return money


