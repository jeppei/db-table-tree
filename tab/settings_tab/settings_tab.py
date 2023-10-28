import ttkbootstrap as tkb
import json

from settings import Settings
from theme.themes import all_themes


class SettingsTab:

    def __init__(self, parent, root_window, table_explorer):
        self.parent = parent
        self.root_window = root_window
        self.table_explorer = table_explorer  # only to be able to change the theme

        self.connection_combo = None
        self.theme_combobox = None

        self.settings = Settings()
        self.create_settings_page(self.settings)

    def create_settings_page(self, settings):
        database_settings_frame = tkb.LabelFrame(self.parent, text="Database")
        database_settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        other_settings_frame = tkb.LabelFrame(self.parent, text="Other Settings")
        other_settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Database settings
        connection_label = tkb.Label(database_settings_frame, text="Connection:")
        connection_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        connection_settings_names = [d.name.get() for d in self.settings.connections_settings]
        self.connection_combo = tkb.Combobox(database_settings_frame, values=connection_settings_names)
        self.connection_combo.set(settings.selected_connection_setting_name)
        self.connection_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.connection_combo.bind("<<ComboboxSelected>>", self.update_connection_settings)

        connection_setting = settings.get_connection_settings(settings.selected_connection_setting_name)

        # Entry widgets associated with StringVar variables
        host_label = tkb.Label(database_settings_frame, text="Host:")
        host_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        host_entry = tkb.Entry(database_settings_frame, textvariable=connection_setting.host)
        host_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        port_label = tkb.Label(database_settings_frame, text="Port:")
        port_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        port_entry = tkb.Entry(database_settings_frame, textvariable=connection_setting.port)
        port_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        database_label = tkb.Label(database_settings_frame, text="Database:")
        database_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        database_entry = tkb.Entry(database_settings_frame, textvariable=connection_setting.database)
        database_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        user_label = tkb.Label(database_settings_frame, text="User:")
        user_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        user_entry = tkb.Entry(database_settings_frame, textvariable=connection_setting.user)
        user_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        password_label = tkb.Label(database_settings_frame, text="Password:")
        password_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        password_entry = tkb.Entry(database_settings_frame, textvariable=connection_setting.password, show="*")
        password_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Other settings
        show_parents_checkbox = tkb.Checkbutton(
            other_settings_frame,
            text="Show Parents",
            variable=settings.show_visited_parents
        )
        show_parents_checkbox.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        # Theme settings
        theme_label = tkb.Label(other_settings_frame, text="Theme:")
        theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        theme_names = [theme.name for theme in all_themes]  # Get names of themes
        self.theme_combobox = tkb.Combobox(other_settings_frame, textvariable=settings.theme, values=theme_names)
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)
        self.theme_combobox.set(settings.theme.get())
        self.change_theme(settings.theme.get())

        # Save button
        save_button = tkb.Button(self.parent, text="Save Settings", command=self.save_settings)
        save_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def change_theme(self, _):
        selected_theme_name = self.theme_combobox.get()
        selected_theme = next((theme for theme in all_themes if theme.name == selected_theme_name), None)
        if selected_theme:
            self.root_window.style.theme_use(selected_theme.name)
            self.table_explorer.change_theme(selected_theme)

    def save_settings(self):
        self.settings.save_settings()

    def update_connection_settings(self, _):
        self.settings.selected_connection_setting_name = self.connection_combo.get()
        self.create_settings_page(self.settings)


