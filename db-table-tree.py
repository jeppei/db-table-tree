import sys

import mysql.connector  # pip install mysql-connector-python
import argparse
import os
import tkinter as tk
from tkinter import ttk


log_debug = True
nodes = {}


class NodeType:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction


class NodeTypes:
    CHILDREN_WITH_CHILDREN = (
        NodeType('Child with childs          ', '>>'))
    CHILDREN_WITH_CHILDREN_VISITED = (
        NodeType('Child with childs (visited)', '->'))
    PARENT = (
        NodeType('Parent                     ', '<<'))
    PARENT_VISITED = (
        NodeType('Parent (visited)           ', '<-'))
    PARENT_LIST_NODE = (
        NodeType('Parent list node           ', '<>'))
    LEAF = (
        NodeType('Leaf                       ', '--'))
    DUMMY = (
        NodeType('Dummy                      ', '..'))


class Node:
    def __init__(
        self,
        full_path,
        parent_path,
        node_type,
        node_id,
        table_name,
        column_to_other_parent=None,
        other_parent_id=-1
    ):
        self.full_path = full_path
        self.parent_path = parent_path
        self.node_type = node_type
        self.node_id = node_id
        self.table_name = table_name
        self.column_to_other_parent = column_to_other_parent
        self.other_parent_id = other_parent_id


def debug(*print_args):
    if log_debug:
        print(*print_args)


def get_my_db(env):
    debug("Connecting to the database")

    if env == "dev" or env == "local":
        host = os.environ['DATABASE_HOST']
        port = os.environ['DATABASE_PORT']
        database = os.environ['DATABASE_NAME']
        user = os.environ['DATABASE_USER']
        password = os.environ['DATABASE_PASSWORD']

    elif env == "test":
        host = os.environ['DATABASE_TEST_HOST']
        port = os.environ['DATABASE_TEST_PORT']
        database = os.environ['DATABASE_TEST_NAME']
        user = os.environ['DATABASE_TEST_USER']
        password = os.environ['DATABASE_TEST_PASSWORD']

    elif env == "prod":
        host = os.environ['DATABASE_PROD_HOST']
        port = os.environ['DATABASE_PROD_PORT']
        database = os.environ['DATABASE_PROD_NAME']
        user = os.environ['DATABASE_PROD_USER']
        password = os.environ['DATABASE_PROD_PASSWORD']

    else:
        debug("Invalid environment.")
        sys.exit()

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


def add_to_tree(node, node_text):
    debug(f'{node.node_type.direction}: Adding {node.node_type.name}: {node.full_path}')
    if tree.exists(node.full_path):
        return False
    nodes[node.full_path] = node
    tree.insert(
        node.parent_path,
        10000,
        node.full_path,
        text=node_text,
        tags=(node.node_type.name,)
    )
    return True


def get_children(table_name, property_value):
    if property_value == "" or property_value == "None" or property_value is None or property_value == -1:
        query = f"""
            select *
            from {table_name}
            limit 0
        """
    else:
        query = f"""
            select *
            from {table_name}
            where {table_name}.id={property_value}
            limit 1
        """

    debug(query)
    my_cursor.execute(query)
    table_data = my_cursor.fetchall()
    number_of_columns = len(my_cursor.description)
    column_keys = [i[0] for i in my_cursor.description]

    column_values = [""] * number_of_columns

    debug(f'len(table_data)={len(table_data)}')
    if len(table_data) == 1:
        column_values = table_data[0]

    return column_keys, column_values


def get_children_with_children(table_name):
    query = f"""
        SELECT REFERENCED_TABLE_NAME, COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
        WHERE TABLE_SCHEMA = SCHEMA()
        AND REFERENCED_TABLE_NAME IS NOT NULL
        AND TABLE_NAME = '{table_name}';
    """
    debug(query)
    my_cursor.execute(query)
    data = my_cursor.fetchall()

    relations = {}
    for d in data:
        relations[d[1]] = d[0]

    return relations


