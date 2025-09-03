import mysql.connector, os
import sensitive

def clear_and_print(header):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(header)

def add_transaction():
    # First get the type of transaction, is it expense or income
    trans_type = -1
    while trans_type not in (1, 2):
        clear_and_print("-----Transaction Type-----")
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
    if trans_type == 1:   cat_table = cursor.execute("SELECT * FROM expense_categories")
    elif trans_type == 2: cat_table = cursor.execute("SELECT * FROM income_categories")
    
    all_rows = cursor.fetchall()
    max_val = len(all_rows)
    category_id = float('inf')
    
    while category_id not in range(1, max_val + 1):
        header = "-----Expense Type-----" if trans_type == 1 else "-----Income Type-----"
        clear_and_print(header)
        for id, type in all_rows:
            print(f'{id}) {type}')
        try:
            category_id = int(input("Source: "))
        except ValueError:
            pass
    
    category_id, category_name = all_rows[category_id - 1]
    
    # Now lets get the account information
    account_id = 0
    cursor.execute("SELECT * FROM Personal_Finance_DB.accounts")
    all_rows = cursor.fetchall()
    
    while account_id not in range(1, len(all_rows) + 1):
        clear_and_print("-----Account Information-----")
        for id, name, _, _ in all_rows:
            print(f'{id}) {name}')
        account_id = int(input("Account: "))
    
    # Now lets get the final information required
    while(True):
        clear_and_print("-----Additional Information-----")
        date = input("Date: ")
        amt = input("Amount: ")
        desc = input("Description: ")
        break
    

add_transaction()