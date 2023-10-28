import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from database.db import DB
from database.db_navigator import DBNavigator
from theme.themes import Themes

from database_search_tab.database_search import DatabaseSearch
from table_explorer_tab.table_explorer import TableExplorer
from tab.settings_tab.settings_tab import SettingsTab


class MainWindow:
    def __init__(self, table, row_id, env):
        self.env = env
        self.my_db_navigator = DBNavigator(DB(self.env))
        self.theme = Themes.superhero

        self.root_window = create_window(self.theme)

        tab1, tab2, tab3 = create_notebook(self.root_window)
        self.table_explorer = tab1
        self.database_search = tab2
        self.settings = tab3

        self.table_explorer = TableExplorer(tab3, self.theme, self.my_db_navigator, table, row_id)
        self.database_search = DatabaseSearch(tab2, self.my_db_navigator)
        self.settings = SettingsTab(tab1, self.root_window, self.table_explorer)

        self.root_window.mainloop()


def create_window(theme):
    root = tkb.Window(themename=theme.name)
    root.geometry("1000x1000")
    root.title("Expandable Tree")
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=1)
    return root


def create_notebook(parent):
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
