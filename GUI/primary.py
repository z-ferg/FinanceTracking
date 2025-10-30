import sys, os
from datetime import datetime
from PySide6 import QtCore, QtWidgets

from add_transaction import AddTransactionWidget
from check_balance import CheckBalanceWidget

from dotenv import load_dotenv, dotenv_values
cur_dir = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(cur_dir)
dotenv_path = os.path.join(par_dir, "sensitive.env")
load_dotenv(dotenv_path)
NAME = os.getenv("NAME")

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.resize(900, 600)
        
        # -- Buttons for Application Navigation --
        btns = []
        self.home_btn = QtWidgets.QPushButton("Home")
        btns.append(self.home_btn)
        self.check_btn = QtWidgets.QPushButton("Check Balances")
        btns.append(self.check_btn)
        self.add_btn = QtWidgets.QPushButton("Add Transaction")
        btns.append(self.add_btn)
        self.bgt_btn = QtWidgets.QPushButton("Budgeting")
        btns.append(self.bgt_btn)
        self.invst_btn = QtWidgets.QPushButton("Investments")
        btns.append(self.invst_btn)
        
        # -- Style the Buttons --
        for btn in btns:
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                    QPushButton {
                        background-color: #5f8a8b;
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #6ea1a2;
                    }
                    QPushButton:pressed {
                        background-color: #4e7a7b;
                    }
            """)
        
        # -- Welcome Box --
        welcome_box = QtWidgets.QFrame()
        welcome_box.setFrameShape(QtWidgets.QFrame.Box)
        welcome_box.setStyleSheet("""
            QFrame {
                background-color: #5f8a8b;
                border: none;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        welcome_layout = QtWidgets.QHBoxLayout()
        welcome_label = QtWidgets.QLabel(f"Welcome, {NAME}")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label)
        welcome_box.setLayout(welcome_layout)

        
        # -- Design the physical layout of the Navigation --
        self.nav_layout = QtWidgets.QVBoxLayout()
        self.nav_layout.addWidget(welcome_box)
        for btn in btns:
            self.nav_layout.addWidget(btn)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.addStretch()
        
        # -- Implement the Navigation Widget --
        nav_widget = QtWidgets.QWidget()
        nav_widget.setStyleSheet("""
            background-color: #7baaba;
        """)
        nav_widget.setLayout(self.nav_layout)
        nav_widget.setFixedWidth(200)
        
        # -- Create the Primary Widget and Add Feature Widgets --
        self.stack = QtWidgets.QStackedWidget()
        self.stack.setStyleSheet("""
            background-color: #808080;
        """)
        self.add_transaction_page = AddTransactionWidget()
        self.check_balance_page = CheckBalanceWidget()
        self.stack.addWidget(self.add_transaction_page)
        self.stack.addWidget(self.check_balance_page)
        
        # -- Design Layout of Entire Window --
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.stack, stretch=1)
        self.setLayout(main_layout)
        
        # -- Add Button Functionality --
        self.add_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.add_transaction_page))
        self.check_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.check_balance_page))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())