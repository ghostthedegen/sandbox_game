def get_customer_options(time_of_day, reputation):

    customer_options = ["coffee", "energy", "snack"]

    if reputation >= 5:
        customer_options.append("protein")

    if reputation >= 10:
        customer_options.append("premium_coffee")

    if time_of_day == "night":
        customer_options.append("night_drink")

    return customer_options