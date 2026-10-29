from shop import remove_item
import random

def complete_order(money, inventory, reputation, customer_order, sell_prices):

    if customer_order in inventory:
        selling_price = sell_prices[customer_order]
        money += selling_price 
        inventory = remove_item(inventory, customer_order)
        reputation += 1
        print("order completed")
        order_completed = True
            
    else:
        print("You don't have the required item")
        order_completed = False
    return money, inventory, reputation, order_completed

def create_customer_queue(customer_options):
    customer_queue = []

    for i in range(3):
        customer_order = random.choice(customer_options)
        customer_queue.append(customer_order)

    return customer_queue

def replace_customer(customer_queue, customer_options):
    customer_queue.pop(0)
    customer_order = random.choice(customer_options)
    customer_queue.append(customer_order)
    print(f"New customer wants: {customer_order}")
    return customer_queue