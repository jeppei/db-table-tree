import ttkbootstrap as tkb
import json

from tab.settings_tab.database_connection_settings import DatabaseConnectionSettings
from tab.settings_tab.database.db import DB
from tab.settings_tab.database.db_navigator import DBNavigator
from theme.themes import all_themes


class Settings:

    def __init__(self):
        # Default values
        self.default_connections_settings = [
            {
                "name": "production",
                "host": "Production",
                "port": "11",
                "database": "db_prod",
                "user": "prod_user",
                "password": "prod_pwd"
            }, {
                "name": "testing",
                "host": "Testing",
                "port": "22",
                "database": "db_test",
                "user": "test_user",
                "password": "test_pwd"
            }, {
                "name": "local",
                "host": "Local",
                "port": "33",
                "database": "db_local",
                "user": "local_user",
                "password": "local_pwd"
            }
        ]
        self.default_selected_connection_setting_name = "local"
        self.default_selected_connection_setting = self.default_connections_settings[0]
        self.default_show_visited_parents = True
        self.default_theme = "superhero"

        # Try read from file
        self.settings_file = "settings.json"  # JSON file to store settings
        print(f"Loading settings from {self.settings_file}")
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                self.connections_settings = [
                    DatabaseConnectionSettings(
                        connection_setting.get("name", ""),
                        connection_setting.get("host", ""),
                        connection_setting.get("port", ""),
                        connection_setting.get("database", ""),
                        connection_setting.get("user", ""),
                        connection_setting.get("password", "")
                    ) for connection_setting in settings.get("connections", self.default_connections_settings)
                ]
                self.selected_connection_setting_name = settings.get(
                    "selected_connection_setting_name",
                    self.default_selected_connection_setting_name
                )
                self.selected_connection_setting = self.get_connection_settings(self.selected_connection_setting_name)
                self.show_visited_parents = tkb.StringVar()
                self.show_visited_parents.set(settings.get("show_parents", self.default_show_visited_parents))
                self.theme = tkb.StringVar()
                self.theme.set(settings.get("theme", self.default_theme))

        except FileNotFoundError:
            print("Could not find settings file!")
            pass  # File not found, use default values

        self.my_db_navigator = DBNavigator(DB(self.selected_connection_setting))

    def save_settings(self):
        print(f"Saving settings")        # Create a dictionary to store the settings you want to save
        settings_to_save = {
            "connections": [
                {
                    "name": conn.name.get(),
                    "host": conn.host.get(),
                    "port": conn.port.get(),
                    "database": conn.database.get(),
                    "user": conn.user.get(),
                    "password": conn.password.get()
                }
                for conn in self.connections_settings
            ],
            "selected_connection_setting_name": self.selected_connection_setting_name,
            "show_parents": self.show_visited_parents.get(),
            "theme": self.theme.get()
        }

        # Write the settings to the JSON file
        with open(self.settings_file, "w") as file:
            json.dump(settings_to_save, file, indent=4)

        print(f"Settings saved to {self.settings_file}")
        self.my_db_navigator = DBNavigator(DB(self.selected_connection_setting))

    def get_connection_settings(self, name):
        for connection_setting in self.connections_settings:
            if connection_setting.name.get() == name:
                return connection_setting

    def get_theme(self):
        return next((theme for theme in all_themes if theme.name == self.theme.get()), None)


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
