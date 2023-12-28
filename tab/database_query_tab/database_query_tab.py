import tkinter as tk
from tkinter import ttk
import sqlite3

from tab.settings_tab.settings_tab import SettingsTab


class DatabaseQuery:
    def __init__(self, root, settings_tab: SettingsTab):
        self.settings_tab = settings_tab

        self.root = root
        self.root.grid_columnconfigure(0, weight=1)

        # Query frame
        self.query_frame = ttk.LabelFrame(self.root, text="Enter your SQL query")
        self.query_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.query_frame.columnconfigure(0, weight=1)

        self.query_text = tk.Text(self.query_frame, height=5, width=40)
        self.query_text.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.execute_button = ttk.Button(self.query_frame, text="Execute Query", command=self.execute_query)
        self.execute_button.grid(row=1, column=0, pady=(0, 10))

        # Resulting frame
        self.result_frame = ttk.LabelFrame(self.root, text="Result")
        self.result_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)

        self.scrolling_frame = ttk.Frame(self.result_frame)
        self.scrolling_frame.columnconfigure(0, weight=1)
        self.scrolling_frame.rowconfigure(0, weight=1)
        self.scrolling_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.result_table = ttk.Treeview(self.scrolling_frame, columns='Result', show='headings')
        self.result_table.heading('Result', text='')
        self.result_table.grid(row=0, column=0, sticky='nsew')

        self.vsb = ttk.Scrollbar(self.scrolling_frame, orient="vertical", command=self.result_table.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.result_table.configure(yscrollcommand=self.vsb.set)

        self.hsb = ttk.Scrollbar(self.scrolling_frame, orient="horizontal", command=self.result_table.xview)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.result_table.configure(xscrollcommand=self.hsb.set)

    def execute_query(self):
        query = self.query_text.get("1.0", "end-1c")  # Get the query from the Text widget
        try:
            db_navigator = self.settings_tab.settings.my_db_navigator
            result, column_headers = db_navigator.execute_query(query)

            # Clear the treeview
            for record in self.result_table.get_children():
                self.result_table.delete(record)

            self.result_table["columns"] = column_headers
            for col in column_headers:
                self.result_table.heading(col, text=col, anchor='w')
            # Insert the result into the treeview
            for row in result:
                self.result_table.insert('', 'end', values=row)
        except sqlite3.Error as e:
            self.result_label.config(text=f"Error: {e}")
