import datetime


def ask_integer(min_value, max_value, prompt):
    """fonction qui a pour but de demander a l'utilisateur de rentrer une valeur entiere comprise
    entre min_value et max_value et de reiterer cette demande pour chaque saisie erronée"""
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return str(value)
        except ValueError:
            pass


def ask_string(min_length, max_length, prompt):
    """fonction qui a pour but de demander a l'utilisateur de rentrer une valeur entiere comprise
    entre min_value et max_value et de reiterer cette demande pour chaque saisie erronée"""
    while True:
        try:
            value = input(prompt)
            if min_length <= len(value) <= max_length:
                return value
        except ValueError:
            pass


def ask_choice(choices, prompt):
    """fonction qui a pour but de demander a l'utilisateur de rentrer une valeur entiere comprise
    entre min_value et max_value et de reiterer cette demande pour chaque saisie erronée"""
    print(prompt)
    while True:
        try:
            value = input("Enter Your Choice : ")
            if value.capitalize() in choices:
                return value.capitalize()
        except ValueError:
            pass


def ask_date(min_date, max_date, prompt):
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