def get_parent_rows(other_table_name, other_table_column_key, other_table_column_value):

    if (
        other_table_column_value == "" or
        other_table_column_value == "None" or
        other_table_column_value is None or
        other_table_column_value == -1
    ):
        query = f"""
            SELECT *
            FROM {other_table_name}
            LIMIT 0;
        """
    else:
        query = f"""
            SELECT *
            FROM {other_table_name}
            WHERE {other_table_column_key}={other_table_column_value}
        """
    debug(query)
    my_cursor.execute(query)
    rows = my_cursor.fetchall()

    number_of_columns = len(my_cursor.description)
    columns = [i[0] for i in my_cursor.description]

    if len(rows) == 0:
        rows = [[""] * number_of_columns]

    return columns, rows


def get_parent_table_names_and_column_relation(table_name):
    to_this_query = f"""
        SELECT TABLE_NAME, COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
        WHERE TABLE_SCHEMA = SCHEMA()
        AND REFERENCED_TABLE_NAME IS NOT NULL
        AND REFERENCED_TABLE_NAME= '{table_name}';
    """
    my_cursor.execute(to_this_query)
    data = my_cursor.fetchall()

    relations = {}
    for d in data:
        parent_table = d[0]
        parent_table_column = d[1]
        relations[parent_table] = parent_table_column

    return relations


def toggle_node(event):
    parent_path = tree.selection()[0]  # table1/table2/(key=value) or table1/table2(key=value)
    parent_node = nodes[parent_path]
    debug(parent_path)
    if parent_node.node_type == NodeTypes.LEAF:
        return
    if parent_node.node_type == NodeTypes.DUMMY:
        return
    if parent_node.node_type == NodeTypes.PARENT_LIST_NODE:
        return

    if tree.exists(f'{parent_path}/(double-click)'):
        tree.delete(f'{parent_path}/(double-click)')

    if parent_node.node_type == NodeTypes.PARENT:
        new_parent_columns, new_parents = get_parent_rows(
            parent_node.table_name,
            parent_node.column_to_other_parent,
            parent_node.other_parent_id
        )
        parent_list_number = 1
        for new_parent in new_parents:
            parent_list_node = Node(
                f'{parent_path}/{parent_list_number}',
                parent_path,
                NodeTypes.PARENT_LIST_NODE,
                None,
                None,
            )
            add_to_tree(parent_list_node, f'{parent_list_number}: {parent_node.table_name}')

            child_children = get_children_with_children(parent_node.table_name)
            child_parents = get_parent_table_names_and_column_relation(parent_node.table_name)
            add_childrens_to_tree(
                child_parents,
                parent_list_node,
                new_parent_columns,
                new_parent,
                child_children,
                parent_node.column_to_other_parent
            )

            parent_list_number = parent_list_number + 1

    if parent_node.node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
        column_keys, column_values = get_children(parent_node.table_name, parent_node.node_id)
        child_children = get_children_with_children(parent_node.table_name)
        child_parents = get_parent_table_names_and_column_relation(parent_node.table_name)

        debug("")
        debug(f'table_name: {parent_node.table_name}')
        debug(f"relations_to_others: {child_children}")
        debug(f'relations_from_others: {child_parents}')
        debug(f'column_keys: {column_keys}')
        debug(f'column_values: {column_values}')

        add_childrens_to_tree(
            child_parents,
            parent_node,
            column_keys,
            column_values,
            child_children,
            parent_node.column_to_other_parent
        )


