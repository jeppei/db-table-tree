import ttkbootstrap as tkb
from tkinter import ttk


class DatabaseSearch:

    def __init__(self, root, db_navigator):
        self.root = root
        self.db_navigator = db_navigator  # Initialize your database utility
        self.result_label = None

        # Create and place the entry, combobox, and search button
        self.search_entry = tkb.Entry(self.root)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.search_type = ttk.Combobox(self.root, width=10, values=["table", "column"])
        self.search_type.set("table")
        self.search_type.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.search_button = tkb.Button(self.root, text="Search", width=7, command=self.search_tables)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Create a Treeview widget to display results with two columns
        self.result_tree = ttk.Treeview(self.root, columns=("Column1", "Column2"), selectmode="browse")
        self.result_tree.heading("Column1", text="")
        self.result_tree.heading("Column2", text="")
        self.result_tree.column("#0", width=0, stretch=False)  # Hide the first column
        self.result_tree.column("Column1", width=200)
        self.result_tree.column("Column2", width=200)
        self.result_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights for expansion
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def search_tables(self):
        # Clear the previous search results
        self.result_tree.delete(*self.result_tree.get_children())

        # Get the search string and search type from the widgets
        search_string = self.search_entry.get()
        search_type = self.search_type.get()

        # Call your database method to get matching table names or columns
        if search_type == "table":
            self.result_tree.heading("Column1", text="Name")
            self.result_tree.heading("Column2", text="Count")
            column1, column2 = self.db_navigator.find_table(search_string)
        elif search_type == "column":
            self.result_tree.heading("Column1", text="Table")
            self.result_tree.heading("Column2", text="Column")
            column1, column2 = self.db_navigator.find_column(search_string)
        else:
            column1 = []
            column2 = []

        if column1:
            for i in range(len(column1)):
                self.result_tree.insert("", "end", values=(column1[i], column2[i]))
        else:
            self.result_tree.insert("", "end", values=(f"No matching {search_type}s found", ""))
