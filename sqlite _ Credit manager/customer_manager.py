from datetime import datetime
from db_utility import DBUtility as db
import sqlite3
class Customer:
    def __init__(self, customer_fname,customer_lname,customer_mname=None, address=None, phone_number=None, email=None, promised_date=None):
        self.customer_fname = customer_fname
        self.customer_lname = customer_lname
        self.customer_mname =customer_mname
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.promised_date = promised_date
        self.create_table()
        self.customer_id = self.generate_customer_id()
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.validate_customer_name()  # Automatic validation during initialization

    def create_table(self):
        '''
        Create the Customers table in the database if it doesn't already exist.
        '''
        schema = '''
            customer_id TEXT PRIMARY KEY,
            customer_fname TEXT NOT NULL CHECK(LENGTH(customer_fname) >= 2 AND LENGTH(customer_fname) <= 10),
            customer_lname TEXT NOT NULL CHECK(LENGTH(customer_lname) >= 2 AND LENGTH(customer_lname) <= 10),
            customer_mname TEXT CHECK(LENGTH(customer_mname) <= 3),
            address TEXT CHECK(LENGTH(address) <= 100),
            phone_number TEXT UNIQUE CHECK(LENGTH(phone_number) <= 15),
            email TEXT UNIQUE CHECK(email LIKE '%@%.%' AND LENGTH(email) <= 254),
            promised_date DATE,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        '''
        db.create_table("Customers", schema)

    def generate_customer_id(self):
        '''
        Generate a unique customer ID based on the current date and a sequential number.
        '''
        current_date = datetime.now().strftime("%Y%m%d")
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id LIKE ?", (f"{current_date}%",))
                sequence = cursor.fetchone()[0] + 1
                return f"{current_date}{sequence:02d}"
        except sqlite3.Error as e:
            print(f"Error generating customer ID: {e}")
            return None

    def validate_customer_name(self):
        '''
        Check if the customer name is unique in the database. Raise a ValueError if it already exists.
        '''
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = """
                        SELECT customer_id 
                        FROM Customers 
                        WHERE customer_fname = ? AND customer_lname = ? AND customer_mname = ?

                        """
                cursor.execute(query, (self.customer_fname, self.customer_lname, self.customer_mname))
                result = cursor.fetchone()
                if result:
                    raise ValueError(
                        f"Customer name '{self.customer_fname, self.customer_lname, self.customer_mname}' already exists. Please use a unique name.")
        except sqlite3.Error as e:
            print(f"Error validating customer name: {e}")
            raise

    def save_record(self):
        '''
        Save the customer's details in the database.
        '''
        try:
            columns = "customer_id, customer_fname, customer_lname, customer_mname, address, phone_number, email, promised_date, date_created"
            values = (self.customer_id, self.customer_fname, self.customer_lname, self.customer_mname, self.address, self.phone_number, self.email, self.promised_date, self.date_created)
            db.save_record("Customers", columns, values)
        except sqlite3.Error as e:
            print(f"Error saving record to table 'Customers': {e}")
            
    @staticmethod
    def count_members():
        # Count the total number of customers in the database
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM Customers")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error counting customers: {e}")
            return 0        
    @staticmethod
    def update_customer_details(customer_id, **kwargs):
        """
        Update customer details dynamically.

        Parameters:
        - customer_id: The ID of the customer to update.
        - kwargs: Key-value pairs of columns and their new values (e.g., address="New Address").
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                updates = ", ".join([f"{key} = ?" for key in kwargs.keys()])
                query = f"UPDATE Customers SET {updates} WHERE customer_id = ?"
                cursor.execute(query, (*kwargs.values(), customer_id))
        except sqlite3.Error as e:
            print(f"Error updating customer details: {e}")


# Test Code
if __name__ == "__main__":

    customer1 = Customer("John","Doe", address="123 Test St", phone_number="1234567890", email="john@example.com")
    customer1.save_record()


    
    Customer.update_customer_details(customer1.customer_id, address="456 New St", phone_number="9876543210")
    print(f"Customer '{customer1.customer_fname}' updated successfully!")
    
    try:
        customer = Customer("Alice",'Phiri',customer_mname= 'j.k', address="123 Main St", phone_number="1234567891", email="alice@example.com")
        customer.save_record()
    except ValueError as ve:
        print(f"Validation Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print(f"Total Customer:{Customer.count_members()}")
