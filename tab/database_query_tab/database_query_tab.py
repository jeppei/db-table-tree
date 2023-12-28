import difflib
import tkinter as tk
from tkinter import ttk
import sqlite3

from sql_keywords import SQL_KEYWORDS
from tab.settings_tab.settings_tab import SettingsTab


class DatabaseQuery:
    def __init__(self, root, settings_tab: SettingsTab):
        self.result_label = None
        self.settings_tab = settings_tab

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

        line_number = 1
        for line in sql_query.split('\n'):
            position = 0
            words = line.split()
            for word in words:
                word_length = len(word)

                start_pos = f"{line_number}.{position}"
                end_pos = f"{start_pos}+{word_length}c"

                if word.upper() in SQL_KEYWORDS:
                    self.query_text.tag_add(word.lower(), start_pos, end_pos)
                    self.query_text.tag_config(word.lower(), foreground=theme.color.warning)
                else:
                    self.query_text.tag_add("default", start_pos, end_pos)
                    self.query_text.tag_config("default", foreground=theme.color.fg)

                position += word_length + 1
            line_number = line_number + 1

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

        current_word = words[word_index]
        if current_word in SQL_KEYWORDS:
            return

        suggestions = difflib.get_close_matches(current_word.upper(), SQL_KEYWORDS, n=10, cutoff=0.7)
        if suggestions:
            suggested_words.extend(suggestions)

        if len(suggested_words) == 0:
            return

        suggestion_listbox = tk.Listbox(self.root, selectbackground="lightblue", selectmode=tk.SINGLE)
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

