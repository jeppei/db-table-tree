import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from database_search_tab.database_search import DatabaseSearch
from table_explorer_tab.table_explorer import TableExplorer
from tab.settings_tab.settings_tab import SettingsTab


class MainWindow:
    def __init__(self, table, row_id):

        self.root_window = create_window()

        tab1, tab2, tab3 = create_notebook(self.root_window)
        self.table_explorer = tab1
        self.database_search = tab2
        self.settings = tab3

        self.settings = SettingsTab(tab1, self.root_window)
        self.database_search = DatabaseSearch(tab2, self.settings.settings.my_db_navigator)
        self.table_explorer = TableExplorer(tab3, self.settings.settings, table, row_id)
        self.settings.set_table_explorer(self.table_explorer)

        self.root_window.mainloop()


def create_window():
    root = tkb.Window()
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
