import re
import tkinter as tk
from tkinter import ttk
import sqlite3

import settings_tab
from tab.database_query_tab.sql_keywords import SQL_KEYWORDS
from tab.database_query_tab.sql_functions import SQL_FUNCTIONS
from tab.database_query_tab.sql_symbols import SQL_SYMBOLS
from tab.settings_tab.settings_tab import SettingsTab


class DatabaseQuery:
    def __init__(self, root, settings_tab: SettingsTab):
        self.result_label = None
        self.settings_tab = settings_tab
        self.tables_and_columns = self.settings_tab.settings.my_db_navigator.get_tables_and_columns()

        self.root = root
        self.root.grid_columnconfigure(0, weight=1)

        # Query frame
        self.query_frame = ttk.LabelFrame(self.root, text="Enter your SQL query")
        self.query_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.query_frame.columnconfigure(0, weight=1)

        self.query_text = tk.Text(self.query_frame, height=5, width=40)
        self.query_text.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)
        self.query_text.bind('<KeyRelease>', self.update_coloring_and_dropdown)
        #self.query_text.bind('<Control-space>', lambda event: update_coloring_and_dropdown(event))

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

    def get_aliases(self, query):
        words = query.split()
        mapping = {}

        for i in range(1, len(words) - 1):
            if words[i].lower() == "as":
                abbreviation = words[i + 1]
                table_name = words[i - 1]
                if table_name in self.tables_and_columns:
                    mapping[abbreviation] = table_name

        return mapping

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

    def update_coloring_and_dropdown(self, event):
        self.update_sql_coloring(event)
        self.autocorrect(event)

    def update_sql_coloring(self, event):
        sql_query = self.query_text.get("1.0", tk.END)

        self.query_text.tag_remove(tk.ALL, "1.0", tk.END)
        for tag in self.query_text.tag_names():
            self.query_text.tag_delete(tag)

        theme = self.settings_tab.get_theme()

        aliases = self.get_aliases(sql_query)

        line_number = 1
        for line in sql_query.split('\n'):
            position = 0
            words = re.split(r'\s+|=', line)
            for word in words:
                start_pos = f"{line_number}.{position}"
                end_pos = f"{start_pos}+{len(word)}c"

                contains_start_parenthesis = "(" in word
                function_word = word.split("(")[0]
                function_word_end_pos = f"{start_pos}+{len(function_word)}c"
                quotation_marks = ("'", '"')
                tables_and_aliases = set(self.tables_and_columns.keys()) | set(aliases.keys())

                if len(word) == 0 or word in quotation_marks:
                    continue

                elif word[0] in quotation_marks and word[-1] in quotation_marks:
                    self.add_tag_for_word(start_pos, end_pos, "STRING"+word.lower(), "green")

                elif word.upper() in SQL_KEYWORDS:
                    self.add_tag_for_word(start_pos, end_pos, word.lower(), theme.color.warning)

                elif (contains_start_parenthesis and function_word.upper() in SQL_FUNCTIONS) or (word.upper() in SQL_FUNCTIONS):
                    self.add_tag_for_word(start_pos, function_word_end_pos, function_word.lower(), "blue")

                elif word.upper() in SQL_SYMBOLS:
                    self.add_tag_for_word(start_pos, end_pos, word.lower(), "grey")

                elif '.' in word and word.split('.')[0] in tables_and_aliases:
                    table_column = word.split('.')
                    table_or_alias = table_column[0]
                    alias = table_or_alias
                    table = table_or_alias
                    if alias in aliases:
                        table = aliases[table_or_alias]

                    table_columns = self.tables_and_columns[table]

                    table_end_pos = f"{start_pos}+{len(table_or_alias)}c"
                    column_start_pos = f"{start_pos}+{len(table_or_alias)+1}c"
                    self.add_tag_for_word(start_pos, table_end_pos, table_or_alias, theme.color.fg)

                    column = table_column[1]

                    if column in table_columns:
                        self.add_tag_for_word(column_start_pos, end_pos, word, "purple")
                    else:
                        self.add_tag_for_word(column_start_pos, end_pos, word, "red")

                elif word in tables_and_aliases:
                    self.add_tag_for_word(start_pos, end_pos, word, "brown")

                else:
                    self.add_default_tag_for_word(start_pos, end_pos, theme.color.fg)

                position += len(word) + 1
            line_number = line_number + 1

    def add_tag_for_word(self, start_pos, end_pos, word, color):
        self.query_text.tag_add(word, start_pos, end_pos)
        self.query_text.tag_config(word, foreground=color)

    def add_default_tag_for_word(self, start_pos, end_pos, color):
        self.query_text.tag_add("default", start_pos, end_pos)
        self.query_text.tag_config("default", foreground=color)

    def autocorrect(self, event):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Listbox):
                widget.destroy()

        cursor_position = self.query_text.index(tk.INSERT)
        line, col = map(int, cursor_position.split('.'))
        current_line = self.query_text.get(f"{line}.0", f"{line}.end")
        words = current_line.split()

        last_character = self.query_text.get(f"{line}.{col-1}", f"{line}.{col}")
        if len(last_character.strip()) == 0:
            return

        word_index = 0
        cursor_index = self.query_text.index(tk.INSERT)
        for i, word in enumerate(words):
            cursor_after_text_start = cursor_index >= self.query_text.index(f"{line}.{col}")
            cursor_before_text_end = cursor_index < self.query_text.index(f"{line}.{col + len(word)}")
            if i == len(words) - 1 or (cursor_after_text_start and cursor_before_text_end):
                word_index = i
                break

        suggested_words = []

        if len(words) == 0:
            return

        sql_query = self.query_text.get("1.0", tk.END)
        aliases = self.get_aliases(sql_query)
        tables_and_aliases = set(self.tables_and_columns.keys()) | set(aliases.keys())
        current_word = words[word_index]
        all_sql_words_and_tables = SQL_KEYWORDS | SQL_FUNCTIONS | tables_and_aliases

        if current_word in all_sql_words_and_tables:
            return

        if '.' in current_word:
            table_or_alias, _ = current_word.split('.', 1)
            alias = table_or_alias
            table = table_or_alias
            if alias in aliases:
                table = aliases[table]

            words_to_check_against = set()
            if table_or_alias in tables_and_aliases:
                for column in self.tables_and_columns[table]:
                    words_to_check_against.add(f"{table_or_alias}.{column}")
        else:
            words_to_check_against = all_sql_words_and_tables

        suggestions = [w for w in words_to_check_against if w.startswith(current_word)]
        suggestions_sorted = sorted(suggestions, key=len)

        if suggestions_sorted:
            suggested_words.extend(suggestions_sorted)

        if current_word in suggestions_sorted:
            suggestions_sorted.remove(current_word)

        if len(suggestions_sorted) == 0:
            return

        longest_word_length = max(len(word) for word in suggestions_sorted)
        suggestion_listbox = tk.Listbox(
            self.root,
            selectbackground="lightblue",
            selectmode=tk.SINGLE,
            width=longest_word_length
        )
        for suggested_word in suggested_words:
            suggestion_listbox.insert(tk.END, suggested_word)

        x, y, _, _ = self.query_text.bbox(f"{line}.{col - len(current_word)}")
        y += 55
        x += 20

        suggestion_listbox.place(x=x, y=y)
        suggestion_listbox.selection_set(0)

        def on_select(_):
            selected_index = suggestion_listbox.curselection()
            print(f'selected index_{selected_index}')
            if selected_index:
                selected_suggestion = suggestion_listbox.get(selected_index[0])
                start_pos = self.query_text.index(f"{line}.{col - len(current_word)}")
                end_pos = self.query_text.index(f"{line}.{col}")
                self.query_text.delete(start_pos, end_pos)
                self.query_text.insert(start_pos, selected_suggestion)
            suggestion_listbox.destroy()
            self.query_text.focus_set()

        def move_up(_):
            current_index = suggestion_listbox.curselection()
            if current_index and current_index[0] > 0:
                suggestion_listbox.selection_clear(current_index[0])
                suggestion_listbox.selection_set(current_index[0] - 1)

        def move_down(_):
            current_index = suggestion_listbox.curselection()
            if current_index and current_index[0] < suggestion_listbox.size() - 1:
                suggestion_listbox.selection_clear(current_index[0])
                suggestion_listbox.selection_set(current_index[0] + 1)

        suggestion_listbox.bind("<Return>", on_select)
        suggestion_listbox.bind("<KP_Enter>", on_select)
        suggestion_listbox.bind("<Escape>", lambda escape_event: suggestion_listbox.destroy() or self.query_text.focus_set())
        suggestion_listbox.bind("<Up>", move_up)
        suggestion_listbox.bind("<Down>", move_down)
        suggestion_listbox.bind("<FocusOut>", lambda focus_out_event: suggestion_listbox.destroy())

        if event and event.keysym == "Down":
            suggestion_listbox.focus_set()
            suggestion_listbox.selection_set(0)

