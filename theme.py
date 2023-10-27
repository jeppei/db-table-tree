from color import Color


class Theme:

    def __init__(self, theme_name):
        self.name = theme_name
        self.color = Color(theme_name)
