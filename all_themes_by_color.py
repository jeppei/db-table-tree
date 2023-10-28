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

tree.insert("", 1, f'secondary', open=True, text='secondary',)
tree.insert("", 1, f'success',   open=True, text='success',)
tree.insert("", 1, f'info',      open=True, text='info',)
tree.insert("", 1, f'warning',   open=True, text='warning',)
tree.insert("", 1, f'danger',    open=True, text='danger',)
tree.insert("", 1, f'light',     open=True, text='light',)
tree.insert("", 1, f'dark',      open=True, text='dark',)
tree.insert("", 1, f'bg',        open=True, text='bg',)
tree.insert("", 1, f'fg',        open=True, text='fg',)
tree.insert("", 1, f'selectbg',  open=True, text='selectbg',)
tree.insert("", 1, f'selectfg',  open=True, text='selectfg',)
tree.insert("", 1, f'border',    open=True, text='border',)
tree.insert("", 1, f'inputfg',   open=True, text='inputfg',)
tree.insert("", 1, f'inputbg',   open=True, text='inputbg',)
tree.insert("", 1, f'primary',   open=True, text='primary',)

# Add some sample data
for theme in all_themes:

    # Good colors
    tree.insert(f'success',   1, f'success/{theme.name}',     text=theme.name, tags=(f'{theme.name}.success', ))
    tree.insert(f'info',      1, f'info/{theme.name}',        text=theme.name, tags=(f'{theme.name}.info', ))
    tree.insert(f'danger',    1, f'danger/{theme.name}',      text=theme.name, tags=(f'{theme.name}.danger', ))
    tree.insert(f'fg',        1, f'fg/{theme.name}',          text=theme.name, tags=(f'{theme.name}.fg', ))
    tree.insert(f'inputfg',   1, f'inputfg/{theme.name}',     text=theme.name, tags=(f'{theme.name}.inputfg', ))
    tree.insert(f'primary',   1, f'primary/{theme.name}',     text=theme.name, tags=(f'{theme.name}.primary', ))

    # Kind of good
    tree.insert(f'warning',   1, f'warning/{theme.name}',     text=theme.name, tags=(f'{theme.name}.warning', ))
    tree.insert(f'selectbg',  1, f'selectbg/{theme.name}',    text=theme.name, tags=(f'{theme.name}.selectbg', ))
    tree.insert(f'secondary', 1, f'secondary/{theme.name}',   text=theme.name, tags=(f'{theme.name}.secondary', ))

    # Bad colors
    # tree.insert(f'light',     1, f'light/{theme.name}',       text=theme.name, tags=(f'{theme.name}.light', ))
    # tree.insert(f'dark',      1, f'dark/{theme.name}',        text=theme.name, tags=(f'{theme.name}.dark', ))
    # tree.insert(f'bg',        1, f'bg/{theme.name}',          text=theme.name, tags=(f'{theme.name}.bg', ))
    # tree.insert(f'selectfg',  1, f'selectfg/{theme.name}',    text=theme.name, tags=(f'{theme.name}.selectfg', ))
    # tree.insert(f'border',    1, f'border/{theme.name}',      text=theme.name, tags=(f'{theme.name}.border', ))
    # tree.insert(f'inputbg',   1, f'inputbg/{theme.name}',     text=theme.name, tags=(f'{theme.name}.inputbg', ))

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
