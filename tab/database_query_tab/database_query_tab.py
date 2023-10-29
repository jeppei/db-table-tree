import tkinter as tk
from tkinter import ttk
import sqlite3

from settings_tab import SettingsTab


class DatabaseQuery:
    def __init__(self, root, settings_tab: SettingsTab):
        self.root = root
        self.settings_tab = settings_tab

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the query input
        self.query_frame = ttk.Frame(self.root)
        self.query_frame.grid(row=0, column=0, padx=10, sticky='ew')

        # Create a label for the SQL query
        self.query_label = ttk.Label(self.query_frame, text="Enter SQL Query:")
        self.query_label.grid(row=0, column=0)

        # Create a Text widget for multi-line SQL query input
        self.query_text = tk.Text(self.query_frame, height=5, width=40)
        self.query_text.grid(row=1, column=0, sticky='nsew')
        self.query_frame.columnconfigure(0, weight=1)  # Make the text box expand horizontally

        # Create a button to execute the query
        self.execute_button = ttk.Button(self.root, text="Execute Query", command=self.execute_query)
        self.execute_button.grid(row=1, column=0, pady=10)

        # Create a frame for the result display
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.grid(row=2, column=0, padx=10, sticky='nsew')

        # Create a treeview to display the result
        self.treeview = ttk.Treeview(self.result_frame, columns=('Result'), show='headings')
        self.treeview.heading('Result', text='Result')
        self.treeview.grid(row=0, column=0, sticky='nsew')
        self.result_frame.columnconfigure(0, weight=1)  # Make the treeview expand horizontally
        self.result_frame.rowconfigure(0, weight=1)  # Make the treeview expand vertically

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.treeview.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.treeview.configure(yscrollcommand=vsb.set)

        # Create a horizontal scrollbar
        hsb = ttk.Scrollbar(self.result_frame, orient="horizontal", command=self.treeview.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.treeview.configure(xscrollcommand=hsb.set)

        # Create a label to display error messages
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=3, column=0, pady=10)

        # Configure row and column weights to make the frames expand vertically and horizontally
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def execute_query(self):
        query = self.query_text.get("1.0", "end-1c")  # Get the query from the Text widget
        try:
            db_navigator = self.settings_tab.settings.my_db_navigator
            result, column_headers = db_navigator.execute_query(query)

            # Clear the treeview
            for record in self.treeview.get_children():
                self.treeview.delete(record)

            self.treeview["columns"] = column_headers
            for col in column_headers:
                self.treeview.heading(col, text=col, anchor='w')
            # Insert the result into the treeview
            for row in result:
                self.treeview.insert('', 'end', values=row)
        except sqlite3.Error as e:
            self.result_label.config(text=f"Error: {e}")
