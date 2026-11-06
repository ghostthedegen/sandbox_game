import time

day = 1

customers_served_today = 0

phase_start_time = time.time()

time_of_day = "day"

def update_time_of_day(time_of_day, phase_start_time, day):

    current_time = time.time()
    seconds = current_time - phase_start_time

    if seconds >= 2400:

        if time_of_day == "day":
            time_of_day = "night"
            print("Starting Night Time")

        else:
            time_of_day = "day"
            day += 1
            print("Starting Day Time")
            print(f"Day {day}")

        phase_start_time = current_time

    return time_of_day, phase_start_time, day

def time_remaining(phase_start_time):
    
    current_time = time.time()

    seconds = current_time - phase_start_time

    current = 2400 - seconds

    time_left = current / 60

    return time_left

def phase_elapsed(phase_start_time):

    return time.time() - phase_start_time

def phase_start_from_elapsed(elapsed_seconds):

    return time.time() - elapsed_seconds
