import tkinter as tk
from tkinter import ttk, messagebox
from mainlogic import MainLogic

class ReportTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_home_tab()
        self.update_stats()

    def update_stats(self):
        try:
            dashboard = MainLogic.get_dashboard_summary()
            self.total_credited.config(text=f"Total Credited: ${dashboard['total_credited']:.2f}")
            self.total_paid.config(text=f"Total Paid: ${dashboard['total_paid']:.2f}")
            self.total_pending.config(text=f"Pending: ${dashboard['total_pending']:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_home_tab(self):
        # Dashboard Section
        stats_frame = ttk.LabelFrame(self.frame, text="Quick Stats")
        stats_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.total_credited = ttk.Label(stats_frame, text="Total Credited: $0.00")
        self.total_paid = ttk.Label(stats_frame, text="Total Paid: $0.00")
        self.total_pending = ttk.Label(stats_frame, text="Pending: $0.00")

        self.total_credited.grid(row=0, column=0, padx=10, pady=5)
        self.total_paid.grid(row=1, column=0, padx=10, pady=5)
        self.total_pending.grid(row=2, column=0, padx=10, pady=5)

        # Quick Actions
        action_frame = ttk.LabelFrame(self.frame, text="Quick Actions")
        action_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        ttk.Button(action_frame, text="Refresh Stats", command=self.update_stats).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="View All Customers", command=self.show_all_customers).grid(row=0, column=1, padx=5)

    def show_all_customers(self):
        customers = MainLogic.fetch_all_customers()
        # Implement Treeview display in a new window