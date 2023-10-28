import ttkbootstrap.themes.standard


class Color:
    def __init__(self, theme_name):
        themes = ttkbootstrap.themes.standard.STANDARD_THEMES
        colors = themes[theme_name]["colors"]
        self.primary = colors["primary"],
        self.secondary = colors["secondary"],
        self.success = colors["success"],
        self.info = colors["info"],
        self.warning = colors["warning"],
        self.danger = colors["danger"],
        self.light = colors["light"],
        self.dark = colors["dark"],
        self.bg = colors["bg"],
        self.fg = colors["fg"],
        self.select_bg = colors["selectbg"],
        self.select_fg = colors["selectfg"],
        self.border = colors["border"],
        self.input_fg = colors["inputfg"],
        self.input_bg = colors["inputbg"],
