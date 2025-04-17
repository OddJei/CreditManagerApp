import sqlite3
from db_utility import DBUtility as db
from check_payment import CheckPayment

class Display:
    @staticmethod
    def get_credit_info(customer_id):
        """
        Fetch total credited amount and dates for a specific customer.

        Parameters:
        - customer_id: The ID of the customer.

        Returns:
        - A tuple (dates_credited, total_credited).
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT date_credited, amount_credited
                    FROM Credits
                    WHERE customer_id = ?
                '''
                cursor.execute(query, (customer_id,))
                records = cursor.fetchall()

                dates_credited = [record[0] for record in records]
                total_credited = sum(record[1] for record in records)
                return (",".join(dates_credited), total_credited)
        except sqlite3.Error as e:
            print(f"Error fetching credit info for customer {customer_id}: {e}")
            return ("", 0)

    @staticmethod
    def get_pay_info(customer_id):
        """
        Fetch total paid amount and dates for a specific customer.

        Parameters:
        - customer_id: The ID of the customer.

        Returns:
        - A tuple (dates_paid, total_paid).
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT date_paid, amount_paid
                    FROM PayCredits
                    WHERE customer_id = ?
                '''
                cursor.execute(query, (customer_id,))
                records = cursor.fetchall()

                dates_paid = [record[0] for record in records]
                total_paid = sum(record[1] for record in records)
                return (",".join(dates_paid), total_paid)
        except sqlite3.Error as e:
            print(f"Error fetching payment info for customer {customer_id}: {e}")
            return ("", 0)

    @staticmethod
    def get_customer_id_by_name(fname, lname, mname=None):
        """
        Fetch customer IDs matching a given names.

        Parameters:
        - name_to_search: The names of the customer.

        Returns:
        - A list of customer IDs matching the names.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                            SELECT customer_id
                            FROM Customers
                            WHERE customer_fname = ? AND customer_lname = ? OR customer_mname IS NULL = ?
                        '''
                cursor.execute(query, (fname, lname, mname,))
                return [record[0] for record in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching customer ID by name {fname, lname, mname}: {e}")
            return []

    @staticmethod
    def get_not_paid_customers():
        """
        Fetch customers who have credits but no payments.

        Returns:
        - A list of customer IDs.
        """
        return CheckPayment.find_not_paid_customers()

    @staticmethod
    def display_records(customers):
        """
        Display records for a given list of customers.

        Parameters:
        - customers: List of tuples containing (customer_id, customer_name).
        """
        if not customers:
            print("No matching records found.")
            return

        print("Customer ID | Customer Name | Date Credited | Amount Credited | Date Paid | Amount Paid | Pending Amount")
        print("-" * 100)

        for customer_id, customer_name in customers:
            credited_info = Display.get_credit_info(customer_id)
            paid_info = Display.get_pay_info(customer_id)
            pending_amount = CheckPayment.find_pending_amount(customer_id)
            print(f'{customer_id} | {customer_name} | {credited_info[0]} | {credited_info[1]:.2f} | {paid_info[0]} | {paid_info[1]:.2f} | {pending_amount:.2f}')

    @staticmethod
    def display_all_records():
        """
        Display all customer records.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT *
                    FROM Customers
                '''
                cursor.execute(query)
                customers = cursor.fetchall()
                Display.display_records(customers)
        except sqlite3.Error as e:
            print(f"Error displaying all records: {e}")

    @staticmethod
    def display_paid_records():
        """
        Display records of customers who have made payments.
        """
        try:
            paid_customers = CheckPayment.find_not_paid_customers()
            Display.display_records(paid_customers)
        except Exception as e:
            print(f"Error displaying paid records: {e}")

    @staticmethod
    def display_not_paid_customers():
        """
        Display records of customers who have credits but no payments.
        """
        try:
            not_paid_customers = Display.get_not_paid_customers()
            Display.display_records(not_paid_customers)
        except Exception as e:
            print(f"Error displaying not-paid customers: {e}")

if __name__ == "__main__":
    '''
    
    try:
        # Example: Display all records
        Display.display_all_records()

        # Example: Display paid customers
        Display.display_paid_records()

        # Example: Display not paid customers
        Display.display_not_paid_customers()

        # Test displaying records
        customers = [("2025040301", "John Doe"), ("2025040302", "Jane Smith")]
        Display.display_records(customers)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    '''    
    print (Display.get_customer_id_by_name( 'John' ,'Doe' ))