import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from themes import all_themes

# Create the main window
show_already_visited_parents = False
root = tkb.Window()
root.title("Expandable Tree")
root.geometry("1000x1000")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a Treeview widget
tree = tkb.Treeview(root)
tree.grid(row=0, column=0, sticky="nsew")  # Use grid layout manager and sticky option

# Set custom indentation for child nodes
custom_indentation = 30  # Adjust the value as needed
tree.configure(style="custom.Treeview")

# Add some sample data
for theme in all_themes:
    tree.insert("", 1, theme.name, text=theme.name, open=True, tags=(f'{theme.name}.fg', ))  # 'open=True' makes the root node expanded by default
    tree.insert(theme.name, 1, f'{theme.name}/good',  text="good",  open=True, tags=(f'{theme.name}.fg', ))  # 'open=True' makes the root node expanded by default
    tree.insert(theme.name, 1, f'{theme.name}/works', text="works", open=True, tags=(f'{theme.name}.fg', ))  # 'open=True' makes the root node expanded by default
    tree.insert(theme.name, 1, f'{theme.name}/bad',   text="bad",   open=False, tags=(f'{theme.name}.fg', ))  # 'open=True' makes the root node expanded by default

    # Good colors
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/success',     text='success',     tags=(f'{theme.name}.success', ))
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/info',        text='info',        tags=(f'{theme.name}.info', ))
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/danger',      text='danger',      tags=(f'{theme.name}.danger', ))
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/fg',          text='fg',          tags=(f'{theme.name}.fg', ))
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/inputfg',     text='inputfg',     tags=(f'{theme.name}.inputfg', ))
    tree.insert(f'{theme.name}/good', 1, f'{theme.name}/good/primary',     text='primary',     tags=(f'{theme.name}.primary', ))

    # Kind of good
    tree.insert(f'{theme.name}/works', 1, f'{theme.name}/works/root/warning',     text='warning',     tags=(f'{theme.name}.warning', ))
    tree.insert(f'{theme.name}/works', 1, f'{theme.name}/works/root/selectbg',    text='selectbg',    tags=(f'{theme.name}.selectbg', ))
    tree.insert(f'{theme.name}/works', 1, f'{theme.name}/works/root/secondary',   text='secondary',   tags=(f'{theme.name}.secondary', ))

    # Bad colors
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/light',       text='light',       tags=(f'{theme.name}.light', ))
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/dark',        text='dark',        tags=(f'{theme.name}.dark', ))
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/bg',          text='bg',          tags=(f'{theme.name}.bg', ))
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/selectfg',    text='selectfg',    tags=(f'{theme.name}.selectfg', ))
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/border',      text='border',      tags=(f'{theme.name}.border', ))
    tree.insert(f'{theme.name}/bad', 1, f'{theme.name}/bad/inputbg',     text='inputbg',     tags=(f'{theme.name}.inputbg', ))

    tree.tag_configure(f'{theme.name}.primary',      background=theme.color.bg, foreground=theme.color.primary)
    tree.tag_configure(f'{theme.name}.secondary',    background=theme.color.bg, foreground=theme.color.secondary)
    tree.tag_configure(f'{theme.name}.success',      background=theme.color.bg, foreground=theme.color.success)
    tree.tag_configure(f'{theme.name}.info',         background=theme.color.bg, foreground=theme.color.info)
    tree.tag_configure(f'{theme.name}.warning',      background=theme.color.bg, foreground=theme.color.warning)
    tree.tag_configure(f'{theme.name}.danger',       background=theme.color.bg, foreground=theme.color.danger)
    tree.tag_configure(f'{theme.name}.light',        background=theme.color.bg, foreground=theme.color.light)
    tree.tag_configure(f'{theme.name}.dark',         background=theme.color.bg, foreground=theme.color.dark)
    tree.tag_configure(f'{theme.name}.bg',           background=theme.color.bg, foreground=theme.color.bg)
    tree.tag_configure(f'{theme.name}.fg',           background=theme.color.bg, foreground=theme.color.fg)
    tree.tag_configure(f'{theme.name}.selectbg',     background=theme.color.bg, foreground=theme.color.select_bg)
    tree.tag_configure(f'{theme.name}.selectfg',     background=theme.color.bg, foreground=theme.color.select_fg)
    tree.tag_configure(f'{theme.name}.border',       background=theme.color.bg, foreground=theme.color.border)
    tree.tag_configure(f'{theme.name}.inputfg',      background=theme.color.bg, foreground=theme.color.input_fg)
    tree.tag_configure(f'{theme.name}.inputbg',      background=theme.color.bg, foreground=theme.color.input_bg)

root.mainloop()
