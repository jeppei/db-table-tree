import json
import random
import tkinter as tk
from tkinter import ttk

from tab.settings_tab.settings_tab import SettingsTab


class TextEditor:

    def __init__(self, root, settings_tab: SettingsTab):
        self.root = root
        self.settings_tab = settings_tab  # Initialize your database utility

        self.tabControl.pack(expand=1, fill="both")
        self.text_widget = tk.Text(root, height=20, width=50, wrap="none")
        self.text_widget.pack(side=tkinter.RIGHT, fill="both", expand=True, padx=10, pady=10)

        y_scrollbar = tkinter.Scrollbar(self.text_widget, orient="vertical", command=self.text_widget.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=y_scrollbar.set)

        x_scrollbar = tkinter.Scrollbar(self.text_widget, orient="horizontal", command=self.text_widget.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        self.text_widget.config(xscrollcommand=x_scrollbar.set)

        self.create_text_editor()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")

        # Binding keyboard events
        self.bind('<Control-a>', self.select_all)
        #self.bind('<Control-v>', self.paste_text)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-Shift-z>', self.redo)

        # Variables for undo and redo
        self.undo_stack = []
        self.redo_stack = []

    def create_text_editor(self):
        button_frame = ttk.Frame(self.tab1)
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)

        # Format
        ttk.Label(button_frame, text="Format:").pack(side=tk.TOP, padx=5, pady=(20, 0), anchor="w")
        self.add_button(button_frame, "Format as JSON", self.format_as_json)

        # Replace
        ttk.Label(button_frame, text="Replace:").pack(side=tk.TOP, padx=5, pady=(20, 0), anchor="w")
        self.add_button(button_frame, "Replace \' with \"", self.replace_single_quotes_with_double_quotes)
        self.add_button(button_frame, "Replace \\\"' with \"", self.replace_backslash_double_qoutes_with_double_quotes)
        self.add_button(button_frame, "Replace \\n", self.replace_newline_with_newlines)
        self.add_button(button_frame, "Replace \\t", self.replace_tab)
        self.add_button(button_frame, "Replace \\n\\t", self.replace_newline_tab)
        self.add_button(button_frame, "Replace bad words", self.replace_bad_words)
        # Reorder
        ttk.Label(button_frame, text="Reorder:").pack(side=tk.TOP, padx=5, pady=(20, 0), anchor="w")
        self.add_button(button_frame, "Shuffle lines", self.shuffle_lines)
        self.add_button(button_frame, "Sort lines", self.sort_lines)
        # Remove
        ttk.Label(button_frame, text="Remove:").pack(side=tk.TOP, padx=5, pady=(20, 0), anchor="w")
        self.add_button(button_frame, "Remove Every Other Line", self.remove_every_other_line)
        self.add_button(button_frame, "Remove empty lines", self.remove_empty_lines)
        self.add_button(button_frame, "Remove first and last character", self.remove_first_and_last_character)
    def format_as_json(self):
        try:
            text = self.text_widget.get("1.0", tk.END)
            formatted_text = json.dumps(json.loads(text), indent=4)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, formatted_text)
        except Exception as e:
            print("Error formatting as JSON:", e)

    def replace_newline_tab(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("\\n\\t", "\n\t")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def replace_tab(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("\\t", "\t")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def replace_single_quotes_with_double_quotes(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("\'", "\"")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def replace_backslash_double_qoutes_with_double_quotes(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("\\\"", "\"")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def replace_bad_words(self):
        text = self.text_widget.get("1.0", tk.END)

        replacements = []
        with open('replacements.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(",")  # Split by the comma
                replacements.append([key, value])

        for replacement in replacements:
            bad_word = replacement[0]
            good_word = replacement[1]
            text = re.sub(re.escape(bad_word), good_word, text, flags=re.IGNORECASE)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def shuffle_lines(self):
        text = self.text_widget.get("1.0", tk.END)
        lines = text.split('\n')
        random.shuffle(lines)
        shuffled_text = '\n'.join(lines)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, shuffled_text)

    def sort_lines(self):
        text = self.text_widget.get("1.0", tk.END)
        lines = text.split('\n')
        sorted_lines = sorted(lines)
        sorted_text = '\n'.join(sorted_lines)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, sorted_text)

    def remove_empty_lines(self):
        text = self.text_widget.get("1.0", tk.END)
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        non_empty_text = '\n'.join(non_empty_lines)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, non_empty_text)

    def replace_at_comp(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("at com.budbee", "\n at com.budbee")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def remove_every_other_line(self):
        text = self.text_widget.get("1.0", tk.END)
        lines = text.split("\n")
        for i in range(len(lines)):
            if i % 2 == 0:
                lines[i] = ""  # You can replace this line with any desired operation
        text = "\n".join(lines).replace("\n\n", "\n")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def replace_newline_with_newlines(self):
        text = self.text_widget.get("1.0", tk.END)
        text = text.replace("\\n", "\n")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)

    def remove_first_and_last_character(self):
        text = self.text_widget.get("1.0", tk.END).strip()
        if len(text) > 1:
            text = text[1:-1]
        else:
            text = ""

        self.text_widget.delete("1.0", tk.END)  # Clear the text widget
        self.text_widget.insert(tk.END, text)  # Insert modified text

    def select_all(self, event):
        self.text_widget.tag_add("sel", "1.0", "end")

    def paste_text(self, event):
        if self.text_widget.tag_ranges("sel"):
            self.text_widget.delete("sel.first", "sel.last")
        self.text_widget.insert("insert", self.clipboard_get())

    def undo(self, event=None):
        if self.undo_stack:
            self.redo_stack.append(self.text_widget.get("1.0", "end-1c"))
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", self.undo_stack.pop())

    def redo(self, event=None):
        if self.redo_stack:
            self.undo_stack.append(self.text_widget.get("1.0", "end-1c"))
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", self.redo_stack.pop())

    def add_button(
        self,
        button_frame: tk.Frame,
        text: str,
        method
    ):
        ttk.Button(
            button_frame,
            text=text,
            command=method,
            width=30,
        ).pack(side=tk.TOP, padx=5, pady=5)