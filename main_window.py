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
        self.combo_box = self.create_combo_box_for_tables()
        self.text_box = self.create_text_input_for_row_id()
        self.button = self.create_go_button()
        self.tree = None
        self.root.grid_rowconfigure(1, weight=1)

        self.root.mainloop()

    def create_window(self):
        root = tkb.Window(themename=self.theme.name)
        root.geometry("1000x1000")
        root.title("Expandable Tree")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=0)
        return root

    def create_combo_box_for_tables(self):
        all_table_names = self.my_db_navigator.get_all_table_names()
        combo_box = tkb.Combobox(self.root, values=all_table_names)
        combo_box.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Use grid layout manager
        if self.table in combo_box['values']:
            combo_box.set(self.table)
        return combo_box

    def create_text_input_for_row_id(self):
        text_box = tkb.Text(self.root, height=1, width=25, wrap="none")
        text_box.insert("1.0", self.row_id)
        text_box.grid(row=0, column=1, padx=0, pady=0, sticky="ew")  # Use grid layout manager
        text_box.bind("<Return>", self.on_enter_pressed)
        return text_box

    def create_go_button(self):
        button = tkb.Button(self.root, text="GO!", command=self.button_click)
        button.grid(row=0, column=2, padx=0, pady=0)  # Use grid layout manager
        return button

    def button_click(self):
        row_id = self.text_box.get("1.0", "end-1c")
        table = self.combo_box.get()
        self.tree = Tree(self.root, self.theme, table, row_id, self.my_db_navigator)

    def on_enter_pressed(self, _):
        if self.text_box == self.root.focus_get():
            self.button_click()
            return 'break'  # Prevents the newline from being inserted
