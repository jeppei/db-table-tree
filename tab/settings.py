import ttkbootstrap as tkb
import json
from tkinter import ttk
from theme.themes import all_themes

class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.settings_file = "settings.json"  # JSON file to store settings
        self.connections = []  # List of database connection configurations
        self.selected_connection = None  # Currently selected database connection
        self.connection_var = tkb.StringVar()
        self.theme_var = tkb.StringVar()
        self.host_var = tkb.StringVar()
        self.port_var = tkb.StringVar()
        self.database_var = tkb.StringVar()
        self.user_var = tkb.StringVar()
        self.password_var = tkb.StringVar()
        self.show_parents_var = tkb.BooleanVar()

        self.create_settings_page()

        self.load_settings()  # Load settings from the JSON file

    def create_settings_page(self):
        database_settings_frame = tkb.LabelFrame(self.parent, text="Database")
        database_settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        other_settings_frame = tkb.LabelFrame(self.parent, text="Other Settings")
        other_settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Database settings
        connection_label = tkb.Label(database_settings_frame, text="Connection:")
        connection_combo = tkb.Combobox(database_settings_frame, textvariable=self.connection_var)

        host_label = tkb.Label(database_settings_frame, text="Host:")
        host_entry = tkb.Entry(database_settings_frame, textvariable=self.host_var)

        port_label = tkb.Label(database_settings_frame, text="Port:")
        port_entry = tkb.Entry(database_settings_frame, textvariable=self.port_var)

        database_label = tkb.Label(database_settings_frame, text="Database:")
        database_entry = tkb.Entry(database_settings_frame, textvariable=self.database_var)

        user_label = tkb.Label(database_settings_frame, text="User:")
        user_entry = tkb.Entry(database_settings_frame, textvariable=self.user_var)

        password_label = tkb.Label(database_settings_frame, text="Password:")
        password_entry = tkb.Entry(database_settings_frame, textvariable=self.password_var, show="*")

        # Other settings
        show_parents_checkbox = tkb.Checkbutton(other_settings_frame, text="Show Parents", variable=self.show_parents_var)

        # Theme settings
        theme_label = tkb.Label(other_settings_frame, text="Theme:")
        theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        theme_names = [theme.name for theme in all_themes]  # Get names of themes
        self.theme_combobox = tkb.Combobox(other_settings_frame, textvariable=self.theme_var, values=theme_names)
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # Save button
        save_button = tkb.Button(self.parent, text="Save Settings", command=self.save_settings)
        save_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Add labels and input fields to the database settings frame
        connection_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        connection_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        connection_combo.bind("<<ComboboxSelected>>", self.update_connection_settings)

        host_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        host_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        port_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        port_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        database_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        database_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        user_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        user_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        password_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        password_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        show_parents_checkbox.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

    def change_theme(self, event):
        selected_theme_name = self.theme_var.get()
        selected_theme = next((theme for theme in all_themes if theme.name == selected_theme_name), None)
        if selected_theme:
            #tkb.(selected_theme.name)
            print(selected_theme)

    def save_settings(self):
        settings = {
            "connections": self.connections,
            "show_parents": self.show_parents_var.get(),
            "theme": self.theme_var.get()
        }

        with open(self.settings_file, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                self.connections = settings.get("connections", [])
                self.show_parents_var.set(settings.get("show_parents", True))
                self.theme_var.set(settings.get("theme", "superhero"))
        except FileNotFoundError:
            print("Could not find settings file!")
            pass  # File not found, use default values

        # Populate the connection ComboBox with names
        connection_names = [connection["name"] for connection in self.connections]
        self.connection_var.set(connection_names[0] if connection_names else "")

        # Load the settings for the selected connection (default: the first connection)
        self.selected_connection = self.connections[0] if self.connections else {}
        self.update_connection_settings()

    def update_connection_settings(self, _event=None):
        # Update the database settings based on the selected connection
        selected_connection_name = self.connection_var.get()
        for connection in self.connections:
            if connection["name"] == selected_connection_name:
                self.selected_connection = connection
                break

        # Update the UI elements with the selected connection settings
        self.host_var.set(self.selected_connection.get("host", ""))
        self.port_var.set(self.selected_connection.get("port", ""))
        self.database_var.set(self.selected_connection.get("database", ""))
        self.user_var.set(self.selected_connection.get("user", ""))
        self.password_var.set(self.selected_connection.get("password", ""))

        # You may add additional logic here to update other settings if needed

# Example JSON settings file:
# {
#   "connections": [
#     {
#       "name": "Production",
#       "host": "prod",
#       "port": "1234",
#       "database": "prod_db",
#       "user": "prod_user",
#       "password": "prod_password"
#     },
#     {
#       "name": "Test",
#       "host": "test",
#       "port": "5678",
#       "database": "test_db",
#       "user": "test_user",
#       "password": "test_password"
#     }
#   ],
#   "show_parents": true,
#   "theme": "superhero"
# }
