import argparse
import tkinter as tk
from tkinter import ttk

from db import DB
from db_navigator import DBNavigator
from node_tags import NodeTags
from node_types import NodeTypes
from node import Node


def has_no_value(variable):
    return variable is None or variable == "" or variable == "None"


class ExpandableTree:
    def __init__(self, table, row_id, env):
        self.table = table
        self.row_id = row_id
        self.env = env
        self.my_db_navigator = DBNavigator(DB(self.env))
        self.nodes = {}

        # database
        my_db_navigator = DBNavigator(DB(env))

        # create the main window with a Treeview widget
        self.root = tk.Tk()
        self.root.geometry("1000x1000")
        self.root.title("Expandable Tree")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.root, height=1000)

        # Create a Combobox widget
        all_table_names = my_db_navigator.get_all_table_names()
        self.combo_box = ttk.Combobox(self.root, values=all_table_names)
        self.combo_box.grid(row=0, column=0, padx=0, pady=0, sticky="ew")  # Use grid layout manager
        if table in self.combo_box['values']:
            self.combo_box.set(table)

        self.root.grid_rowconfigure(0, weight=0)

        # Create a Text widget
        self.text_box = tk.Text(self.root, height=1, width=50, wrap="none")
        self.text_box.insert("1.0", row_id)
        self.text_box.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")  # Use grid layout manager
        self.text_box.bind("<Return>", self.on_enter_pressed)

        # Create a button
        button = tk.Button(self.root, height=1, text="GO!", command=self.button_click)
        button.grid(row=0, column=2, padx=0, pady=0)  # Use grid layout manager

        self.root.mainloop()

    def add_to_tree(self, node, node_text):
        if self.tree.exists(node.full_path):
            return False
        print(f'{node.node_type.direction}: Adding {node.node_type.name}: {node.full_path}')
        self.nodes[node.full_path] = node

        tags = (node.node_type.name, )
        if node.node_id == "" or node.node_id is None:
            tags = tags + (NodeTags.NO_VALUE, )
        if node.visited:
            tags = tags + (NodeTags.VISITED, )

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
            new_parent_columns, new_parents = self.my_db_navigator.get_parents(
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
                            new_parent[primary_keys[0]] == parent_node.parent_node.parent_node.node_id)

                parent_list_node = Node(
                    f'{parent_path}/{parent_list_number}',
                    parent_node,
                    node_type,
                    None,
                    None,
                    list_node_expanded_as_parent
                )

                self.add_to_tree(parent_list_node, f'{parent_list_number}: {parent_node.table_name} {id_string}')

                if list_node_expanded_as_parent:
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
            self.add_to_tree(child_node, f'[{child_table_name}.{child_column_key}]')

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

                if child_node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
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

        self.tree = ttk.Treeview(self.root, height=1000)
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Use grid layout and sticky option
        self.tree.column("#0", stretch=tk.YES)  # Allow the treeview column to expand

        self.tree.tag_configure(NodeTypes.LEAF.name, background='white')
        self.tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN.name, background='#cccccc')
        self.tree.tag_configure(NodeTypes.PARENT.name, background='#f5c84c')
        self.tree.tag_configure(NodeTags.NO_VALUE, foreground='grey')
        self.tree.tag_configure(NodeTags.VISITED, foreground='grey')

        self.tree.bind("<<TreeviewOpen>>", self.toggle_node)
        style_name = "Custom.Treeview"
        ttk.Style().configure(style=style_name, indent=65)
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


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--table", nargs="?", type=str,  default="none", help="")
    cli.add_argument("--env",   nargs="?", type=str,  default="prod", help="")
    cli.add_argument("--id",    nargs="?", type=int,  default=1, help="")
    args = cli.parse_args()

    expandable_tree = ExpandableTree(
        args.table,
        args.id,
        args.env
    )
