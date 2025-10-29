import time
from datetime import datetime
from Utils.program_utils import *
from Utils.supabase_utils import *


def add_transaction():
    # Anonymous Function to determine Expense vs Income
    def get_transaction_type():
        options = [
            {"id": 1, "name": "Expense"},
            {"id": 2, "name": "Income"}
        ]
        choice = get_choice("-----Transaction Type-----", options)
        return choice == 1

    # Anonymous Function for Fetching Additional Transaction Information
    def get_transaction_info():
        while True:
            try:
                clear_and_print("-----Additional Information-----")
                date = datetime.strptime(input("MM-DD-YYYY: "), "%m-%d-%Y").date()
                amt = float(input("Amount: "))
                desc = input("Description: ")
                return date, amt, desc
            except ValueError:
                clear_and_print("-----Invalid input. Try again.-----")
                time.sleep(0.75)
    
    # Primary work to get information and add to database!
    expense = get_transaction_type()
    table = "PF_expense_categories" if expense else "PF_income_categories"
    
    category_id = get_choice("-----Category-----", view_table(table).data)
    account_id = get_choice("-----Account-----", view_table("PF_accounts").data)
    
    clear_and_print("-----Additional Information-----")
    date, amt, desc = get_transaction_info()
    
    transactions = view_table("PF_transactions", view_limit=float('inf')).data
    transaction = {
        'id': len(transactions) + 1,
        "date": date.isoformat(),
        "amount": amt,
        "description": desc,
        "expense": expense,
        "category_id": category_id,
        "account_id": account_id
    }
    
    add_to_db("PF_transactions", transaction)


def check_balances():
    accounts = view_table("PF_accounts").data
    account_id = get_choice("-----Account to Check-----", accounts)
    
    account = next(acc for acc in accounts if acc["id"] == account_id)
    clear_and_print(f'-----{account["name"]}-----')
    print(f'Type of Account: {account["type"]}')
    print(f'Account Balance: {account["balance"]}\n')

    filter = {"col": "account_id", "op": "eq", "x": account_id}
    recent = view_table("PF_transactions", view_limit=5, filter=filter).data
    
    for rt in recent:
        sign = "-" if rt["expense"] else ""
        print(f"{sign}${rt['amount']} - {rt['date']}")
        print(f"{rt['description']}\n")


def program_primary():
    options = [
        {"id": 1, "name": "Add a Transaction"},
        {"id": 2, "name": "Check Account Balances"}
    ]
    action = get_choice("-----Personal Finance Tracker-----", options)
    match action:
        case 1:
            add_transaction()
        case 2:
            check_balances()
        case _:
            pass

if __name__=="__main__":
    program_primary()