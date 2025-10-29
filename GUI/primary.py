import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets

from add_transaction import AddTransactionWidget
from check_balance import CheckBalanceWidget

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.resize(900, 600)
        
        self.add_btn = QtWidgets.QPushButton("Add Transaction")
        self.check_btn = QtWidgets.QPushButton("Check Balances")
        
        self.nav_layout = QtWidgets.QVBoxLayout()
        self.nav_layout.addWidget(self.add_btn)
        self.nav_layout.addWidget(self.check_btn)
        self.nav_layout.addStretch()
        
        nav_widget = QtWidgets.QWidget()
        nav_widget.setStyleSheet("background-color: #7baaba;")
        nav_widget.setLayout(self.nav_layout)
        nav_widget.setFixedWidth(200)
        
        self.stack = QtWidgets.QStackedWidget()
        self.stack.setStyleSheet("background-color: #8d9091;")
        self.add_transaction_page = AddTransactionWidget()
        self.check_balance_page = CheckBalanceWidget()
        self.stack.addWidget(self.add_transaction_page)
        self.stack.addWidget(self.check_balance_page)
        
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.stack, stretch=1)
        self.setLayout(main_layout)
        
        self.add_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.add_transaction_page))
        self.check_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.check_balance_page))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())