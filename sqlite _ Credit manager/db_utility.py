import sqlite3

class DBUtility:
    DB_NAME = "CreditManager.db"

    @staticmethod
    def create_table(table_name, schema):
        """
        Create a table in the database if it doesn't exist.

        Parameters:
        - table_name: Name of the table to create.
        - schema: SQL schema defining the table structure.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
                cursor.execute(query)
                print(f"Table '{table_name}' ensured in the database.")
        except sqlite3.Error as e:
            print(f"Error creating table '{table_name}': {e}")

    @staticmethod
    def save_record(table_name, columns, values):
        """
        Save a record to the specified table.

        Parameters:
        - table_name: Name of the table to insert the record.
        - columns: Comma-separated string of column names.
        - values: Tuple of values to insert.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                placeholders = ", ".join(["?" for _ in values])
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                connection.commit()
                print(f"Record inserted into table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error saving record to table '{table_name}': {e}")

    @staticmethod
    def fetch_total(column, table_name, condition=None):
        """
        Fetch the total of a specific column from a table.

        Parameters:
        - column: Name of the column to sum.
        - table_name: Name of the table to query.
        - condition: SQL condition to filter rows (optional).

        Returns:
        - Total sum as a float, or 0 if no rows match or error occurs.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                query = f"SELECT SUM({column}) FROM {table_name}"
                if condition:
                    query += f" WHERE {condition}"
                cursor.execute(query)
                total = cursor.fetchone()[0]
                return total if total is not None else 0.0
        except sqlite3.Error as e:
            print(f"Error fetching total from table '{table_name}': {e}")
            return 0.0

    @staticmethod
    def fetch_unique_values(column, table_name):
        """
        Fetch unique values of a column from a table.

        Parameters:
        - column: Column name to retrieve distinct values.
        - table_name: Name of the table to query.

        Returns:
        - List of unique values, or an empty list if error occurs.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                query = f"SELECT DISTINCT {column} FROM {table_name}"
                cursor.execute(query)
                results = cursor.fetchall()
                return [result[0] for result in results]
        except sqlite3.Error as e:
            print(f"Error fetching unique values from table '{table_name}': {e}")
            return []

    @staticmethod
    def execute_query(query, params=None):
        """
        Execute a custom SQL query.

        Parameters:
        - query: The SQL query to execute.
        - params: A tuple of parameters for the query (optional).

        Returns:
        - The result of the query if it fetches data, otherwise None.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                else:
                    connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        

    @staticmethod
    def fetch_customer_data(customer_id=None, customer_name=None, attributes=None):
        """
        Fetch customer-related data from all tables based on customer_id or customer_name.

        Parameters:
        - customer_id: The customer ID to filter records.
        - customer_name: The customer name to filter records.
        - attributes: A list of attributes (columns) to retrieve. Defaults to all attributes.

        Returns:
        - A dictionary containing data from 'Customers', 'Credits', and 'PayCredits'.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                
                # Determine filtering condition
                condition = ""
                params = ()
                if customer_id:
                    condition = "customer_id = ?"
                    params = (customer_id,)
                elif customer_name:
                    condition = "customer_name = ?"
                    params = (customer_name,)
                else:
                    raise ValueError("Either customer_id or customer_name must be provided.")

                # Fetch customer data
                if not attributes:
                    attributes = "*"
                else:
                    attributes = ", ".join(attributes)
                
                result = {}

                # Query Customers table
                query_customers = f"SELECT {attributes} FROM Customers WHERE {condition}"
                cursor.execute(query_customers, params)
                result["Customers"] = cursor.fetchall()

                # Query Credits table
                query_credits = f"SELECT {attributes} FROM Credits WHERE {condition}"
                cursor.execute(query_credits, params)
                result["Credits"] = cursor.fetchall()

                # Query PayCredits table
                query_pay_credits = f"SELECT {attributes} FROM PayCredits WHERE {condition}"
                cursor.execute(query_pay_credits, params)
                result["PayCredits"] = cursor.fetchall()

                return result
        except sqlite3.Error as e:
            print(f"Error fetching customer data: {e}")
            return {}
        except ValueError as ve:
            print(ve)
            return {}

    @staticmethod
    def fetch_all_runbal_customer():
        """
        Fetches all customers with a positive run balance (pending amount > 0).

        Uses a SQL query with LEFT JOINs:
        - Joins 'Customers' with 'Credits' to calculate total credited.
        - Joins 'Customers' with 'PayCredits' to calculate total paid.
        - Computes pending amount as (total credited - total paid).
        Only customers where the pending amount is greater than 0 are returned.
        
        Returns:
        - A list of tuples containing customer data along with total_credit, total_payments, and pending_amount.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                query = """
                SELECT 
                    c.*,
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
                ) pc ON c.customer_id = pc.customer_id
                WHERE (COALESCE(cr.total_credit, 0) - COALESCE(pc.total_payments, 0)) > 0;
                """
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except sqlite3.Error as e:
            print(f"Error fetching run balance customers: {e}")
            return []



    @staticmethod
    def fetch_all_paid_customer():
        """
        Fetches all customers with a run balance 0 (pending amount == 0).

        Uses a SQL query with LEFT JOINs:
        - Joins 'Customers' with 'Credits' to calculate total credited.
        - Joins 'Customers' with 'PayCredits' to calculate total paid.
        - Computes pending amount as (total credited - total paid).
        Only customers where the pending amount is greater  0 are returned.
        
        Returns:
        - A list of tuples containing customer data along with total_credit, total_payments, and pending_amount.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                query = """
                SELECT 
                    c.*,
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
                ) pc ON c.customer_id = pc.customer_id
                WHERE (COALESCE(cr.total_credit, 0) - COALESCE(pc.total_payments, 0)) = 0;
                """
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except sqlite3.Error as e:
            print(f"Error fetching run balance customers: {e}")
            return []

    @staticmethod
    def fetch_customer_id(fname=None, lname=None, phone=None, email=None):
        """
        Fetch a customer's ID based on provided name, phone number, or email.

        Parameters:
        - fname (str): First name of the customer (optional)
        - lname (str): Last name of the customer (optional)
        - phone (str): Phone number of the customer (optional)
        - email (str): Email address of the customer (optional)

        Returns:
        - Customer ID if found (unique match), else raises an error with a tip.
        """
        query = "SELECT DISTINCT customer_id FROM customers WHERE "
        conditions = []
        params = []

        # Add filtering conditions dynamically
        if fname:
            conditions.append("customer_fName = ?")
            params.append(fname)
        if lname:
            conditions.append("customer_lname = ?")
            params.append(lname)
        if phone:
            conditions.append("phone_number = ?")
            params.append(phone)
        if email:
            conditions.append("email = ?")
            params.append(email)

        # Ensure at least one condition exists
        if not conditions:
            raise ValueError("At least one search parameter (name, phone, or email) must be provided.")

        query += " AND ".join(conditions)  # Build the WHERE clause dynamically

        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()  # Fetch all matching records
                
                # Handle multiple results
                if len(results) == 0:
                    return None  
                elif len(results) == 1:
                    return results[0][0] 
                else:
                    # Raise an error for multiple matches
                    raise ValueError(
                        f"Multiple matches found ({len(results)}). Please refine your search "
                        f"criteria by specifying at least two fields (e.g., First Name and Last Name)."
                    )
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        
    @staticmethod
    def clear_all_rows():
        """
        Deletes all rows from every table in the database.

        Use with caution, as this will permanently remove all data.
        """
        try:
            with sqlite3.connect(DBUtility.DB_NAME) as connection:
                cursor = connection.cursor()

                # Retrieve the list of all tables in the database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                # Iterate over each table and delete all rows
                for table in tables:
                    table_name = table[0]  # Extract table name from the tuple
                    cursor.execute(f"DELETE FROM {table_name};")  # Delete all rows from the table
                    cursor.execute(f"VACUUM;")  # Optional: Reclaim unused space
                    print(f"Cleared all rows from table: {table_name}")

                connection.commit()
                print("All rows cleared successfully!")

        except sqlite3.Error as e:
            print(f"An error occurred while clearing the database: {e}")



# Test Code
if __name__ == "__main__":
    
    DBUtility.create_table("TestTable", "id INTEGER PRIMARY KEY, name TEXT")
    DBUtility.save_record("TestTable", "id, name", (1, "TestUser"))
    total = DBUtility.fetch_total("id", "TestTable")
    print(f"Total fetched: {total}")
    unique_values = DBUtility.fetch_unique_values("name", "TestTable")
    print(f"Unique values fetched: {unique_values}")
    
    print (DBUtility.fetch_all_runbal_customer())

    

    
