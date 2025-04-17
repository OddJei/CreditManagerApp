import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from mainlogic import MainLogic

class ViewTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_view_tab()


    def create_view_tab(self):
        # Treeview for data display
        self.tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "FName", "LName", "MName", "Credit", "Paid", "Pending"), 
            show='headings'
        )

        self.tree.column("ID", width=100)
        self.tree.heading("ID", text="Customer ID", )
        
        self.tree.column("FName", width=150)
        self.tree.heading("FName", text="First Name")

        self.tree.column("LName", width=150)
        self.tree.heading("LName", text="Last Name")

        self.tree.column("MName", width=100)
        self.tree.heading("MName", text="Initials")

        self.tree.column("Credit", width=120)
        self.tree.heading("Credit", text="Total Credit")

        self.tree.column("Paid", width=120)
        self.tree.heading("Paid", text="Total Paid")

        self.tree.column("Pending", width=120)
        self.tree.heading("Pending", text="Pending Amount")
        self.tree.pack(expand=True, fill='both')


        # Create a vertical scrollbar
        scrollbar_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Refresh button
        tk.Button(self.frame, text="Summery view all", command=self.load_data, cursor= 'hand2', bg= 'lime green', fg= 'white').pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame, text="summery view not paid customers ", command=self.load_unpaid_data, cursor= 'hand2', bg= 'lime green', fg= 'white').pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame, text="summery view paid customers", command=self.load_paid_data, cursor= 'hand2', bg= 'lime green', fg= 'white').pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame, text=" view all records", command=self.Load_all_customers, cursor= 'hand2', bg= 'lime green', fg= 'white').pack(side=tk.RIGHT,padx=10)

        

    def load_data(self):
        try:
            # Clear existing entries in the Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            # Fetch all records (list of dictionaries)
            customers = MainLogic.fetch_all_customer_data()
            
            # Insert each customer into the Treeview
            for cust in customers:
                self.tree.insert("", "end", values=(
                    cust['customer_id'],   
                    cust['customer_fname'],
                    cust['customer_lname'],
                    cust['customer_mname'],
                    cust['total_credit'],
                    cust['total_payments'],
                    cust['pending_amount']
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            

    def load_unpaid_data(self):
        try:
            # Clear existing entries in the Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            # Fetch all records (list of dictionaries)
            customers = MainLogic.fetch_unpaid_customers()
            
            # Insert each customer record into the Treeview.
            for cust in customers:
                self.tree.insert("", "end", values=(
                    cust[0],  # customer_id
                    cust[1],  # customer_fname
                    cust[2],  # customer_lname
                    cust[3],  # customer_mname
                    cust[9],  # total_credit
                    cust[10], # total_payments
                    cust[11]  # pending_amount
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))



    def load_paid_data(self):
        try:
            # Clear existing entries in the Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            # Fetch all records (list of dictionaries)
            customers = MainLogic.fetch_paid_customers()
            
            # Insert each customer record into the Treeview.
            for cust in customers:
                self.tree.insert("", "end", values=(
                    cust[0],  # customer_id
                    cust[1],  # customer_fname
                    cust[2],  # customer_lname
                    cust[3],  # customer_mname
                    cust[9],  # total_credit
                    cust[10], # total_payments
                    cust[11]  # pending_amount
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))



    def Load_all_customers(self):
        try:
            # Retrieve all customers with a positive run balance (pending > 0)
            # MainLogic.fetch_all_runbal_customers() should return a list of tuples,
            # where each tuple represents a customer record including financial details.
            customers = MainLogic.fetch_all_customer_data()
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch customers: {e}")
            return

        # Create a new top-level window for displaying the customer list.
        runbal_window = tk.Toplevel(self.frame)
        runbal_window.title("Complete Record View")
        runbal_window.geometry("900x400")

        # Define the columns corresponding to the customer and financial records.
        columns = (
            "customer_id",
            "customer_fname",
            "customer_lname",
            "customer_mname",
            "address",
            "phone_number",
            "email",
            "promised_date",
            "date_created",
            "amount_credited",
            "amount_paid",
            "pending_amount"
        )

        # Create the Treeview widget with only the headings showing.
        tree = ttk.Treeview(runbal_window, columns=columns, show="headings")

        # Set up each column's heading and display format.
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=100, anchor="center")

        # Insert each customer record into the Treeview.
        for cust in customers:
            tree.insert("", tk.END, values=(
                    cust['customer_id'],   
                    cust['customer_fname'],
                    cust['customer_lname'],
                    cust['customer_mname'],
                    cust['address'],
                    cust['phone_number'],
                    cust['email'],
                    cust['promised_date'],
                    cust['date_created'],
                    cust['total_credit'],
                    cust['total_payments'],
                    cust['pending_amount']
            ))

        # Pack the Treeview to fill the window.
        tree.pack(fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar linked to the Treeview.
        scrollbar = ttk.Scrollbar(runbal_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
