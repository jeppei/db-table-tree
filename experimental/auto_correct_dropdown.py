import tkinter as tk
import difflib
import re


def update_sql_coloring(event):
    sql_code = sql_entry.get("1.0", tk.END)
    sql_tokens = re.findall(r"\b(?:SELECT|FROM|WHERE|AND|OR|INSERT|INTO|VALUES|UPDATE|SET|DELETE|ORDER BY|GROUP BY|BY|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN)\b", sql_code, re.IGNORECASE)

    sql_entry.tag_remove("default", "1.0", tk.END)

    for token in sql_tokens:
        start_pos = "1.0"
        while True:
            start_pos = sql_entry.search(token, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(token)}c"
            sql_entry.tag_add(token.lower(), start_pos, end_pos)
            start_pos = end_pos

    sql_entry.tag_config("select", foreground="blue")
    sql_entry.tag_config("from", foreground="blue")
    sql_entry.tag_config("where", foreground="blue")
    sql_entry.tag_config("and", foreground="blue")
    sql_entry.tag_config("or", foreground="blue")
    sql_entry.tag_config("insert", foreground="blue")
    sql_entry.tag_config("into", foreground="blue")
    sql_entry.tag_config("values", foreground="blue")
    sql_entry.tag_config("update", foreground="blue")
    sql_entry.tag_config("set", foreground="blue")
    sql_entry.tag_config("delete", foreground="blue")
    sql_entry.tag_config("order by", foreground="blue")
    sql_entry.tag_config("group by", foreground="blue")
    sql_entry.tag_config("by", foreground="blue")
    sql_entry.tag_config("join", foreground="blue")
    sql_entry.tag_config("inner join", foreground="blue")
    sql_entry.tag_config("left join", foreground="blue")
    sql_entry.tag_config("right join", foreground="blue")
    autocorrect(event)


def autocorrect(event):
    # Destroy the existing suggestion_listbox, if any
    for widget in root.winfo_children():
        if isinstance(widget, tk.Listbox):
            widget.destroy()

    cursor_position = sql_entry.index(tk.INSERT)
    line, col = map(int, cursor_position.split('.'))
    current_line = sql_entry.get(f"{line}.0", f"{line}.end")
    words = current_line.split()

    # Identify the word where the insertion cursor is located
    word_index = 0
    cursor_index = sql_entry.index(tk.INSERT)
    for i, word in enumerate(words):
        if i == len(words) - 1 or (cursor_index >= sql_entry.index(f"{line}.{col}") and cursor_index < sql_entry.index(f"{line}.{col + len(word)}")):
            word_index = i
            break

    suggested_words = []

    if len(words) == 0:
        return
    current_word = words[word_index]
    if current_word in sql_keywords:
        return

    # Generate suggestions for the current word
    suggestions = difflib.get_close_matches(current_word, sql_keywords, n=10, cutoff=0.8)
    if suggestions:
        suggested_words.extend(suggestions)

    if len(suggested_words) == 0:
        return

    # Create a Listbox for suggestions
    suggestion_listbox = tk.Listbox(root, selectbackground="lightblue", selectmode=tk.SINGLE)
    for suggested_word in suggested_words:
        suggestion_listbox.insert(tk.END, suggested_word)

    # Place the Listbox near the current word
    x, y, _, _ = sql_entry.bbox(f"{line}.{col - len(current_word)}")

    # Small window
    # y += 25
    # x += 10

    # Fullscreen
    y += 15

    suggestion_listbox.place(x=x, y=y)

    # Automatically select the first item
    suggestion_listbox.selection_set(0)

    # Function to handle suggestion selection
    def on_select(event):
        selected_index = suggestion_listbox.curselection()
        print(f'selected index_{selected_index}')
        if selected_index:
            selected_suggestion = suggestion_listbox.get(selected_index[0])
            start_pos = sql_entry.index(f"{line}.{col - len(current_word)}")
            end_pos = sql_entry.index(f"{line}.{col}")
            sql_entry.delete(start_pos, end_pos)
            sql_entry.insert(start_pos, selected_suggestion)
        suggestion_listbox.destroy()
        sql_entry.focus_set()

    def move_up(event):
        current_index = suggestion_listbox.curselection()
        if current_index and current_index[0] > 0:
            suggestion_listbox.selection_clear(current_index[0])
            suggestion_listbox.selection_set(current_index[0] - 1)

    def move_down(event):
        current_index = suggestion_listbox.curselection()
        if current_index and current_index[0] < suggestion_listbox.size() - 1:
            suggestion_listbox.selection_clear(current_index[0])
            suggestion_listbox.selection_set(current_index[0] + 1)

    suggestion_listbox.bind("<Return>", on_select)
    suggestion_listbox.bind("<KP_Enter>", on_select)  # For Enter key on numpad
    suggestion_listbox.bind("<Escape>", lambda event: suggestion_listbox.destroy())
    suggestion_listbox.bind("<Up>", move_up)
    suggestion_listbox.bind("<Down>", move_down)

    # Bind the Listbox to the event handler
    suggestion_listbox.bind("<FocusOut>", lambda event: suggestion_listbox.destroy())
    suggestion_listbox.bind("<Escape>", lambda event: suggestion_listbox.destroy() or sql_entry.focus_set())

    # Set the focus on the Listbox
    # suggestion_listbox.focus_set()
    # Check if the down arrow key was pressed in the text box
    if event and event.keysym == "Down":
        suggestion_listbox.focus_set()


root = tk.Tk()
root.attributes('-zoomed', True)


root.title("SQL Syntax Färgning och Autocorrect")

sql_keywords = ["SELECT", "FROM", "FROM1", "FROM2", "WHERE", "AND", "OR", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "ORDER BY", "GROUP BY", "BY", "JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"]

# Fullscreen
sql_entry = tk.Text(root, wrap="word")
sql_entry.pack(expand=True, fill="both")

#Small window
#sql_entry = tk.Text(root, wrap="word", width=40, height=10)
# sql_entry.pack(padx=10, pady=10)

sql_entry.bind('<KeyRelease>', update_sql_coloring)
# sql_entry.bind('<Control-space>', lambda event: autocorrect())
sql_entry.bind('<Control-space>', lambda event: autocorrect(event))


root.mainloop()
