import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from HomeTab import HomeTab
from AddRecordTab import AddRecordTab
from ManageTab import ManageTab
from ViewTab import ViewTab

class MainGUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")  # Modern theme
        self.root.title("Credits Manager")
        self.setup_window()
        self.create_tabs()
        self.root.mainloop()

    def setup_window(self):
        # Set fixed window size
        window_width = 1000
        window_height = 614
        self.root.geometry(f"{window_width}x{window_height}")

        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"+{position_right}+{position_down}")

       # Prevent resizing
        self.root.resizable(False, False)

    def create_tabs(self):
        # Create a custom style for the tab headers
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 9), padding=[97, 20])

        # Tab control (Notebook)
        tab_control = ttk.Notebook(self.root, padding=10)

        # Initialize all tabs
        home_tab = HomeTab(tab_control)
        add_record_tab = AddRecordTab(tab_control)
        manage_tab = ManageTab(tab_control)
        view_tab = ViewTab(tab_control)


        # Add tabs to notebook
        tab_control.add(home_tab.frame, text="HOME")
        tab_control.add(add_record_tab.frame, text="ADD RECORD")
        tab_control.add(manage_tab.frame, text="MANAGE")
        tab_control.add(view_tab.frame, text="VIEW")

        

        # Pack the notebook (fills entire window)
        tab_control.pack(expand=True, fill="both")
        

if __name__ == "__main__":
    app = MainGUI()