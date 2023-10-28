import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from database.db import DB
from database.db_navigator import DBNavigator
from theme.themes import Themes
from tree import Tree


class MainWindow:
    def __init__(self, table, row_id, env):
        self.table = table
        self.row_id = row_id
        self.env = env
        self.my_db_navigator = DBNavigator(DB(self.env))
        self.theme = Themes.superhero

        self.root = self.create_window()

        tab1, tab2, tab3 = self.create_notebook(self.root)
        self.table_explorer = tab1
        self.database_search = tab2
        self.settings = tab3

        self.combo_box = self.create_combo_box_for_tables(tab1, table)
        self.text_box = self.create_text_input_for_row_id(tab1, row_id)
        self.button = self.create_go_button(tab1)
        self.tree = None

        self.root.mainloop()

    def create_window(self):
        root = tkb.Window(themename=self.theme.name)
        root.geometry("1000x1000")
        root.title("Expandable Tree")
        root.grid_rowconfigure(0, weight=0)
        root.grid_columnconfigure(0, weight=1)
        return root

    def create_notebook(self, parent):
        notebook = tkb.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        tab1 = tkb.Frame(notebook)
        tab1.grid_rowconfigure(1, weight=1)
        tab1.grid_columnconfigure(0, weight=1)

        tab2 = tkb.Frame(notebook)
        tab2.grid_rowconfigure(1, weight=1)
        tab2.grid_columnconfigure(0, weight=1)

        tab3 = tkb.Frame(notebook)
        tab3.grid_rowconfigure(1, weight=1)
        tab3.grid_columnconfigure(0, weight=1)

        notebook.add(tab1, text="Table explorer")
        notebook.add(tab2, text="Database search")
        notebook.add(tab3, text="Settings")

        return tab1, tab2, tab3

    def create_combo_box_for_tables(self, parent, table):
        all_table_names = self.my_db_navigator.get_all_table_names()
        combo_box = tkb.Combobox(parent, values=all_table_names)
        combo_box.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Use grid layout manager
        if table in combo_box['values']:
            combo_box.set(table)
        return combo_box

    def create_text_input_for_row_id(self, parent, row_id):
        text_box = tkb.Text(parent, height=1, width=25, wrap="none")
        text_box.insert("1.0", row_id)
        text_box.grid(row=0, column=1, padx=0, pady=0, sticky="ew")  # Use grid layout manager
        text_box.bind("<Return>", self.on_enter_pressed)
        return text_box

    def create_go_button(self, parent):
        button = tkb.Button(parent, text="GO!", command=self.button_click)
        button.grid(row=0, column=2, padx=0, pady=0)  # Use grid layout manager
        return button

    def button_click(self):
        row_id = self.text_box.get("1.0", "end-1c")
        table = self.combo_box.get()
        self.tree = Tree(self.table_explorer, self.theme, table, row_id, self.my_db_navigator)

    def on_enter_pressed(self, _):
        if self.text_box == self.root.focus_get():
            self.button_click()
            return 'break'  # Prevents the newline from being inserted
