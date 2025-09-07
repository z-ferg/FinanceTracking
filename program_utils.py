import os

def clear_and_print(header):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(header)


def get_choice(header, options, key="name"):
    choice = None
    ids = [row["id"] for row in options]
    
    while choice not in ids:
        clear_and_print(header)
        for row in options:
            print(f"{row['id']}) {row[key]}")
        try:
            choice = int(input("Select: "))
        except ValueError:
            pass
    return choice