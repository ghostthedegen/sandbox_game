shop = {
    "coffee": 20,
    "energy": 15,
    "snack": 10,
    "night_drink": 50
}

sell_prices = {
    "coffee": 30,
    "energy": 25,
    "snack": 18,
    "night_drink": 80
}

def add_item(inventory, item, quantity):

    
    if item in inventory:
        inventory[item] += quantity
    else:
        inventory[item] = quantity

    return inventory

def remove_item(inventory, item):

    if item in inventory:
        inventory[item] -= 1

        if inventory[item] == 0:
            del inventory[item]
            
    return inventory
   
def buy_item(money, inventory, item, shop, quantity):

    if item in shop:
        print(f"Current item in the inventory: {inventory}")
        price = shop[item]

        total_cost = price * quantity

        if money >= total_cost:
            money -= total_cost
            inventory = add_item(inventory, item, quantity)

            print(f"Bought {quantity} {item}")
            print(f"Total cost: ${total_cost}")
            print(f"Money remaining: ${money}")

        else:
            print("not enough money")

    else:
        print("Item does not exist")
    
    return money, inventory
        
def sell_item(money, inventory, item, sell_prices):

    if item in inventory:
        selling_price = sell_prices[item]
        money += selling_price
        inventory = remove_item(inventory, item)
        print(f"Sold {item} for ${selling_price}")
        
    else:
        print("You don't own the item")
    
    return money, inventory