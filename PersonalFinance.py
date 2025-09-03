import mysql.connector, os
import sensitive

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def add_transaction(date, amount, description, cat_id, act_id, recur_id=0):
    # First get the type of transaction, is it expense or income
    trans_type = -1
    while trans_type not in (1, 2):
        clear_terminal()
        print("-----Transaction Type-----")
        print("1) Expense")
        print("2) Income")
        trans_type = int(input("Type: "))
    
    # Now get the categories table for that specific type
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sensitive.password,
        database="Personal_Finance_DB"
    )
    
    cursor = my_db.cursor()
    if trans_type == 1: # Expense
        cat_table = cursor.execute("SELECT * FROM expense_categories")
    elif trans_type == 2: #Income
        cat_table = cursor.execute("SELECT * FROM income_categories")
    else:
        raise Exception
    
    temp = cursor.fetchall()

    print(temp)

add_transaction(None, None, None, None, None)