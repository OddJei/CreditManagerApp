import sqlite3
from customer_manager import Customer
from credit_manager import Credit
from pay_credit import PayCredit
from check_payment import CheckPayment
from display import Display
from db_utility import DBUtility as db

class MainLogic:
    '''
        this is the first six set of method from the customer manager 
        '''
    @staticmethod
    def add_customer(customer_fname,
                     customer_lname,
                     customer_mname= None,
                     amount_credited=None,
                     address=None,
                     phone=None,
                     email=None,
                     promised_date=None):
        """
        Adds a new customer to the database and assigns initial credit.
        """
        try:
            customer = Customer(customer_fname, customer_lname, customer_mname=customer_mname, address=address, phone_number=phone, email=email, promised_date=promised_date)
            customer.save_record()

            if amount_credited > 0:
                credit = Credit(customer.customer_id, amount_credited)
                credit.save_record()

            return f"Customer '{customer_fname, customer_lname ,customer_mname}' successfully added with initial credit of {amount_credited:.2f}."
        except Exception as e:
            return f"Error adding customer: {str(e)}"
                
    @staticmethod
    def fetch_all_customers():
        """
        Retrieves all customers from the database.
        """
        try:
            return Display.display_all_records()  
        except Exception as e:
            return f"Error fetching customer records: {str(e)}"
        
    @staticmethod
    def fetch_customer_summary(customer_id):
        """
        Fetches the detailed summary of a customer, including credits, payments, and pending amounts.
        """
        try:
            summary = CheckPayment.get_customer_history(customer_id)
            pending_amount = CheckPayment.find_pending_amount(customer_id)
            summary["pending_amount"] = pending_amount 
            return summary
        except Exception as e:
            return f"Error fetching summary for customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def update_customer_details(customer_id, **kwargs):
        """
        Updates an existing customer's details in the database.
        """
        try:
            Customer.update_customer_details(customer_id, **kwargs)
            return f"Customer ID '{customer_id}' updated successfully."
        except Exception as e:
            return f"Error updating customer: {str(e)}"

    @staticmethod
    def remove_customer(customer_id):
        """
        Removes a customer and their associated records from the database.
        """
        try:
            query = "DELETE FROM Customers WHERE customer_id = ?"
            db.execute_query(query, (customer_id,))
            return f"Customer ID '{customer_id}' removed successfully."
        except Exception as e:
            return f"Error removing customer: {str(e)}"
        
    @staticmethod
    def fetch_customer_by_name(fname, lname, mname):
        """
        Fetches customer details by name for search functionality.
        """
        try:
            return Display.get_customer_id_by_name(fname, lname, mname)
        except Exception as e:
            return f"Error fetching customer by name '{fname, lname, mname}': {str(e)}"
        

    '''
    Set 2: Handling Credits and Payments
    '''


    @staticmethod
    def add_credit_to_customer(customer_id, amount_credited, date_credited=None):
        """
        Adds a credit record to an existing customer.
        """
        try:
            credit = Credit(customer_id, amount_credited, date_credited=date_credited)
            credit.save_record()
            return f"Credit of {amount_credited:.2f} added successfully to Customer ID '{customer_id}'."
        except Exception as e:
            return f"Error adding credit to customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def add_payment_to_customer(customer_id, amount_paid, date_paid=None):
        """
        Adds a payment record to an existing customer.
        """
        try:
            payment = PayCredit(customer_id, amount_paid, date_paid=date_paid)
            payment.save_record()
            return f"Payment of {amount_paid:.2f} added successfully to Customer ID '{customer_id}'."
        except Exception as e:
            return f"Error adding payment to customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def fetch_pending_amount(customer_id):
        """
        Retrieves the pending amount for a specific customer.
        """
        try:
            pending_amount = CheckPayment.find_pending_amount(customer_id)
            return f"Pending amount for Customer ID '{customer_id}' is {pending_amount:.2f}."
        except Exception as e:
            return f"Error fetching pending amount for customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def fetch_payment_history(customer_id):
        """
        Fetches the payment history of a specific customer.
        """
        try:
            history = CheckPayment.get_customer_history(customer_id)
            return history.get("payments", [])
        except Exception as e:
            return f"Error fetching payment history for customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def fetch_credit_history(customer_id):
        """
        Fetches the credit history of a specific customer.
        """
        try:
            history = CheckPayment.get_customer_history(customer_id)
            return history.get("credits", [])
        except Exception as e:
            return f"Error fetching credit history for customer ID '{customer_id}': {str(e)}"

    @staticmethod
    def fetch_unpaid_customers():
        """
        Returns:
        - A list of tuples containing customer data along with total_credit, total_payments, and pending_amount.
        """
        try:
            unpaid_customers = db.fetch_all_runbal_customer()
            return unpaid_customers
        except Exception as e:
            return f"Error fetching unpaid customers: {str(e)}"
        


    """
    Set 3: Display and Record Management
    """

    @staticmethod
    def fetch_all_customer_data():
        """
            Fetches all records from the Customers, Credits, and PayCredits tables, joined by customer_id.
            
            Returns:
            - A list of dictionaries, where each dictionary contains combined data from all three tables.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = """
                    SELECT 
                        c.customer_id, 
                        c.customer_fname, 
                        c.customer_lname, 
                        c.customer_mname, 
                        c.address, 
                        c.phone_number, 
                        c.email, 
                        c.promised_date, 
                        c.date_created,
                        COALESCE(cr.total_credit, 0) AS total_credit,
                        COALESCE(pc.total_payments, 0) AS total_payments,
                        (COALESCE(cr.total_credit, 0) - COALESCE(pc.total_payments, 0)) AS pending_amount
                    FROM Customers c
                    LEFT JOIN (
                        SELECT customer_id, SUM(amount_credited) AS total_credit
                        FROM Credits
                        GROUP BY customer_id
                    ) cr ON c.customer_id = cr.customer_id
                    LEFT JOIN (
                        SELECT customer_id, SUM(amount_paid) AS total_payments
                        FROM PayCredits
                        GROUP BY customer_id
                    ) pc ON c.customer_id = pc.customer_id;
                """
                cursor.execute(query)
                results = cursor.fetchall()

                # Convert to a list of dictionaries for better usability
                column_names = [description[0] for description in cursor.description]
                records = [dict(zip(column_names, row)) for row in results]

                return records
        except sqlite3.Error as e:
            print(f"Error fetching all customer data: {e}")
            return []
    
        
    @staticmethod
    def get_customer_summary_by_name(customer_name):
        """
        Fetches a detailed summary for a customer using their name.
        """
        try:
            customer_ids = Display.get_customer_id_by_name(customer_name)
            if not customer_ids:
                return f"No customer found with name '{customer_name}'."
            
            summaries = []
            for customer_id in customer_ids:
                summary = MainLogic.fetch_customer_summary(customer_id)
                summaries.append(summary)
            
            return summaries
        except Exception as e:
            return f"Error fetching summary for customer name '{customer_name}': {str(e)}"
        
        
    @staticmethod
    def fetch_paid_customers():
        """
        Fetches records of customers who have made payments.
        """
        try:
            paid_customers = db.fetch_all_paid_customer()
            return paid_customers
        except Exception as e:
            return f"Error fetching paid customers: {str(e)}"
        
    @staticmethod
    def get_payment_info_for_display(customer_id):
        """
        Fetches total paid amount and payment dates for display.
        """
        try:
            payment_info = Display.get_pay_info(customer_id)
            return payment_info
        except Exception as e:
            return f"Error fetching payment info for customer ID '{customer_id}': {str(e)}"
        


    """
    Set 4: Query and Filtering Features
    """

    @staticmethod
    def get_dashboard_summary():
        """
        Provides a summary for the dashboard, including totals for credits, payments, and pending amounts.
        """
        try:
            total_customers = Customer.count_members()
            total_credited = Credit.sum_amount_credited()
            total_paid = PayCredit.sum_amount_paid()
            total_pending = total_credited - total_paid

            return {
                "total_Customers": total_customers,
                "total_credited": total_credited,
                "total_paid": total_paid,
                "total_pending": total_pending,
            }
        except Exception as e:
            return f"Error generating dashboard summary: {str(e)}"

    @staticmethod
    def fetch_customer_id(fname, lname, phone, email):
        """
        Retrieves  customer IDs.
        """
        try:
            customer_id = db.fetch_customer_id(fname=fname, lname=lname, phone=phone, email=email)
            return customer_id
        except Exception as e:
            return f"Error fetching customer IDs: {str(e)}"

    @staticmethod
    def fetch_total_paid(customer_id=None):
        """
        Calculates the total paid amount.
        If `customer_id` is provided, fetches the total paid for the specific customer.
        """
        try:
            if customer_id:
                total_paid = db.fetch_total("amount_paid", "PayCredits", f"customer_id = '{customer_id}'")
                return f"Total paid for Customer ID '{customer_id}': {total_paid:.2f}."
            else:
                total_paid = PayCredit.sum_amount_paid()
                return f"Total paid across all customers: {total_paid:.2f}."
        except Exception as e:
            return f"Error fetching total paid: {str(e)}"

    @staticmethod
    def fetch_total_credited(customer_id=None):
        """
        Calculates the total credited amount.
        If `customer_id` is provided, fetches the total credited for the specific customer.
        """
        try:
            if customer_id:
                total_credited = db.fetch_total("amount_credited", "Credits", f"customer_id = '{customer_id}'")
                return f"Total credited for Customer ID '{customer_id}': {total_credited:.2f}."
            else:
                total_credited = Credit.sum_amount_credited()
                return f"Total credited across all customers: {total_credited:.2f}."
        except Exception as e:
            return f"Error fetching total credited: {str(e)}"

    @staticmethod
    def filter_payments_by_date(start_date, end_date):
        """
        Filters payment records within a specific date range.
        """
        try:
            payments = PayCredit.filter_payments_by_date(start_date, end_date)
            return payments
        except Exception as e:
            return f"Error filtering payments by date range ({start_date} to {end_date}): {str(e)}"

    @staticmethod
    def filter_credits_by_date(start_date, end_date):
        """
        Filters credit records within a specific date range.
        """
        try:
            credits = Credit.filter_credits_by_date(start_date, end_date)
            return credits
        except Exception as e:
            return f"Error filtering credits by date range ({start_date} to {end_date}): {str(e)}"
        


    """
    Set 5: Utilities and Extras
    """
            
    @staticmethod
    def bulk_add_customers(customers):
        """
        Adds multiple customers to the database.

        Parameters:
        - customers: List of dictionaries, where each dictionary contains customer details.
        """
        try:
            for customer_data in customers:
                MainLogic.add_customer(
                    customer_name=customer_data.get("customer_name"),
                    amount_credited=customer_data.get("amount_credited", 0.0),
                    address=customer_data.get("address"),
                    phone=customer_data.get("phone"),
                    email=customer_data.get("email"),
                    promised_date=customer_data.get("promised_date")
                )
            return "Bulk customer addition completed successfully."
        except Exception as e:
            return f"Error in bulk customer addition: {str(e)}"

    @staticmethod
    def bulk_add_credits(credits):
        """
        Adds multiple credit records for different customers.

        Parameters:
        - credits: List of dictionaries, where each dictionary contains credit details.
        """
        try:
            for credit_data in credits:
                MainLogic.add_credit_to_customer(
                    customer_id=credit_data.get("customer_id"),
                    amount_credited=credit_data.get("amount_credited"),
                    date_credited=credit_data.get("date_credited")
                )
            return "Bulk credit addition completed successfully."
        except Exception as e:
            return f"Error in bulk credit addition: {str(e)}"

    @staticmethod
    def bulk_add_payments(payments):
        """
        Adds multiple payment records for different customers.

        Parameters:
        - payments: List of dictionaries, where each dictionary contains payment details.
        """
        try:
            for payment_data in payments:
                MainLogic.add_payment_to_customer(
                    customer_id=payment_data.get("customer_id"),
                    amount_paid=payment_data.get("amount_paid"),
                    date_paid=payment_data.get("date_paid")
                )
            return "Bulk payment addition completed successfully."
        except Exception as e:
            return f"Error in bulk payment addition: {str(e)}"

    @staticmethod
    def fetch_customer_data_by_criteria(**criteria):
        """
        Fetches customer data based on specific criteria.

        Parameters:
        - criteria: Key-value pairs for filtering customers (e.g., email="john@example.com").

        Returns:
        - List of matching customers or an appropriate error message.
        """
        try:
            condition = " AND ".join([f"{key} = '{value}'" for key, value in criteria.items()])
            query = f"SELECT * FROM Customers WHERE {condition}"
            results = db.execute_query(query)
            return results if results else "No matching customers found."
        except Exception as e:
            return f"Error fetching customer data by criteria: {str(e)}"

    @staticmethod
    def generate_report():
        """
        Generates a report summarizing credits, payments, and pending amounts for all customers.
        """
        try:
            all_records = MainLogic.fetch_all_records()
            report = {
                "total_customers": len(all_records),
                "total_credited": Credit.sum_amount_credited(),
                "total_paid": PayCredit.sum_amount_paid(),
                "total_pending": Credit.sum_amount_credited() - PayCredit.sum_amount_paid(),
            }
            return report
        except Exception as e:
            return f"Error generating report: {str(e)}"
    @staticmethod
    def reset_database():
        """
        Resets the database by clearing all records from all tables.
        """
        try:
            tables = ["Customers", "Credits", "PayCredits"]
            for table in tables:
                query = f"DELETE FROM {table}"
                db.execute_query(query)
            return "Database reset successfully."
        except Exception as e:
            return f"Error resetting database: {str(e)}"
        

    def fetch_raw_data(customer_id):
        try:
            with sqlite3.connect("CreditManager.db") as connection:
                cursor = connection.cursor()

                # Fetch customer details
                customer_query = "SELECT * FROM Customers WHERE customer_id = ?"
                cursor.execute(customer_query, (customer_id,))
                customer_data = cursor.fetchone()  # Single row

                # Fetch credit details
                credit_query = "SELECT * FROM Credits WHERE customer_id = ?"
                cursor.execute(credit_query, (customer_id,))
                credit_data = cursor.fetchall()  # All rows

                # Fetch payment (paycredit) details
                paycredit_query = "SELECT * FROM PayCredits WHERE customer_id = ?"
                cursor.execute(paycredit_query, (customer_id,))
                paycredit_data = cursor.fetchall()  # All rows

                return customer_data, credit_data, paycredit_data

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None, None, None

