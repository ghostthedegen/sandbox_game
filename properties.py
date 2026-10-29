property_levels = {"small_shop": 1}
upgrade_costs = {1: 200, 2: 400}   
MAX_LEVEL = 3
property_name = {"small_shop": 300}

def upgrade_property(building, owned_properties, property_levels, money):
    if building not in owned_properties:
        print("You do not own this property")
        return money, building, property_levels
        

    level = property_levels[building]

    if level >= MAX_LEVEL:
        print("Property is already max level")
        return money, building, property_levels   

    cost = upgrade_costs[level]

    if money < cost:
        print(f"${money}")
        print("Not enough money")
        return money, building, property_levels
        
    print(f"Money: ${money}")
    money -= cost
    print(f"Money Remaining: ${money}")
    property_levels[building] += 1
    print(f"{building} upgraded to level {property_levels[building]}")

    return money, building, property_levels

def property_bonus(building, owned_properties, property_levels):

    if building in owned_properties:
        
        if property_levels[building] == 2:
            print("property bonus $5 per customer")
            return 5

        elif property_levels[building] == 3:
            print("property bonus $10 per customer")
            return 10

        else:
            return 0
    
    else:
        print("You do not own the property")
        return 0

def buy_property(money, property_name, owned_properties):

    for building, cost in property_name.items():

        if building in owned_properties:
            print("you already own this property")

        elif money >= cost:
            print(f"Money: ${money}")
            answer = input("Are you sure you want to purchase the property ? ").lower()
            if answer == "yes" or answer == "y":
                money -= cost
                owned_properties.append(building)
                print("Property has been purchased")
                print(f"Money remaining: ${money}")
            else:
                print("Property has not been purchased")

        else:
            print("You don't have enough money")

    return money, owned_properties