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
    "night_drink": 80,
    "protein": 60,
    "premium_coffee": 110
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

    if quantity <= 0:
        print("Quantity must be above 0")

    elif item in shop:
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

def show_inventory(inventory, sell_prices):

    if not inventory:
        print("Inventory is empty")
        return

    print("\n========== INVENTORY ==========")

    for item in inventory:

        stock = inventory[item]
        price = sell_prices.get(item, 0)

        if stock == 0:
            status = "OUT OF STOCK"

        elif 0 < stock <= 2:
            status = "LOW STOCK"

        else:
            status = "GOOD STOCK"

        print(f"{item:<15} | Stock: {stock:<5} | Price: ${price} | {status}")

    print("================================")

def calculate_restock(inventory, item, target_stock):

    if target_stock < 0:
        return 0

    stock = inventory.get(item, 0)

    missing_stock = target_stock - stock

    if missing_stock <= 0:
        return 0

    return missing_stock

def calculate_inventory_value(inventory, shop):

    total_cost = 0

    print("========== INVENTORY VALUE ==========")

    for item in inventory:

        quantity = inventory[item]
        price = shop[item]
        

        total_value = price * quantity

        total_cost += total_value

        print(f"{item:<15} | {quantity:<5} | ${price} | ${total_value}")

    print("=====================================")
    print(f"Total inventory value: ${total_cost}")

    return total_cost













        