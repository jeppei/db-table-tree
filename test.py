import tkinter as tk
from tkinter import ttk

def on_node_open(event):
    item = tree.selection()[0]
    print(f"Node '{item}' was expanded")

def on_node_close(event):
    item = tree.selection()[0]
    print(f"Node '{item}' was collapsed")

# Create the main window
root = tk.Tk()
root.title("Expandable Tree")

# Create a Combobox widget
values = ["Option 1", "Option 2", "Option 3"]
combo_box = ttk.Combobox(root, values=values)
combo_box.grid(row=0, column=0, padx=10, pady=10)  # Use grid layout manager

# Create a Treeview widget
tree = ttk.Treeview(root)
tree.grid(row=1, column=0, sticky="nsew")  # Use grid layout manager and sticky option

# Bind methods to handle node expansion and collapse
tree.bind("<<TreeviewOpen>>", on_node_open)
tree.bind("<<TreeviewClose>>", on_node_close)

# Set custom indentation for child nodes
custom_indentation = 30  # Adjust the value as needed
tree.configure(style="custom.Treeview")

# Add some sample data
tree.insert("", "0", "root", text="Root Node", open=True)  # 'open=True' makes the root node expanded by default

for i in range(3):
    parent_node = f"node{i+1}"
    tree.insert("root", "end", parent_node, text=f"Parent Node {i+1}")

    for j in range(2):
        child_node = f"child{i+1}-{j+1}"
        tree.insert(parent_node, "end", child_node, text=f"Child Node {i+1}-{j+1}")

# Configure the row to have the same height as the Combobox
# root.grid_rowconfigure(0, minsize=combo_box.winfo_reqheight())

root.mainloop()