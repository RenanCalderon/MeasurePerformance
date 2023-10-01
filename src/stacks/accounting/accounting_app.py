import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QDialogButtonBox, QMainWindow, QGridLayout, QWidget, QDateEdit
from PyQt5.QtCore import Qt, QDate
from db.utilities_db import create_connection
from config import config

host = config["database"]["mysql_host"]
user = config["database"]["mysql_user"]
password = config["database"]["mysql_password"]
database = config["database"]["accounting_database"]


class AddExpenseIncomeDialog(QDialog):
    def __init__(self, is_expense, parent=None):
        super().__init__(parent)
        self.is_expense = is_expense

        layout = QVBoxLayout()

        # Title label
        if is_expense:
            title = "Add Expense"
        else:
            title = "Add Income"

        title_label = QLabel(title)
        layout.addWidget(title_label)

        # Input fields
        label_date = QLabel("Date:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_text_color = "color: black;"
        self.date_edit.setStyleSheet(date_text_color)
        layout.addWidget(label_date)
        layout.addWidget(self.date_edit)

        label_amount = QLabel("Amount:")
        self.amount_edit = QLineEdit()
        layout.addWidget(label_amount)
        layout.addWidget(self.amount_edit)

        label_description = QLabel("Description:")
        self.description_edit = QLineEdit()
        layout.addWidget(label_description)
        layout.addWidget(self.description_edit)

        label_category = QLabel("Category:")
        self.category_edit = QLineEdit()
        layout.addWidget(label_category)
        layout.addWidget(self.category_edit)

        label_accounting_account = QLabel("Accounting Account:")
        self.accounting_account_edit = QLineEdit()
        layout.addWidget(label_accounting_account)
        layout.addWidget(self.accounting_account_edit)

        label_payment_method = QLabel("Payment Method:")
        self.payment_method_edit = QLineEdit()
        layout.addWidget(label_payment_method)
        layout.addWidget(self.payment_method_edit)

        label_currency = QLabel("Currency:")
        self.currency_edit = QLineEdit()
        layout.addWidget(label_currency)
        layout.addWidget(self.currency_edit)

        label_notes = QLabel("Notes:")
        self.notes_edit = QLineEdit()
        layout.addWidget(label_notes)
        layout.addWidget(self.notes_edit)

        # OK and Cancel buttons
        button_box = QDialogButtonBox()
        button_box.setOrientation(Qt.Horizontal)
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.setStyleSheet("""
                            color: #000000;
                            font-size: 14px;
                        """)
        self.cancel_button.setStyleSheet("""
                            color: #000000;
                            font-size: 14px;
                        """)

        button_box.addButton(self.ok_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(self.cancel_button, QDialogButtonBox.RejectRole)
        layout.addWidget(button_box)

        # Input Style
        line_edit_style = "QLineEdit { color: black; }"
        self.description_edit.setStyleSheet(line_edit_style)
        self.amount_edit.setStyleSheet(line_edit_style)
        self.category_edit.setStyleSheet(line_edit_style)
        self.accounting_account_edit.setStyleSheet(line_edit_style)
        self.payment_method_edit.setStyleSheet(line_edit_style)
        self.currency_edit.setStyleSheet(line_edit_style)
        self.notes_edit.setStyleSheet(line_edit_style)

        self.setLayout(layout)
        self.setWindowTitle(title)

        # Connect buttons to slots
        self.ok_button.clicked.connect(self.insert_record)
        self.cancel_button.clicked.connect(self.reject)

    def insert_record(self):
        try:
            # Establish the connection to the database using the configuration from config.py
            connection = create_connection(host, user, password, database)
            cursor = connection.cursor()

            # Determine the destination table based on whether it's an expense or income
            if self.is_expense:
                table_name = "expenses"
            else:
                table_name = "income"

            # Retrieve the values entered into dialog
            date = self.date_edit.date().toString("yyyy-MM-dd")
            description = self.description_edit.text()
            amount = self.amount_edit.text()
            category = self.category_edit.text()
            accounting_account = self.accounting_account_edit.text()
            payment_method = self.payment_method_edit.text()
            currency = self.currency_edit.text()
            notes = self.notes_edit.text()
            # Insert query with updated column names
            insert_query = f"""
                INSERT INTO {table_name} (date, amount, description, category, accounting_account, 
                                          payment_method, currency, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Values to insert
            values = (date, amount, description, category, accounting_account,
                      payment_method, currency, notes)

            # Execute the insertion
            cursor.execute(insert_query, values)

            # Commit the insertion to the database
            connection.commit()

            # Close the connection
            cursor.close()
            connection.close()

            # Close the dialog
            self.accept()

        except Exception as e:
            print("Error inserting record:", str(e))


class AccountingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.setWindowTitle("Accounting App")
        self.setGeometry(100, 100, 400, 300)

        # Buttons for expenses and income
        btn_expenses = QPushButton("Expenses", self)
        btn_expenses.clicked.connect(self.open_expenses_dialog)
        btn_expenses.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        btn_income = QPushButton("Income", self)
        btn_income.clicked.connect(self.open_income_dialog)
        btn_income.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Window layout
        layout = QGridLayout()
        layout.addWidget(btn_expenses, 0, 0)
        layout.addWidget(btn_income, 0, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_expenses_dialog(self):
        # Open the expenses dialog
        add_expense_dialog = AddExpenseIncomeDialog(is_expense=True, parent=self)
        add_expense_dialog.exec_()

    def open_income_dialog(self):
        # Open the income dialog
        add_income_dialog = AddExpenseIncomeDialog(is_expense=False, parent=self)
        add_income_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    accounting_app = AccountingWindow()
    accounting_app.show()
    sys.exit(app.exec_())

