import os

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = [
    "Morning",
    "Afternoon",
    "Evening",
    "Night",
]

def parse_choice(user_input, allowed_options, field_name):
    cleaned_input = str(user_input).strip()

    for allowed_option in allowed_options:
        if allowed_option.lower() == cleaned_input.lower():
            return allowed_option

    raise ValueError(
        f"Invalid {field_name}. "
        f"Choose from : {', '.join(allowed_options)}"
    )

def parse_int_in_range(user_input, minimum, maximum):
    cleaned_input = str(user_input).strip()
    
    try:
        number = int(cleaned_input)

    except ValueError:
        raise ValueError(
            f"Must be a whole number! "
            f"Range must be from {minimum} to {maximum}"
        )

    if number < minimum or number > maximum:
        raise ValueError(
            f"Value must be from {minimum} to {maximum}"

        )

    return number

def parse_name(user_input):
    cleaned_input = str(user_input).strip()

    if cleaned_input == "":
        raise ValueError("Name cannot be empty")

    return cleaned_input


def parse_destination(user_input):
    return parse_choice(user_input, DESTINATIONS, "destination")

def parse_timeslot(user_input):
    return parse_choice(user_input, TIME_SLOTS, "time slot")

def parse_year(user_input):
    return parse_int_in_range(user_input, 1, 5)

def parse_seats(user_input):
    return parse_int_in_range(user_input, 1, 4)

def ask_user(question, parser):
    while True:
        user_input = input(question)

        if user_input.strip().lower() == "cancel":
            return None

        try:
            valideted_value = parser(user_input)
            return valideted_value

        except ValueError as error:
            print(error)
