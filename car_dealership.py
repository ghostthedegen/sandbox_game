
car_shop_inventory = {
    "Tesla Model 3": 38990,
    "Toyota Camry": 26420,
    "Ford Mustang": 30920,
    "Honda Civic": 23950,
    "BMW 3 Series": 44500
}

car_sell_prices = {
    "Tesla Model 3": 33000,
    "Toyota Camry": 22500,
    "Ford Mustang": 26000,
    "Honda Civic": 20000,
    "BMW 3 Series": 38000
}


def add_item(inventory, item, quantity):

    if quantity <= 0:
        print("[ERROR] Quantity must be greater than zero!")
        return inventory

    if item in inventory:
        inventory[item] += quantity
    else:
        inventory[item] = quantity

    return inventory


def remove_item(inventory, item):

    if item not in inventory or inventory[item] <= 0:
        print("[ERROR] You don't own this vehicle!")
        return inventory

    inventory[item] -= 1

    if inventory[item] == 0:
        del inventory[item]

    return inventory


def show_garage(inventory):

    print("\n========== YOUR GARAGE ==========")

    if not inventory:
        print("Your garage is empty.")
    else:
        for car, quantity in inventory.items():
            print(f"{car:<20} | Owned: {quantity}")

    print("=================================")


def show_car_shop(car_shop_inventory):

    print("\n============== CAR DEALERSHIP ==============")
    print(f"{'VEHICLE':<22} | {'BUY PRICE':>12}")
    print("--------------------------------------------")

    for car, price in car_shop_inventory.items():
        print(f"{car:<22} | ${price:>11,}")

    print("============================================")


def buy_car(car_shop_inventory, money, inventory):

    show_car_shop(car_shop_inventory)

    print(f"\nAvailable Balance: ${money:,}")

    car = input("\nWhich car would you like to buy? ").strip()

    if car not in car_shop_inventory:
        print("\n[ERROR] Vehicle not available!")
        return money, inventory

    car_price = car_shop_inventory[car]

    if money < car_price:
        print("\n========== PURCHASE FAILED ==========")
        print(f"Vehicle:          {car}")
        print(f"Vehicle Price:    ${car_price:,}")
        print(f"Your Balance:     ${money:,}")
        print(f"Money Needed:     ${car_price - money:,}")
        print("=====================================")
        return money, inventory

    money -= car_price
    inventory = add_item(inventory, car, 1)

    print("\n========== PURCHASE SUCCESSFUL ==========")
    print(f"Vehicle:          {car}")
    print(f"Purchase Price:   ${car_price:,}")
    print(f"Money Remaining:  ${money:,}")
    print("========================================")

    return money, inventory


def sell_car(inventory, money, car_sell_prices):

    show_garage(inventory)

    if not inventory:
        return money, inventory

    car = input("\nWhich car would you like to sell? ").strip()

    if car not in inventory or inventory[car] <= 0:
        print("\n[ERROR] You don't own this vehicle!")
        return money, inventory

    if car not in car_sell_prices:
        print("\n[ERROR] Selling price unavailable!")
        return money, inventory

    car_price = car_sell_prices[car]

    money += car_price
    inventory = remove_item(inventory, car)

    print("\n========== VEHICLE SOLD ==========")
    print(f"Vehicle:          {car}")
    print(f"Sale Price:       ${car_price:,}")
    print(f"Money Remaining:  ${money:,}")
    print("==================================")

    return money, inventory
