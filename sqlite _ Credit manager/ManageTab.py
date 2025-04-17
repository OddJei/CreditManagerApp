import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from mainlogic import MainLogic
from db_utility import DBUtility as db

class ManageTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_frames()

    def create_frames(self):
        # Frame 1: "Search Records" (Fits 30% of the width)
        self.search_frame = ttk.LabelFrame(self.frame, text="Search Records")
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Instruction Label
        search_label = ttk.Label(
            self.search_frame,
            text="Search for a customer\nusing Name or Contact details:",
            font=('Arial', 10),
            foreground="black"
        )
        search_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Entry Fields for Name (First + Last + Optional Middle)
        name_label = ttk.Label(self.search_frame, text="Full Name (First, Last, Middle - optional):")
        name_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        ttk.Label(self.search_frame, text='First Name').grid(row=2, column=0)
        self.fname_entry = ttk.Entry(self.search_frame, width=18)
        self.fname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.search_frame, text='Last Name').grid(row=3, column=0)
        self.lname_entry = ttk.Entry(self.search_frame, width=18)
        self.lname_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.search_frame, text='Initials').grid(row=4, column=0)
        self.mname_entry = ttk.Entry(self.search_frame, width=18)
        self.mname_entry.grid(row=4, column=1, padx=5, pady=5)

        # Alternative Search: Phone Number or Email
        contact_label = ttk.Label(self.search_frame, text="Enter Phone Number or Email:")
        contact_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        ttk.Label(self.search_frame, text='Phone Number*').grid(row=6, column=0)
        self.phone_entry = ttk.Entry(self.search_frame, width=22)
        self.phone_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.search_frame, text="Email*").grid(row=7, column=0)
        self.email_entry = ttk.Entry(self.search_frame, width=22)
        self.email_entry.grid(row=7, column=1, padx=5, pady=5)

        # Search Button
        search_button = tk.Button(
            self.search_frame,
            text="Search",
            font=('Arial', 10, 'bold'),
            foreground="white",
            background="lime green",
            cursor="hand2",
            command= self.search_button_handler
        )
        search_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Configure resizing
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=1)

        # Frame 2: "View and Edit Records" 
        self.view_edit_frame = ttk.LabelFrame(self.frame, text="View and Edit Records")
        self.view_edit_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # Column widths adjusted for 500px total space
        column_widths = {
            "ID": 70, "FName": 70, "LName": 70, "MName": 70, "Address": 100,
            "Phone": 70, "Email": 120, "Created": 70, "Amount": 20, 
            "Date Credited": 20, "Amount Paid": 20, "Payment Date": 20
        }

        # Adjust Treeview heights
        treeview_height = 4  
        credit_payment_height = 6  

        # Proper row weight distribution
        self.view_edit_frame.grid_rowconfigure(0, weight=1)  
        self.view_edit_frame.grid_rowconfigure(1, weight=0)  
        self.view_edit_frame.grid_rowconfigure(2, weight=4)  
        self.view_edit_frame.grid_rowconfigure(3, weight=2) 
        self.view_edit_frame.grid_columnconfigure(0, weight=1) 
        self.view_edit_frame.grid_columnconfigure(1, weight=1)  

        # Customer Details Frame
        self.customer_frame = ttk.LabelFrame(self.view_edit_frame, text="Customer Details")
        self.customer_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        

        self.customer_tree = ttk.Treeview(self.customer_frame, columns=(
            "ID", "FName", "LName", "MName", "Address", "Phone", "Email", "Created"
        ), show="headings", height=treeview_height)
        self.customer_tree.bind("<Double-1>", self.on_double_click)  # Double-click to edit cells

        for col in self.customer_tree["columns"]:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=column_widths[col], anchor="center")

        # Horizontal Scrollbar
        customer_x_scroll = ttk.Scrollbar(self.customer_frame, orient="horizontal", command=self.customer_tree.xview)
        self.customer_tree.configure(xscrollcommand=customer_x_scroll.set)
        customer_x_scroll.pack(side="bottom", fill="x")

        self.customer_tree.pack(expand=True, fill="both")

        # Credit Details Frame
        self.credit_frame = ttk.LabelFrame(self.view_edit_frame, text="Credit Details")
        self.credit_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.credit_tree = ttk.Treeview(self.credit_frame, columns=("Amount", "Date Credited"), show="headings", height=credit_payment_height)
        for col in self.credit_tree["columns"]:
            self.credit_tree.heading(col, text=col)
            self.credit_tree.column(col, width=column_widths[col], anchor="center")

        # Vertical Scrollbar for Credit Treeview (Ensures scrolling works for all columns)
        credit_y_scroll = ttk.Scrollbar(self.credit_frame, orient="vertical", command=self.credit_tree.yview)
        self.credit_tree.configure(yscrollcommand=credit_y_scroll.set)
        credit_y_scroll.pack(side="right", fill="y")

        self.credit_tree.pack(expand=True, fill="both")

        # Payment Details Frame
        self.payment_frame = ttk.LabelFrame(self.view_edit_frame, text="Payment Details")
        self.payment_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.payment_tree = ttk.Treeview(self.payment_frame, columns=("Amount Paid", "Payment Date"), show="headings", height=credit_payment_height)
        for col in self.payment_tree["columns"]:
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, width=column_widths[col], anchor="center")

        # Vertical Scrollbar for Payment Treeview (Ensures scrolling works for all columns)
        payment_y_scroll = ttk.Scrollbar(self.payment_frame, orient="vertical", command=self.payment_tree.yview)
        self.payment_tree.configure(yscrollcommand=payment_y_scroll.set)
        payment_y_scroll.pack(side="right", fill="y")

        self.payment_tree.pack(expand=True, fill="both")

        # Edit Button (Bottom of view_edit_frame)
        edit_button = tk.Button(
            self.view_edit_frame,
            text="commit changes",
            font=('Arial', 12, 'bold'),
            foreground="white",
            background="lime green",
            cursor="hand2",
        )
        edit_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="s")



        # Frame 3: "Database Management"
        self.db_frame = ttk.LabelFrame(self.frame, text="Database Management")
        self.db_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Instruction Label
        instruction_label = ttk.Label(
            self.db_frame,
            text="Caution:\nResetting the database\nwill delete all data!",
            font=('merriweather', 10),
            foreground="black",
            anchor="center"
        )
        instruction_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Tomato Color Button for Reset
        reset_button = tk.Button(
            self.db_frame,
            text="Reset Database",
            font=('merriweather', 12, 'bold'),
            foreground="white",
            background="tomato",
            cursor="hand2", 
            anchor= 'center',
            command= self.reset_db

        )
        reset_button.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # Optional: Configure row and column weights for resizing
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)

    def search_button_handler(self):
        """
        Handles the logic when the 'Search' button is clicked:
        - Fetches customer ID(s) based on search parameters.
        - Ensures unique customer matches and provides helpful tips if multiple IDs are found.
        """
        # Get input values from the search frame
        fname = self.fname_entry.get().title().strip()
        lname = self.lname_entry.get().title().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        try:
            # Fetch customer ID(s) using the DBUtility method
            customer_ids = MainLogic.fetch_customer_id(fname=fname, lname=lname, phone=phone, email=email)

            # Handle cases with no matches, one match, or multiple matches
            if  not customer_ids:
                messagebox.showinfo("Search Result", "No customer found. Please check your input and try again.")
            elif len(customer_ids) == 10:
                customer_id = customer_ids
                messagebox.showinfo("Search Result", f"Customer ID found: {customer_id}")
                self.populate_treeviews(customer_id)
                self.fname_entry.delete(0, tk.END)
                self.lname_entry.delete(0, tk.END)
                self.mname_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                
            else:
                # Raise an error for multiple matches and suggest refining the search
                messagebox.showwarning(
                    "Multiple Matches Found",
                    f"{len(customer_ids), customer_ids} customers match your search criteria. "
                    "Please refine your input by specifying at least two fields (e.g., First Name and Last Name)."
                )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def populate_treeviews(self, customer_id):
        try:
            # Fetch raw data using MainLogic
            customer_data, credit_data, paycredit_data = MainLogic.fetch_raw_data(customer_id)

            # Handle customer data (single row)
            if customer_data:
                self.customer_tree.delete(*self.customer_tree.get_children())  # Clear previous entries
                self.customer_tree.insert("", "end", values=(
                    customer_data[0],  # ID
                    customer_data[1],  # FName
                    customer_data[2],  # LName
                    customer_data[3],  # MName
                    customer_data[4],  # Address
                    customer_data[5],  # Phone
                    customer_data[6],  # Email
                    customer_data[7],  # Created
                ))
            else:
                messagebox.showinfo("No Data", f"No Customer data found for {customer_id}")

            # Handle credit data (multiple rows)
            if credit_data:
                self.credit_tree.delete(*self.credit_tree.get_children())  # Clear previous entries
                for credit_row in credit_data:
                    self.credit_tree.insert("", "end", values=(
                        credit_row[2],  # Amount
                        credit_row[3],  # Date Credited
                    ))
            else:
                messagebox.showinfo("No Data", f"No credit data found for {customer_id}")

            # Handle paycredit data (multiple rows)
            if paycredit_data:
                self.payment_tree.delete(*self.payment_tree.get_children())  # Clear previous entries
                for paycredit_row in paycredit_data:
                    self.payment_tree.insert("", "end", values=(
                        paycredit_row[2],  # Amount Paid
                        paycredit_row[3],  # Payment Date
                    ))
            else:
                messagebox.showinfo("No Data", f"No payment data found for {customer_id}.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def on_double_click(self, event):
        # Get the selected item and column
        selected_item = self.customer_tree.selection()[0]  # Get selected row
        column = self.customer_tree.identify_column(event.x)  # Get column ID
        row_values = self.customer_tree.item(selected_item, "values")  # Get current row values

        # Map column index to column name
        column_map = {
            "#1": "ID",
            "#2": "FName",
            "#3": "LName",
            "#4": "MName",
            "#5": "Address",
            "#6": "Phone",
            "#7": "Email",
            "#8": "Created"
        }

        if column in column_map and column != "#1":  # Prevent editing the "ID" column
            self.editing_column = column_map[column]  # Store which column is being edited
            self.editing_row_id = row_values[0]  # Store the ID of the row being edited

            # Create an Entry widget at the cell location
            x, y, width, height = self.customer_tree.bbox(selected_item, column)
            self.edit_entry = ttk.Entry(self.customer_tree, width=int(width / 10))
            self.edit_entry.place(x=x, y=y, width=width, height=height)
            self.edit_entry.insert(0, row_values[int(column[1:]) - 1])  # Pre-fill current value

            self.edit_entry.focus()
            self.edit_entry.bind("<Return>", self.commit_edit)  # Save changes on Enter
            self.edit_entry.bind("<Escape>", lambda e: self.edit_entry.destroy())  # Cancel editing on Escape


    def commit_edit(self, event):
        new_value = self.edit_entry.get()  # Get the new value from the Entry widget
        self.edit_entry.destroy()  # Remove the Entry widget

        # Update the Treeview
        selected_item = self.customer_tree.selection()[0]
        column_index = int(self.editing_column[-1]) - 1  # Convert "#2" to column index (e.g., 1)
        row_values = list(self.customer_tree.item(selected_item, "values"))  # Get current row values
        row_values[column_index] = new_value  # Update the value in the selected column
        self.customer_tree.item(selected_item, values=row_values)

        # Update the database
        try:
            with sqlite3.connect("CreditManager.db") as connection:
                cursor = connection.cursor()
                query = f"UPDATE customers SET {self.editing_column} = ? WHERE id = ?"
                cursor.execute(query, (new_value, self.editing_row_id))
                connection.commit()
                messagebox.showinfo("Success", "Changes saved to the database!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to save changes to the database: {e}")


    def reset_db():
        db.clear_all_rows()

