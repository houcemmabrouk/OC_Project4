import datetime


def ask_integer(min_value, max_value, prompt):
    """This function aims to control an input of an integer bounded by min_value and max_value besides the function
     takes as an argument the prompt meant to be displayed"""
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return str(value)
        except ValueError:
            pass


def ask_string(min_length, max_length, prompt):
    """This function aims to control an input of a string with a minimum number of characters min_length and a maximum
    number of characters max_length besides the function takes as an argument the prompt meant to be displayed"""
    while True:
        try:
            value = input(prompt)
            if min_length <= len(value) <= max_length:
                return value
        except ValueError:
            pass


def ask_choice(choices, prompt):
    """This function aims to control an input of a choice from a list of choices the function takes as an argument
     the prompt meant to be displayed"""
    print(prompt)
    while True:
        try:
            value = input("Enter Your Choice : ")
            if value.upper() in choices:
                return value.capitalize()
        except ValueError:
            pass


def ask_date(min_date, max_date, prompt):
    """This function aims to control an input of a date from a min_date to a max_date and display a prompt"""
    print(prompt)
    while True:
        try:
            day = int(input("Enter Day : "))
            month = int(input("Enter Month : "))
            year = int(input("Enter Year : "))
            value = datetime.date(year, month, day)
            if min_date <= value <= max_date:
                return value
        except ValueError:
            pass
