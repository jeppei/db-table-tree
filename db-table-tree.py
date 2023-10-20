import argparse
import tkinter as tk
from tkinter import ttk

from db import DB
from db_navigator import DBNavigator

nodes = {}


class NodeType:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction


class NodeTypes:
    CHILDREN_WITH_CHILDREN = (
        NodeType('Child with children',               '>>'))
    PARENT = (
        NodeType('Parent',                            '<<'))
    PARENT_LIST_NODE = (
        NodeType('Parent list node',                  '<>'))
    LEAF = (
        NodeType('Leaf',                              '--'))
    DUMMY = (
        NodeType('Dummy',                             '..'))


class NodeTags:
    NO_VALUE = "NoValue"
    VISITED = "Visited"


class Node:
    def __init__(
        self,
        full_path,
        parent_node,
        node_type,
        node_id,
        table_name,
        visited,
        parent_column_name=None,
        parent_column_name_value=None,
    ):
        self.full_path = full_path
        self.parent_node = parent_node
        self.node_type = node_type
        self.node_id = node_id
        self.table_name = table_name
        self.visited = visited

        # For parents
        self.parent_column_name = parent_column_name
        self.parent_column_name_value = parent_column_name_value


def add_to_tree(node, node_text):
    if tree.exists(node.full_path):
        return False
    print(f'{node.node_type.direction}: Adding {node.node_type.name}: {node.full_path}')
    nodes[node.full_path] = node

    tags = (node.node_type.name, )
    if node.node_id == "" or node.node_id is None:
        tags = tags + (NodeTags.NO_VALUE, )
    if node.visited:
        tags = tags + (NodeTags.VISITED, )

    tree.insert(
        node.parent_node.full_path,
        10000,
        node.full_path,
        text=node_text,
        tags=tags
    )
    return True


def has_no_value(variable):
    return variable is None or variable == "" or variable == "None"


def toggle_node(event):
    parent_path = tree.selection()[0]
    fetch_children(parent_path)


def fetch_children(parent_path):
    message = f'# Expanding on {parent_path} #'
    line = '#' * len(message)
    print(f'\n{line}\n{message}\n{line}\n')
    parent_node = nodes[parent_path]
    if parent_node.node_type == NodeTypes.LEAF:
        return
    if parent_node.node_type == NodeTypes.DUMMY:
        return
    if parent_node.node_type == NodeTypes.PARENT_LIST_NODE:
        return

    if tree.exists(f'{parent_path}/(double-click)'):
        tree.delete(f'{parent_path}/(double-click)')

    if parent_node.node_type == NodeTypes.PARENT:
        primary_keys = my_db_navigator.get_primary_key_of_table(parent_node.table_name)
        new_parent_columns, new_parents = my_db_navigator.get_parents(
            parent_node.table_name,
            parent_node.parent_column_name,
            parent_node.parent_column_name_value
        )
        new_parent_children_with_children = my_db_navigator.get_children_with_children(parent_node.table_name)
        new_parent_parents = my_db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)
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

            add_to_tree(parent_list_node, f'{parent_list_number}: {parent_node.table_name} {id_string}')

            if list_node_expanded_as_parent:
                continue

            add_children_to_tree(
                new_parent_parents,
                parent_list_node,
                new_parent_columns,
                new_parent,
                new_parent_children_with_children,
                parent_node.parent_column_name
            )

            parent_list_number = parent_list_number + 1

    if parent_node.node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
        column_keys, column_values = my_db_navigator.get_children(parent_node.table_name, parent_node.node_id)
        new_parent_children_with_children = my_db_navigator.get_children_with_children(parent_node.table_name)
        new_parent_parents = my_db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)

        # print("")
        # print(f'table_name: {parent_node.table_name}')
        # print(f"relations_to_others: {child_children}")
        # print(f'relations_from_others: {child_parents}')
        # print(f'column_keys: {column_keys}')
        # print(f'column_values: {column_values}')

        add_children_to_tree(
            new_parent_parents,
            parent_node,
            column_keys,
            column_values[0],
            new_parent_children_with_children,
            parent_node.parent_column_name
        )


def add_children_to_tree(
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
        add_to_tree(child_node, f'[{child_table_name}.{child_column_key}]')

        if child_node_type == NodeTypes.PARENT:
            dummy_node = Node(
                f'{child_path}/(double-click)',
                child_node,
                NodeTypes.DUMMY,
                None,
                "dummy",
                False,
            )
            add_to_tree(dummy_node, f'(double click parent to fetch)')

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
            add_to_tree(child_node, node_text)

            if child_node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
                dummy_node = Node(
                    f'{child_path}/(double-click)',
                    child_node,
                    NodeTypes.DUMMY,
                    visited,
                    None,
                    "dummy"
                )
                add_to_tree(dummy_node, f'(double click parent to fetch)')

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
            add_to_tree(child_node, node_text)


global my_db_navigator, tree


def main():
    global my_db_navigator, tree
    # parse input
    cli = argparse.ArgumentParser()
    cli.add_argument("--table", nargs="?", type=str,  default="none", help="")
    cli.add_argument("--env",   nargs="?", type=str,  default="prod", help="")
    cli.add_argument("--id",    nargs="?", type=int,  default=1, help="")
    args = cli.parse_args()
    table = args.table
    row_id = args.id

    # database
    my_db_navigator = DBNavigator(DB(args.env))

    # create the main window with a Treeview widget
    root = tk.Tk()
    root.geometry("1000x1000")
    root.title("Expandable Tree")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a Combobox widget
    values = ["Option 1", "Option 2", "Option 3"]
    combo_box = ttk.Combobox(root, values=values)
    combo_box.grid(row=0, column=0, padx=0, pady=0, sticky="ew")  # Use grid layout manager
    root.grid_rowconfigure(0, weight=0)

    # Create a Text widget
    text_box = tk.Text(root, height=1, width=50)
    text_box.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")  # Use grid layout manager

    # Create the tree
    tree = ttk.Treeview(root)
    tree.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Use grid layout and sticky option
    tree.column("#0", stretch=tk.YES)  # Allow the treeview column to expand

    tree.tag_configure(NodeTypes.LEAF.name, background='white')
    tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN.name, background='#cccccc')
    tree.tag_configure(NodeTypes.PARENT.name, background='#f5c84c')
    tree.tag_configure(NodeTags.NO_VALUE, foreground='grey')
    tree.tag_configure(NodeTags.VISITED, foreground='grey')

    tree.bind("<<TreeviewOpen>>", toggle_node)
    style_name = "Custom.Treeview"
    ttk.Style().configure(style=style_name, indent=65)
    tree.config(style=style_name)

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
    add_to_tree(root_node, f'{table} (id={row_id})')
    fetch_children(root_node_path)
    tree.item(root_node_path, open=True)
    dumb_node = Node(
        f'{root_node_path}/(double-click)',
        root_node,
        NodeTypes.DUMMY,
        None,
        "dummy",
        False
    )
    add_to_tree(dumb_node, '')

    root.mainloop()


if __name__ == "__main__":
    main()
