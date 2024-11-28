import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from tab.database_query_tab.database_query_tab import DatabaseQuery
from tab.database_search_tab.database_search import DatabaseSearch
from tab.table_explorer_tab.table_explorer import TableExplorer
from tab.settings_tab.settings_tab import SettingsTab
from tab.table_path_tab.table_path_tab import TablePathTab
from tab.text_editor_tab.text_editor import TextEditor


class MainWindow:
    def __init__(self):

        self.root_window = create_window()

        tab1, tab2, tab3, tab4, tab5, tab6 = create_notebook(self.root_window)
        self.table_explorer = tab1
        self.database_search = tab2
        self.settings = tab3

        self.settings = SettingsTab(tab1, self.root_window)
        self.table_explorer = TableExplorer(tab2, self.settings)
        self.database_search = DatabaseSearch(tab3, self.settings)
        self.database_query = DatabaseQuery(tab4, self.settings)
        self.table_path = TablePathTab(tab5, self.settings)
        #self.text_editor = TextEditor(tab6, self.settings)
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

    tab4 = tkb.Frame(notebook)
    tab4.grid_rowconfigure(1, weight=1)
    tab4.grid_columnconfigure(0, weight=1)

    tab5 = tkb.Frame(notebook)
    tab5.grid_rowconfigure(1, weight=1)
    tab5.grid_columnconfigure(0, weight=1)

    tab6 = tkb.Frame(notebook)
    tab6.grid_rowconfigure(1, weight=1)
    tab6.grid_columnconfigure(0, weight=1)

    notebook.add(tab1, text="Settings")
    notebook.add(tab2, text="Table explorer")
    notebook.add(tab3, text="Database search")
    notebook.add(tab4, text="Database query")
    notebook.add(tab5, text="Table path")
    notebook.add(tab6, text="Text editor")

    return tab1, tab2, tab3, tab4, tab5, tab6
