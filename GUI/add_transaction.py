import sys, os
from datetime import datetime
from PySide6 import QtCore, QtWidgets

# Retrieve the Utility Files
cur_dir = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from Utils.program_utils import *
from Utils.supabase_utils import *

# Fetch the API Key from environment variables
from dotenv import load_dotenv, dotenv_values
dotenv_path = os.path.join(par_dir, "sensitive.env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")

class AddTransactionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Combo Box for determining Expense/Income (Money Inflow vs Outflow)
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Expense", "Income"])

        # Date for easily getting date of the transaction
        self.date_edit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        # Spin Box for determining amount in transaction (1,000,000+ in would be nice but unrealistic)
        self.amount_edit = QtWidgets.QDoubleSpinBox()
        self.amount_edit.setMaximum(1_000_000)
        self.amount_edit.setPrefix("$")

        # Text box for describing nature of transaction
        self.desc_edit = QtWidgets.QLineEdit()

        self.category_combo = QtWidgets.QComboBox()
        self.account_combo = QtWidgets.QComboBox()

        self.submit_btn = QtWidgets.QPushButton("Add Transaction")
        self.submit_btn.clicked.connect(self.add_transaction)

        # Layout
        form = QtWidgets.QFormLayout()
        form.addRow("Transaction Type:", self.type_combo)
        form.addRow("Date:", self.date_edit)
        form.addRow("Amount:", self.amount_edit)
        form.addRow("Description:", self.desc_edit)
        form.addRow("Category:", self.category_combo)
        form.addRow("Account:", self.account_combo)
        form.addRow(self.submit_btn)
        self.setLayout(form)

        self.load_data()

    def load_data(self):
        self.accounts = view_table(table="PF_accounts", key=API_KEY).data
        self.account_combo.addItems([a["name"] for a in self.accounts])

        self.update_categories()
        self.type_combo.currentIndexChanged.connect(self.update_categories)

    def update_categories(self):
        self.category_combo.clear()
        expense = self.type_combo.currentText() == "Expense"
        table = "PF_expense_categories" if expense else "PF_income_categories"
        self.categories = view_table(table, key=API_KEY).data
        self.category_combo.addItems([c["name"] for c in self.categories])

    def add_transaction(self):
        expense = self.type_combo.currentText() == "Expense"
        category = self.categories[self.category_combo.currentIndex()]
        account = self.accounts[self.account_combo.currentIndex()]
        date = self.date_edit.date().toPython()
        amt = self.amount_edit.value()
        desc = self.desc_edit.text()

        transactions = view_table("PF_transactions", key=API_KEY, view_limit=float("inf")).data
        new_id = len(transactions) + 1

        transaction = {
            "id": new_id,
            "date": date.isoformat(),
            "amount": amt,
            "description": desc,
            "expense": expense,
            "category_id": category["id"],
            "account_id": account["id"],
        }

        add_to_db("PF_transactions", row_vals=transaction, key=API_KEY)
        QtWidgets.QMessageBox.information(self, "Success", "Transaction added successfully!")