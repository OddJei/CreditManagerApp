import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk
from mainlogic import MainLogic

class HomeTab:
    def __init__(self, parent):
        self.notebook = parent
        self.frame = ttk.Frame(parent)
        self.create_home_tab()
        self.update_stats()

    def update_stats(self):
        try:
            dashboard = MainLogic.get_dashboard_summary()
            self.total_customers.config(text=f"Total Customers: {dashboard['total_Customers']}")
            self.total_credited.config(text=f"Total Credited: K{dashboard['total_credited']:.2f}")
            self.total_paid.config(text=f"Total Paid: K{dashboard['total_paid']:.2f}")
            self.total_pending.config(text=f"Pending: K{dashboard['total_pending']:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_home_tab(self):
        #the main section

        #resizing and inserting  the image
        image_path = r"C:\Users\SMART PC\Desktop\BREAD APP PROJECT\sqlite _ Credit manager\Image2.png"
        pil_image = Image.open(image_path)
        resized_image = pil_image.resize((250,250), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(resized_image)

        image_label = Label(self.frame, image=image,)
        image_label.image = image
        image_label.grid(row=0, column=0, rowspan=4, sticky='n', pady=10, padx=(50,150))

        # The welcoming label
        Hello_label = ttk.Label(self.frame, text="Welcome to JimTech's Credit Manager", font=('merriweather sans', 20, 'bold'), foreground= 'tomato')
        Hello_label.grid(row = 0, column = 1, columnspan=2, sticky= 'snew', padx= 5, pady=(10,1) )

        slogan_label = ttk.Label(self.frame, text="The easy way to manage your credits", font=('merriweather sans', 17, 'bold'), foreground= 'lime green')
        slogan_label.grid(row = 1, column = 1, columnspan=2,sticky= 'snew', padx= 50, pady=1 )

        instruction_label = ttk.Label(self.frame, text="Click add Record to manage your credits", font=('merriweather sans', 12), foreground= 'black')
        instruction_label.grid(row = 2, column = 1, columnspan=2, sticky= 'snew', padx= 120, pady=10 )
    
        button_label = tk.Button(self.frame, text="Add Record", font=('merriweather sans', 10, 'bold'),command= self.go_to_add_record_tab, foreground= 'white', background = 'lime green', cursor= 'hand2',)
        button_label.grid(row = 3, column = 1, columnspan=2,sticky= 'snew', padx= 150, pady=10)

        #adding the Horizontal line (separator)
        separator = ttk.Separator(self.frame, orient= 'horizontal')
        separator.grid(row=4, column=0, columnspan= 5, sticky= 'ew', pady=20,padx=20 )

        # Dashboard Section
        
        stats_frame = ttk.LabelFrame(self.frame, text="Quick Stats",padding=20)
        stats_frame.grid(row=5, column=0,columnspan=2, sticky='nsew', padx=10)

        self.total_customers = ttk.Label(stats_frame, text="Total Customers: $0.00", width=30, anchor='w')
        self.total_credited = ttk.Label(stats_frame, text="Total Credited: $0.00", width=30, anchor='e')
        self.total_paid = ttk.Label(stats_frame, text="Total Paid: $0.00", width=30, anchor='w')
        self.total_pending = ttk.Label(stats_frame, text="Pending: $0.00", width=30, anchor='e')

        self.total_customers.grid(row=0, column=0, padx=(10,20), pady=(10,20))
        self.total_credited.grid(row=0, column=1, padx=(20,10), pady=(10,20))
        self.total_paid.grid(row=1, column=0, padx=(10,20), pady=(20,10))
        self.total_pending.grid(row=1, column=1, padx=(20,10), pady=(20,10))

        # Quick Actions
        action_frame = ttk.LabelFrame(self.frame, text="Quick Actions")
        action_frame.grid(row=5, column=2, sticky='nsew', padx=(150,10))

        tk.Button(action_frame, text="Refresh Stats", command=self.update_stats, width=50, cursor= 'hand2', bg= 'white').grid(row=0, column=0, sticky='e',padx=10,pady=20)
        tk.Button(action_frame, text="View All running Balance Customers", command= self.view_all_runbal_customers,width=50, cursor= 'hand2', bg= 'white').grid(row=1, column=0, padx=10, pady=20, sticky='e',)
        
        #adding the Horizontal line (separator)
        separator = ttk.Separator(self.frame, orient= 'horizontal')
        separator.grid(row=6, column=0, columnspan= 5, sticky= 'ew', pady=20,padx=20 )

        #footer section
        
        instruction_label = ttk.Label(self.frame, text="© 2025 JimTech. All rights reserved. | Contact: Jchisulokt@gmail.com", font=('merriweather sans', 12), foreground= 'black',anchor= 'center')
        instruction_label.grid(row = 7, column = 0, columnspan=3, sticky= 'snew', padx= (100,50), pady=10 )
    
    def view_all_runbal_customers(self):
        try:
            # Retrieve all customers with a positive run balance (pending > 0)
            # MainLogic.fetch_all_runbal_customers() should return a list of tuples,
            # where each tuple represents a customer record including financial details.
            customers = MainLogic.fetch_unpaid_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch customers: {e}")
            return

        # Create a new top-level window for displaying the customer list.
        runbal_window = tk.Toplevel(self.frame)
        runbal_window.title("Running Balance Customers")
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
        for customer in customers:
            tree.insert("", tk.END, values=customer)

        # Pack the Treeview to fill the window.
        tree.pack(fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar linked to the Treeview.
        scrollbar = ttk.Scrollbar(runbal_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def go_to_add_record_tab(self):
        """
        Switches the view to the Add Record tab.
        """
        try:
            self.notebook.select(1)
        except Exception as e:
            messagebox.showerror("Error", f"Could not switch to Add Record tab: {e}")