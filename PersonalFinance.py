import mysql.connector, os
import sensitive
import supabase_utils as su
from datetime import datetime

def clear_and_print(header):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(header)


def add_transaction():
    # DETERMINE EXPENSE VS INCOME
    trans_type = -1
    while trans_type not in (1, 2):
        clear_and_print("-----Transaction Type-----")
        print("1) Expense")
        print("2) Income")
        trans_type = int(input("Type: "))
    
    expense = (True, False)[trans_type - 1]
    valid_table = "PF_expense_categories" if expense else "PF_income_categories"

    all_categories = su.view_table(valid_table).data
    max_val = len(all_categories)
    category_id = float('inf')

    while category_id not in range(1, max_val + 1):
        header = "-----Expense Type-----" if expense else "-----Income Type-----"
        clear_and_print(header)

        for row in all_categories:
            print(f"{row['id']}) {row['name']}")

        try:
            category_id = int(input("Type: "))
        except ValueError:
            pass
    
    # FETCH THE ACCOUNT
    account_id = 0
    all_accounts = su.view_table("PF_accounts").data

    while account_id not in range(1, len(all_accounts) + 1):
        clear_and_print("-----Account Information-----")
        
        for row in all_accounts:
            print(f"{row['id']}) {row['name']}")
        
        try:
            account_id = int(input("Account: "))
        except ValueError:
            pass
    
    # FETCH ADDITIONAL TRANSACTION INFORMATION
    # TODO -> Potentially use a natural language API to make a date checker
    clear_and_print("-----Additional Information-----")
    date, amt, desc = None, None, None

    while(True):
        try:
            if not date:
                date_str = input("MM-DD-YYYY: ")
                date = datetime.strptime(date_str, "%m-%d-%Y").date()
            if not amt: 
                amt = float(input("Amount: "))
            if not desc: 
                desc = input("Description: ")
            break
        except ValueError:
            clear_and_print("-----Additional Information-----")
            if date: 
                print(f'MM-DD-YYYY: {date_str}')
            if amt: 
                print("Amount: ", amt)
            if desc: 
                print("Description: ", desc)
    
    # PREPARE TO EXECUTE INSERT ON DATABASE
    trans_dict = {'id': len(su.view_table("PF_transactions", view_limit=float('inf')).data) + 1, 
                  'date': date.isoformat(),
                  'amount': amt,
                  'description': desc,
                  'expense': expense,
                  'category_id': category_id,
                  'account_id': account_id,
                }
    su.add_to_db("PF_transactions", trans_dict)
            
    
def check_balances():
    all_accounts = su.view_table("PF_accounts").data
    
    selected_account_id = 0
    while selected_account_id not in range(1, len(all_accounts) + 1):
        clear_and_print("-----Account to Check-----")
        for account in all_accounts:
            print(f'{account["id"]}) {account["name"]}')
        try:
            selected_account_id = all_accounts[int(input("Account: ")) - 1]['id']
        except (ValueError, IndexError):
            pass
    
    selected_account = all_accounts[selected_account_id - 1]

    clear_and_print(f'-----{selected_account["name"]}-----')
    print(f'Type of Account: {selected_account["type"]}')
    print(f'Account Balance: {selected_account["balance"]}\n')

    filter = {'col': 'account_id', 'op': 'eq', 'x': selected_account_id}
    recent_transactions = su.view_table(table="PF_transactions", view_limit=5, filter=filter).data

    for rt in recent_transactions:
        if rt['expense']:
            print(f"-${rt['amount']} - {rt['date']}")
        else:
            print(f"${rt['amount']} - {rt['date']}")
        print(f"{rt['description']}\n")

def program_primary():
    clear_and_print("-----Personal Finance Tracker-----")
    action = 0
    while action not in (1, 2):
        clear_and_print("-----Personal Finance Tracker-----")
        print("1) Add a Transaction")
        print("2) Check Account Balances")
        action = int(input("Option: "))
    if action == 1: add_transaction()
    elif action == 2: check_balances()

program_primary()