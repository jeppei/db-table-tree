import tkinter as tk
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


root = tk.Tk()
root.title("SQL Syntax Färgning")

sql_entry = tk.Text(root, wrap="word", width=40, height=10)
sql_entry.pack(padx=10, pady=10)

sql_entry.bind('<KeyRelease>', update_sql_coloring)

root.mainloop()
