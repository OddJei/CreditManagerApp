import tkinter as tk
from tkinter import ttk, messagebox
from mainlogic import MainLogic

class AddRecordTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_add_record_tab()

    def create_add_record_tab(self):

        # Customer Details entry field

        ttk.Label(self.frame, text="First Name*", font=('merriweather', 10)).grid(row=0, column=0, pady=20, padx=20)
        self.fname_entry = ttk.Entry(self.frame,width=50,)
        self.fname_entry.grid(row=0, column=1, pady=20,)

        ttk.Label(self.frame, text="Last Name*", font=('merriweather', 10)).grid(row=0, column=2, pady=20, padx=20)
        self.lname_entry = ttk.Entry(self.frame, width=50)
        self.lname_entry.grid(row=0, column=3, pady=20,)

        ttk.Label(self.frame, text="Middle Names(initials)", font=('merriweather', 10)).grid(row=1, column=0, pady=20, padx=20)
        self.mname_entry= ttk.Entry(self.frame,width=50)
        self.mname_entry.grid(row=1, column=1, pady=20, )

        ttk.Label(self.frame, text="Address", font=('merriweather', 10)).grid(row=1, column=2, pady=20, padx=20)
        self.address_entry = ttk.Entry(self.frame, width=50)
        self.address_entry.grid(row=1, column=3, pady=20, )

        ttk.Label(self.frame, text="Phone number*", font=('merriweather', 10)).grid(row=2, column=0, pady=20, padx=20)
        self.phone_entry= ttk.Entry(self.frame, width=50)
        self.phone_entry.grid(row=2, column=1, pady=20,)

        ttk.Label(self.frame, text="Email", font=('merriweather', 10)).grid(row=2, column=2, pady=20, padx=20)
        self.email_entry= ttk.Entry(self.frame, width=50)
        self.email_entry.grid(row=2, column=3, pady=20)

        ttk.Label(self.frame, text="Promised Date", font=('merriweather', 10)).grid(row=3, column=0, pady=20, padx=20)
        self.promise_entry= ttk.Entry(self.frame, width=50)
        self.promise_entry.grid(row=3, column=1, pady=20)

        ttk.Label(self.frame, text="Credited Amount*", font=('merriweather', 10)).grid(row=3, column=2, pady=20, padx=20)
        self.credit_entry = ttk.Entry(self.frame, width=50)
        self.credit_entry.grid(row=3, column=3, pady=20)

        #add customer button

        tk.Button(self.frame, text="Add Customer", font=('merriweather', 9),
                cursor= 'hand2', 
                command=self.add_customer,
                bg= 'lime green',
                fg= 'white',
                anchor='center',
                padx=70,pady=10).grid(row=4, column=0, columnspan=4,padx=20, pady=20 )
        

        # Add Credit entry field
        box1 = tk.LabelFrame(self.frame, text='Add Credit', font=('merriweather', 10), padx=10, pady=10)
        box1.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=5, pady=10)

        # Add content to the LabelFrame
        tk.Label(box1, 
                 text='Added credit to existing customer (Ensure you correctly enter existing Customer detail)',
                font=('merriweather', 7),
                 anchor= 'center').grid(row=0, column=0, columnspan=4, pady=10, padx=10)
        
        tk.Label(box1, text='Fist name',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=1, column=0, pady=5, padx=1, sticky= 'w')
        self.fname = tk.Entry(box1, width=25,)
        self.fname.grid(row=1, column=1, pady=5, padx=1, sticky= 'w')

        tk.Label(box1, text='last name',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=1, column=2, pady=5, padx=1, sticky= 'w')
        self.lname = tk.Entry(box1, width=25,)
        self.lname.grid(row=1, column=3, pady=5, padx=1, sticky= 'w')

        tk.Label(box1, text='initials',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=2, column=0, pady=5, padx=1, sticky= 'w')
        self.mname = tk.Entry(box1, width=25,)
        self.mname.grid(row=2, column=1, pady=5, padx=1, sticky= 'w')

        tk.Label(box1, text='Amount Credited',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=2, column=2, pady=5, padx=1, sticky= 'w')
        self.credit = tk.Entry(box1, width=25,)
        self.credit.grid(row=2, column=3, pady=5, padx=1, sticky= 'w')

        tk.Button(box1, text='Submit Credit', bg='lime green',
                  fg='white',
                  command= self.add_credit
                  ).grid(row=3, column=0, columnspan=4, pady=10, padx=10)


        # Add Payment entry entry field
        box2 = tk.LabelFrame(self.frame, text='Add Payment', font=('merriweather', 10), padx=10, pady=10)
        box2.grid(row=5, column=2, columnspan=2, sticky='nsew', padx=5, pady=10)

        # Add content to the LabelFrame
        tk.Label(box2, 
                 text='Added Payment to existing customer (Ensure you correctly enter existing Customer detail)',
                font=('merriweather', 7),
                 anchor= 'center').grid(row=0, column=0, columnspan=4, pady=10, padx=10)
        
        tk.Label(box2, text='Fist name',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=1, column=0, pady=5, padx=1, sticky= 'w')
        self.pay_fname = tk.Entry(box2, width=25,)
        self.pay_fname.grid(row=1, column=1, pady=5, padx=1, sticky= 'w')

        tk.Label(box2, text='last name',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=1, column=2, pady=5, padx=1, sticky= 'w')
        self.pay_lname = tk.Entry(box2, width=25,)
        self.pay_lname.grid(row=1, column=3, pady=5, padx=1, sticky= 'w')

        tk.Label(box2, text='initials',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=2, column=0, pady=5, padx=1, sticky= 'w')
        self.pay_mname = tk.Entry(box2, width=25,)
        self.pay_mname.grid(row=2, column=1, pady=5, padx=1, sticky= 'w')

        tk.Label(box2, text='Amount Credited',
                font=('merriweather', 8), 
                anchor= 'w').grid(row=2, column=2, pady=5, padx=1, sticky= 'w')
        self.pay_credit_amount = tk.Entry(box2, width=25,)
        self.pay_credit_amount.grid(row=2, column=3, pady=5, padx=1, sticky= 'w')

        tk.Button(box2, text='Submit Payment', bg='lime green',
                fg='white',
                command= self.add_payment).grid(row=3, column=0, columnspan=4, pady=10, padx=10)



    def add_customer(self):
        """
            The add_customer method is responsible for adding a new customer to the database.

            Steps:
            1. Collects customer information from various entry fields in the GUI, including:
            - First name, last name, and optional middle name.
            - Credited amount.
            - Address, phone number, and email.
            - Promised date for repayment.
            2. Passes the collected information to MainLogic.add_customer(), which handles the
            database insertion and returns a success response.
            3. Displays a success message dialog (messagebox.showinfo) to confirm the customer
            was added successfully.
            4. Handles any unexpected errors using a try-except block:
            - If an error occurs during database operations or data retrieval, it displays
                an error dialog (messagebox.showerror) with the error details.

            This method serves as the interface between the GUI inputs and the logic for adding
            a customer to the database.
        """
        try:
            response = MainLogic.add_customer(
                self.fname_entry.get().title(),
                self.lname_entry.get().title(),
                self.mname_entry.get(),
                float(self.credit_entry.get()),
                self.address_entry.get(),
                self.phone_entry.get(),
                self.email_entry.get(),
                self.promise_entry.get()
            )

            messagebox.showinfo("Success", response)

            # Clear the fields after successful submission
            self.fname_entry.delete(0, 'end')
            self.lname_entry.delete(0, 'end')
            self.mname_entry.delete(0, 'end')
            self.credit_entry.delete(0, 'end')
            self.address_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.promise_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def add_credit(self):
        """
            The add_credit method is responsible for adding credit of a customer in the credit table in the database. 

            Steps:
            1. Fetches the customer's ID(s) using their first name, last name, and optional middle name 
            via MainLogic.fetch_customer_by_name().
            2. Validates the response:
            - If no matches are found, an error message is displayed to the user.
            - If multiple matches are found, an error message is shown to inform the user.
            - If exactly one match is found, credit is added to the corresponding customer using
                MainLogic.add_credit_to_customer().
            3. Displays a success message if the credit is added successfully.
            4. Catches and handles any unexpected errors, displaying an error message to the user.
        """
        try:
            response = MainLogic.fetch_customer_by_name(
                self.fname.get().title(),
                self.lname.get().title(),
                self.mname.get()
            )
                    
            if len(response) == 0:
                messagebox.showerror("Error", "No match was found.")
            elif len(response) > 1:
                messagebox.showerror("Error", "Multiple IDs found for the given names.")
            else:

                # Add credit to the customer
                MainLogic.add_credit_to_customer(response[0], float(self.credit.get()))
                messagebox.showinfo("Success", f"Credit successfully added to customer ID: {response[0]}")
                
                #clear the field after a success submission
                self.fname.delete(0, 'end')
                self.lname.delete(0, 'end')
                self.mname.delete(0, 'end')
                self.credit.delete(0, 'end')
                
        except Exception as e:
            # Handle any other unexpected errors
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    

    def add_payment(self):
        """
            The add_payment method is responsible for recording a payment made by a customer in the database.

            Steps:
            1. Fetches the customer's ID(s) by their first name, last name, and optional middle name using
            MainLogic.fetch_customer_by_name(). The names are converted to title case for consistent matching.
            2. Validates the response:
            - If no matches are found, an error message is displayed to inform the user.
            - If multiple matches are found (e.g., customers with the same names), an error message is shown to highlight this ambiguity.
            - If exactly one match is found, the method proceeds to record the payment.
            3. Calls MainLogic.add_payment_to_customer() to add the payment to the matching customer's record.
            4. Displays a success message to confirm that the payment was successfully recorded for the given customer ID.
            5. Handles unexpected errors using a try-except block:
            - If an exception occurs (e.g., database issues or invalid input), it displays an error dialog with the specific error message.

            This method ensures that payments are accurately associated with the correct customer based on the provided name details.
        """
        try:
            response = MainLogic.fetch_customer_by_name(
                self.pay_fname.get().title(),
                self.pay_lname.get().title(),
                self.pay_mname.get()
            )
                    
            if len(response) == 0:
                messagebox.showerror("Error", "No match was found.")
            elif len(response) > 1:
                messagebox.showerror("Error", "Multiple IDs found for the given names.")
            else:
                # Add credit to the customer
                MainLogic.add_payment_to_customer(response[0], float(self.pay_credit_amount.get()))
                messagebox.showinfo("Success", f"Credit successfully added to customer ID: {response[0]}")

                #clear the field after a success submission
                self.pay_fname.delete(0, 'end')
                self.pay_lname.delete(0, 'end')
                self.pay_mname.delete(0, 'end')
                self.pay_credit_amount.delete(0, 'end')
        except Exception as e:
            # Handle any other unexpected errors
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    