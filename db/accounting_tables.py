import logging
from utilities_db import create_connection, create_database
from config import config

LOG = logging.getLogger()


def create_accounting_tables(environment):
    if not environment:
        print("Please enter the database name: ")
        return

    database_name = "accounting_" + environment

    try:

        # Create database
        create_database(host, user, password, database_name)

        # Connect to the database
        connection = create_connection(host, user, password, database_name)

        # Create Expenses Dimension Table
        create_expenses_table_query = """
            CREATE TABLE IF NOT EXISTS Expenses (
                expense_id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                amount DECIMAL(10, 2),
                description VARCHAR(255),
                category VARCHAR(50),
                accounting_account VARCHAR(100),
                payment_method VARCHAR(20),
                currency VARCHAR(10),
                notes VARCHAR(255)
            )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_expenses_table_query)

        # Create Income Dimension Table
        create_income_table_query = """
            CREATE TABLE IF NOT EXISTS income (
                income_id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                amount DECIMAL(10, 2),
                description VARCHAR(255),
                category VARCHAR(50),
                accounting_account VARCHAR(100),
                payment_method VARCHAR(20),
                currency VARCHAR(10),
                notes VARCHAR(255)
            )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_income_table_query)

        # Create a view to calculate profits
        create_profit_view_query = """
            CREATE OR REPLACE VIEW profit AS
            SELECT 
                date,
                COALESCE(SUM(income_amount), 0) AS total_income,
                COALESCE(SUM(expense_amount), 0) AS total_expenses,
                COALESCE(SUM(income_amount), 0) - COALESCE(SUM(expense_amount), 0) AS profit
            FROM (
                SELECT
                    date,
                    amount AS income_amount,
                    NULL AS expense_amount
                FROM income
                UNION ALL
                SELECT
                    date,
                    NULL AS income_amount,
                    amount AS expense_amount
                FROM expenses
            ) subquery
            GROUP BY date
            ORDER BY date;
        """
        with connection.cursor() as cursor:
            cursor.execute(create_profit_view_query)

        connection.close()
        print("Tables and procedures created successfully.")
    except Exception as e:
        LOG.error("An error occurred:", exc_info=True)
        print("Error creating tables and procedures:", str(e))


if __name__ == "__main__":
    host = config["database"]["mysql_host"]
    user = config["database"]["mysql_user"]
    password = config["database"]["mysql_password"]
    environment = input("Enter the environment name: ")
    create_accounting_tables(environment)
