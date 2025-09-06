import mysql.connector, os
import sensitive
import supabase_utils
from datetime import datetime

def clear_and_print(header):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(header)


def open_sql():
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sensitive.password,
        database="Personal_Finance_DB"
    )
    return (my_db.cursor(), my_db)


def add_transaction():
    # First get the type of transaction, is it expense or income
    trans_type = -1
    while trans_type not in (1, 2):
        clear_and_print("-----Transaction Type-----")
        print("1) Expense")
        print("2) Income")
        trans_type = int(input("Type: "))
    
    cursor, my_db = open_sql()
    
    if trans_type == 1:   
        cat_table = cursor.execute("SELECT * FROM expense_categories")
        expense = True
    elif trans_type == 2: 
        cat_table = cursor.execute("SELECT * FROM income_categories")
        expense = False
    
    all_rows = cursor.fetchall()
    max_val = len(all_rows)
    category_id = float('inf')
    
    while category_id not in range(1, max_val + 1):
        header = "-----Expense Type-----" if trans_type == 1 else "-----Income Type-----"
        clear_and_print(header)
        for id, type in all_rows:
            print(f'{id}) {type}')
        try:
            category_id = int(input("Type: "))
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
    # TODO - set up validity check for the date input
    
    clear_and_print("-----Additional Information-----")
    date_str = input("MM-DD-YYYY: ")
    date = datetime.strptime(date_str, "%m-%d-%Y").date()
    
    while(True):
        try:
            amt = float(input("Amount: "))
            desc = input("Description: ")
            break
        except ValueError:
            clear_and_print("-----Additional Information-----")
            print(f'MM-DD-YYYY: {date_str}')
            
    """
    transaction table layout:
        date -> DATE
        amount -> DECIMAL
        description -> VARCHAR
        category_id -> INT
        account_id -> INT
        recur_id -> INT
    """
    cursor.execute('''INSERT INTO transactions (date, amount, description, expense, category_id, account_id) VALUES
                        (%s, %s, %s, %s, %s, %s);''', (date, amt, desc, expense, category_id, account_id))
    
    my_db.commit()
    
    cursor.close()
    my_db.close()
    
    
def check_balances():
    cursor, my_db = open_sql()
    cursor.execute("SELECT * FROM accounts")
    all_accounts = cursor.fetchall()
    
    selected_account = [0]
    while selected_account[0] not in range(1, len(all_accounts) + 1):
        clear_and_print("-----Account to Check-----")
        for account in all_accounts:
            print(f'{account[0]}) {account[1]}')
        try:
            selected_account = all_accounts[int(input("Account: ")) - 1]
        except (ValueError, IndexError):
            pass
    
    clear_and_print(f'-----{selected_account[1]}-----')
    print(f'Type of Account: {selected_account[2]}')
    print(f'Account Balance: {selected_account[3]}\n')
    
    cursor.execute(f"""SELECT * FROM transactions 
                        WHERE account_id = {selected_account[0]}
                        ORDER BY date DESC
                        LIMIT 5""")
    recent_transactions = cursor.fetchall()
    
    if len(recent_transactions) > 0: print(f'-----Recent Transactions-----')
    
    for i in range(0, min(len(recent_transactions), 5)):
        #transaction -> [id, date, amount, description, expense, cat_id, act_id, recur_id]
        t = recent_transactions[i]
        print(f'date: {t[1]}\namount: ${t[2]}\ntype: {"Expense" if t[4] else "Income"}')
        
        if t[4]:
            cursor.execute("""SELECT * FROM expense_categories""")
            expenses = cursor.fetchall()
            print(f'category: {expenses[t[5]][1]}\n')
        else:
            cursor.execute("""SELECT * FROM income_categories""")
            incomes = cursor.fetchall()
            print(f'category: {incomes[t[5]][1]}\n')


def program_primary():
    clear_and_print("-----Personal Finance Tracker-----")
    action = 0
    while action not in (1, 2):
        clear_and_print("-----Personal Finance Tracker-----")
        print("1) Add a Transaction")
        print("2) Check Account Balances")
        action = int(input("Option: "))
    if action == 1: add_transaction()
    elif action == 2: check_balances_2()

program_primary()