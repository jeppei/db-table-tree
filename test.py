import tkinter as tk
import tkinter.ttk as tkb

class MyApplication:
    def __init__(self, parent):
        self.parent = parent
        parent.title("LabelFrame Example")

        # Configure the grid column and row to expand
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        database_settings_frame = tkb.LabelFrame(parent, text="Database")
        database_settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure the LabelFrame to expand both horizontally and vertically
        database_settings_frame.columnconfigure(0, weight=1)
        database_settings_frame.rowconfigure(0, weight=1)

        test_entry = tkb.Entry(database_settings_frame)
        test_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    root.mainloop()
