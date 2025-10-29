import sys, os
from datetime import datetime
from PySide6 import QtCore, QtWidgets

cur_dir = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from Utils.program_utils import *
from Utils.supabase_utils import *

from dotenv import load_dotenv, dotenv_values
dotenv_path = os.path.join(par_dir, "sensitive.env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")

class CheckBalanceWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.account_combo = QtWidgets.QComboBox()
        self.details_text = QtWidgets.QTextEdit()
        self.details_text.setReadOnly(True)
        self.check_btn = QtWidgets.QPushButton("Check Balance")
        self.check_btn.clicked.connect(self.show_balance)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Select Account:"))
        layout.addWidget(self.account_combo)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.details_text)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        self.accounts = view_table("PF_accounts", key=API_KEY).data
        self.account_combo.addItems([a["name"] for a in self.accounts])

    def show_balance(self):
        idx = self.account_combo.currentIndex()
        account = self.accounts[idx]

        text = f"-----{account['name']}-----\n"
        text += f"Type: {account['type']}\n"
        text += f"Balance: ${account['balance']}\n\n"

        filter = {"col": "account_id", "op": "eq", "x": account["id"]}
        recent = view_table("PF_transactions", view_limit=5, filter=filter, key=API_KEY).data
        for rt in recent:
            sign = "-" if rt["expense"] else "+"
            text += f"{sign}${rt['amount']} - {rt['date']}\n{rt['description']}\n\n"

        self.details_text.setText(text)