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
from dotenv import load_dotenv
dotenv_path = os.path.join(par_dir, "sensitive.env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")


class CheckBalanceWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Create balance summary boxes ---
        self.summary_boxes = []
        self.summary_layout = QtWidgets.QHBoxLayout()
        self.summary_layout.setContentsMargins(0, 0, 0, 0)
        self.summary_layout.setSpacing(10)
        
        self.table = self.table_func()

        for i in range(3):
            box = QtWidgets.QFrame()
            box.setFrameShape(QtWidgets.QFrame.Box)
            box.setStyleSheet("""
                QFrame {
                    background-color: #5f8a8b;
                    border-radius: 8px;
                    padding: 12px;
                }
                QLabel {
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            vbox = QtWidgets.QVBoxLayout()
            name_label = QtWidgets.QLabel("Account")
            balance_label = QtWidgets.QLabel("$0.00")
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            balance_label.setAlignment(QtCore.Qt.AlignCenter)
            vbox.addWidget(name_label)
            vbox.addWidget(balance_label)
            box.setLayout(vbox)

            self.summary_boxes.append((name_label, balance_label))
            self.summary_layout.addWidget(box)

        # --- Main layout ---
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.summary_layout)  # Top row of boxes
        layout.addSpacing(20)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # --- Load initial data ---
        self.load_data()

    def load_data(self):
        self.accounts = view_table("PF_accounts", key=API_KEY).data

        # --- Populate summary boxes with balances ---
        for i, account in enumerate(self.accounts):
            name_label, balance_label = self.summary_boxes[i]
            name_label.setText(account["name"])
            balance_label.setText(f"${account['balance']:,}")
    
    def table_func(self):
        table = QtWidgets.QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                background-color: #5f8a8b;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                selection-background-color: #6ea1a2;
            }
            QHeaderView::section {
                background-color: #4e7a7b;
                color: white;
                padding: 6px;
            }
        """)
        
        col_ordering = ["Amount", "Date", "Description", "Category", "Account"]
        table.setColumnCount(len(col_ordering))
        table.setHorizontalHeaderLabels(col_ordering)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        recent_trans = view_table("PF_transactions", key=API_KEY).data
        accounts = view_table("PF_accounts", key=API_KEY).data
        expense_cats = view_table("PF_expense_categories", key=API_KEY).data
        income_cats = view_table("PF_income_categories", key=API_KEY).data
        
        account_ids = {a['id']: a['name'] for a in accounts}
        income_ids = {a['id']: a['name'] for a in income_cats}
        expense_ids = {a['id']: a['name'] for a in expense_cats}
        
        table.setRowCount(len(recent_trans))
        
        for row, t in enumerate(recent_trans):
            if t['expense']:
                cat_name = expense_ids.get(t['category_id'], "Unknown Expense")
            else:
                cat_name = income_ids.get(t['category_id'], "Unknown Income")
            
            values = [
                f"-${t['amount']}" if t['expense'] else f"+${t['amount']}",
                t['date'],
                t['description'],
                cat_name,
                account_ids.get(t['account_id'], "Unknown Account")
            ]
            
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
        
        return table