def add_childrens_to_tree(
        relations_from_others,
        parent_node,
        column_keys,
        column_values,
        relations_to_others,
        explored_column
):
    for child_table_name in relations_from_others.keys():
        child_column_key = relations_from_others[child_table_name]

        child_node_type = NodeTypes.PARENT
        if child_column_key == explored_column:
            child_node_type = NodeTypes.PARENT_VISITED

        debug(f'{child_table_name}: {child_column_key}')
        child_path = f'{parent_node.full_path}/{child_table_name}({child_column_key}=)'
        child_node = Node(
            child_path,
            parent_node.full_path,
            child_node_type,
            child_column_key,
            child_table_name,
            child_column_key,
            parent_node.node_id,
        )
        add_to_tree(child_node, f'id <-- [{child_table_name}.{child_column_key}]')

        if child_node_type == NodeTypes.PARENT:
            dummy_node = Node(f'{child_path}/(double-click)', child_path, NodeTypes.DUMMY, -1, "dummy",)
            add_to_tree(dummy_node, f'(double click parent to fetch)')

    for i in range(len(column_keys)):

        child_column_key = column_keys[i]
        child_column_value = column_values[i]

        if child_column_key in relations_to_others:
            child_table_name = relations_to_others[child_column_key]
            child_path = f'{parent_node.full_path}/{child_table_name}({child_column_key}={child_column_value})'
            node_text = f'{child_column_key}={child_column_value}'
            if child_column_value == "":
                node_text = f'{child_column_key}'

            child_node_type = NodeTypes.CHILDREN_WITH_CHILDREN
            if child_column_key == explored_column:
                child_node_type = NodeTypes.CHILDREN_WITH_CHILDREN_VISITED

            child_node = Node(
                child_path,
                parent_node.full_path,
                child_node_type,
                child_column_value,
                child_table_name
            )
            add_to_tree(child_node, node_text)

            if child_node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
                dummy_node = Node(f'{child_path}/(double-click)', child_path, NodeTypes.DUMMY, -1, "dummy")
                add_to_tree(dummy_node, f'(double click parent to fetch)')

        else:
            node_text = f'{child_column_key}={child_column_value}'
            if child_column_value == "":
                node_text = f'{child_column_key}'
            child_node = Node(
                f'{parent_node.full_path}/({child_column_key}={child_column_value})',
                parent_node.full_path,
                NodeTypes.LEAF,
                child_column_value,
                child_column_key
            )
            add_to_tree(child_node, node_text)


# parse input
cli = argparse.ArgumentParser()
cli.add_argument("--table", nargs="?", type=str,  default="none", help="")
cli.add_argument("--depth", nargs="?", type=int,  default=3, help="")
cli.add_argument("--debug", nargs="?", type=bool, default=False, help="")
cli.add_argument("--env",   nargs="?", type=str,  default="local", help="")
cli.add_argument("--id",    nargs="?", type=int,  default=1, help="")
args = cli.parse_args()
table = args.table
depth = args.depth
row_id = args.depth

# database
my_db = get_my_db(args.env)
my_cursor = my_db.cursor()

# create the main window with a Treeview widget
root = tk.Tk()
root.geometry("1000x1000")
root.title("Expandable Tree")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
tree = ttk.Treeview(root)
tree.grid(row=0, column=0, sticky="nsew")  # Use grid layout and sticky option
tree.column("#0", stretch=tk.YES)  # Allow the treeview column to expand
tree.tag_configure(NodeTypes.LEAF.name,                             foreground='black', background='white')
tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN.name,           foreground='black', background='#cccccc')
tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN_VISITED.name,   foreground='grey',  background='white')
tree.tag_configure(NodeTypes.PARENT.name,                           foreground='black', background='#f5c84c')
tree.tag_configure(NodeTypes.PARENT_VISITED.name,                   foreground='grey',  background='white')
tree.bind("<<TreeviewOpen>>", toggle_node)
style_name = "Custom.Treeview"
ttk.Style().configure(style=style_name, indent=100)
tree.config(style=style_name)

root_node_path = f"{table}(id={row_id})"
root_node = Node(root_node_path, "", NodeTypes.CHILDREN_WITH_CHILDREN, row_id, table)
add_to_tree(root_node, table)
dumb_node = Node(f'{root_node_path}/(double-click)', root_node_path, NodeTypes.DUMMY, -1, "dummy")
add_to_tree(dumb_node, '')
root.mainloop()
