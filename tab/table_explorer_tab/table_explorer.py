import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from tab.settings_tab.settings_tab import SettingsTab
from tab.table_explorer_tab.table_explorer_tree import TableExplorerTree


class TableExplorer:

    def __init__(self, parent_tab, settings_tab: SettingsTab):
        self.theme = None
        self.parent_tab = parent_tab
        self.settings_tab = settings_tab
        self.combo_box = self.create_combo_box_for_tables(parent_tab)
        self.text_box = self.create_text_input_for_row_id(parent_tab)
        self.button = self.create_go_button(parent_tab)
        self.table_explorer_tree = TableExplorerTree(
            self.parent_tab,
            self.settings_tab,
            None,
            None
        )

    def change_theme(self, new_theme):
        self.theme = new_theme
        self.table_explorer_tree.change_theme(new_theme)

    def create_combo_box_for_tables(self, parent):
        db_navigator = self.settings_tab.settings.my_db_navigator
        all_table_names = db_navigator.get_all_table_names()
        combo_box = tkb.Combobox(parent, values=all_table_names)
        combo_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Use grid layout manager
        return combo_box

    def create_text_input_for_row_id(self, parent):
        text_box = tkb.Entry(parent, width=12)
        text_box.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        text_box.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Use grid layout manager
        text_box.bind("<Return>", self.on_enter_pressed)
        return text_box

    def create_go_button(self, parent):
        button = tkb.Button(parent, text="Explore", width=7, command=self.button_click)
        button.grid(row=0, column=2, padx=10, pady=10)  # Use grid layout manager
        return button

    def button_click(self):
        row_id = self.text_box.get()
        table = self.combo_box.get()
        self.table_explorer_tree = TableExplorerTree(
            self.parent_tab,
            self.settings_tab,
            table,
            row_id,
        )

    def on_enter_pressed(self, _):
        if self.text_box == self.parent_tab.focus_get():
            self.button_click()
            return 'break'  # Prevents the newline from being inserted
