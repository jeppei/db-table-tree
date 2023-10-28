import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from database.db import DB
from database.db_navigator import DBNavigator
from node.node_tags import NodeTags
from node.node_types import NodeTypes
from node.node import Node
from theme.themes import Themes


class ExpandableTree:
    def __init__(self, table, row_id, env):
        self.table = table
        self.row_id = row_id
        self.env = env

        self.nodes = {}
        self.my_db_navigator = DBNavigator(DB(self.env))

        self.theme = Themes.superhero
        self.show_already_visited_parents = False

        self.root = self.create_window()
        self.combo_box = self.create_combo_box_for_tables()
        self.text_box = self.create_text_input_for_row_id()
        self.button = self.create_go_button()

        self.root.mainloop()

    def create_window(self):
        root = tkb.Window(themename=self.theme.name)
        root.geometry("1000x1000")
        root.title("Expandable Tree")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=0)
        return root

    def create_combo_box_for_tables(self):
        all_table_names = self.my_db_navigator.get_all_table_names()
        combo_box = tkb.Combobox(self.root, values=all_table_names)
        combo_box.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Use grid layout manager
        if self.table in combo_box['values']:
            combo_box.set(self.table)
        return combo_box

    def create_text_input_for_row_id(self):
        text_box = tkb.Text(self.root, height=1, width=25, wrap="none")
        text_box.insert("1.0", self.row_id)
        text_box.grid(row=0, column=1, padx=0, pady=0, sticky="ew")  # Use grid layout manager
        text_box.bind("<Return>", self.on_enter_pressed)
        return text_box

    def create_go_button(self):
        button = tkb.Button(self.root, text="GO!", command=self.button_click)
        button.grid(row=0, column=2, padx=0, pady=0)  # Use grid layout manager
        return button

    def add_to_tree(self, node, node_text):
        if self.tree.exists(node.full_path):
            return False
        print(f'{node.node_type.direction}: Adding {node.node_type.name}: {node.full_path}')
        self.nodes[node.full_path] = node

        tags = (node.node_type.name, )

        if (
            (not node.exist and not node.parent_node.exist) or
            (not node.exist and node.node_type == NodeTypes.PARENT_LIST_NODE)
        ):
            tags = (NodeTags.NO_VALUE, )
        elif node.visited:
            tags = (NodeTags.VISITED, )

        self.tree.insert(
            node.parent_node.full_path,
            10000,
            node.full_path,
            text=node_text,
            tags=tags
        )
        return True

    def fetch_children(self, parent_path):
        message = f'# Expanding on {parent_path} #'
        line = '#' * len(message)
        print(f'\n{line}\n{message}\n{line}\n')
        parent_node = self.nodes[parent_path]
        if parent_node.node_type == NodeTypes.LEAF:
            return
        if parent_node.node_type == NodeTypes.DUMMY:
            return
        if parent_node.node_type == NodeTypes.PARENT_LIST_NODE:
            return

        if self.tree.exists(f'{parent_path}/(double-click)'):
            self.tree.delete(f'{parent_path}/(double-click)')

        if parent_node.node_type == NodeTypes.PARENT:
            primary_keys = self.my_db_navigator.get_primary_key_of_table(parent_node.table_name)
            new_parent_columns, new_parents, has_parents = self.my_db_navigator.get_parents(
                parent_node.table_name,
                parent_node.parent_column_name,
                parent_node.parent_column_name_value
            )
            new_parent_children_with_children = self.my_db_navigator.get_children_with_children(parent_node.table_name)
            new_parent_parents = self.my_db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)
            parent_list_number = 1
            for new_parent in new_parents:

                id_string = ""
                node_type = NodeTypes.PARENT_LIST_NODE
                list_node_expanded_as_parent = False
                if len(primary_keys) == 1:

                    if new_parent[primary_keys[0]] != "":
                        id_string = f'({primary_keys[0]}={new_parent[primary_keys[0]]})'

                    list_node_expanded_as_parent = (
                            str(new_parent[primary_keys[0]]) == str(parent_node.parent_node.parent_node.node_id))

                node_id = new_parent[primary_keys[0]] if has_parents else ""
                parent_list_node = Node(
                    f'{parent_path}/{parent_list_number}',
                    parent_node,
                    node_type,
                    node_id,
                    None,
                    list_node_expanded_as_parent
                )

                self.add_to_tree(parent_list_node, f'{parent_node.table_name} {id_string}')

                if list_node_expanded_as_parent and not self.show_already_visited_parents:
                    continue

                self.add_children_to_tree(
                    new_parent_parents,
                    parent_list_node,
                    new_parent_columns,
                    new_parent,
                    new_parent_children_with_children,
                    parent_node.parent_column_name
                )

                parent_list_number = parent_list_number + 1

        if parent_node.node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
            column_keys, column_values = self.my_db_navigator.get_children(parent_node.table_name, parent_node.node_id)
            new_parent_children_with_children = self.my_db_navigator.get_children_with_children(parent_node.table_name)
            new_parent_parents = self.my_db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)

            self.add_children_to_tree(
                new_parent_parents,
                parent_node,
                column_keys,
                column_values[0],
                new_parent_children_with_children,
                parent_node.parent_column_name
            )

    def add_children_to_tree(
        self,
        relations_from_others,
        parent_node,
        column_keys,
        row,
        relations_to_others,
        explored_column
    ):
        for child_table_name in relations_from_others.keys():
            child_column_key = relations_from_others[child_table_name]

            child_node_type = NodeTypes.PARENT
            visited = child_column_key == explored_column

            child_path = f'{parent_node.full_path}/{child_table_name}({child_column_key}=)'
            child_node = Node(
                child_path,
                parent_node,
                child_node_type,
                parent_node.node_id,
                child_table_name,
                visited,
                child_column_key,
                parent_node.node_id,
            )
            self.add_to_tree(child_node, f'[{child_table_name}]')

            if child_node_type == NodeTypes.PARENT:
                dummy_node = Node(
                    f'{child_path}/(double-click)',
                    child_node,
                    NodeTypes.DUMMY,
                    None,
                    "dummy",
                    False,
                )
                self.add_to_tree(dummy_node, f'(double click parent to fetch)')

        for child_column_key in column_keys:

            child_column_value = row[child_column_key]

            if child_column_key in relations_to_others:
                child_table_name = relations_to_others[child_column_key]
                child_path = f'{parent_node.full_path}/{child_table_name}({child_column_key}={child_column_value})'

                node_text = f'{child_column_key}={child_column_value}'
                child_node_type = NodeTypes.CHILDREN_WITH_CHILDREN
                if child_column_value == "":
                    node_text = f'{child_column_key}'

                visited = child_column_key == explored_column

                child_node = Node(
                    child_path,
                    parent_node,
                    child_node_type,
                    child_column_value,
                    child_table_name,
                    visited,
                )
                self.add_to_tree(child_node, node_text)

                hide_child_content = visited and not self.show_already_visited_parents

                if child_node_type == NodeTypes.CHILDREN_WITH_CHILDREN and not hide_child_content:
                    dummy_node = Node(
                        f'{child_path}/(double-click)',
                        child_node,
                        NodeTypes.DUMMY,
                        visited,
                        None,
                        "dummy"
                    )
                    self.add_to_tree(dummy_node, f'(double click parent to fetch)')

            else:
                node_text = f'{child_column_key}={child_column_value}'
                child_node_type = NodeTypes.LEAF
                if child_column_value == "":
                    node_text = f'{child_column_key}'
                child_node = Node(
                    f'{parent_node.full_path}/({child_column_key}={child_column_value})',
                    parent_node,
                    child_node_type,
                    child_column_value,
                    child_column_key,
                    False,
                )
                self.add_to_tree(child_node, node_text)

    def create_new_table_tree(self, table, row_id):

        self.tree = tkb.Treeview(self.root, height=20, show="tree")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Use grid layout and sticky option
        self.root.grid_rowconfigure(1, weight=1)

        self.tree.tag_configure(NodeTypes.LEAF.name,                   foreground=self.theme.color.fg)
        self.tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN.name, foreground=self.theme.color.info)
        self.tree.tag_configure(NodeTypes.PARENT.name,                 foreground=self.theme.color.primary)
        self.tree.tag_configure(NodeTypes.PARENT_LIST_NODE.name,       foreground=self.theme.color.primary)
        self.tree.tag_configure(NodeTags.NO_VALUE,                     foreground=self.theme.color.secondary)
        self.tree.tag_configure(NodeTags.VISITED,                      foreground=self.theme.color.success)

        self.tree.bind("<<TreeviewOpen>>", self.toggle_node)
        style_name = "Custom.Treeview"
        tkb.Style().configure(style=style_name, indent=30)
        self.tree.config(style=style_name)

        root_node_path = f"{table}(id={row_id})"
        parent_root_node = Node(
            "",
            None,
            NodeTypes.DUMMY,
            None,
            "",
            False,
        )
        root_node = Node(
            root_node_path,
            parent_root_node,
            NodeTypes.CHILDREN_WITH_CHILDREN,
            row_id,
            table,
            False,
        )
        self.add_to_tree(root_node, f'{table} (id={row_id})')
        self.fetch_children(root_node_path)
        self.tree.item(root_node_path, open=True)
        dumb_node = Node(
            f'{root_node_path}/(double-click)',
            root_node,
            NodeTypes.DUMMY,
            None,
            "dummy",
            False
        )
        self.add_to_tree(dumb_node, '')

    def toggle_node(self, _):
        parent_path = self.tree.selection()[0]
        self.fetch_children(parent_path)

    def button_click(self):
        row_id = self.text_box.get("1.0", "end-1c")
        table = self.combo_box.get()
        self.create_new_table_tree(table, row_id)

    def on_enter_pressed(self, _):
        if self.text_box == self.root.focus_get():
            self.button_click()
            return 'break'  # Prevents the newline from being inserted
