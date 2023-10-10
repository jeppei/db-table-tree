import sys

import mysql.connector  # pip install mysql-connector-python
import argparse
import os
import tkinter as tk
from tkinter import ttk


log_debug = False


def debug(*args):
    if log_debug:
        print(*args)


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
        print("Invalid environment.")
        sys.exit()

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


def add_to_tree(tree, parent_path, index, child_path, node_text, direction, tag):
    print(f'{index}: Adding {direction}: {child_path}')
    if tree.exists(child_path):
        return False
    tree.insert(
        parent_path,
        index,
        child_path,
        text=node_text,
        tags=(tag,)
    )
    return True


def get_table_data(table_name, property_value):
    if property_value == "":
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

    print(query)
    my_cursor.execute(query)
    table_data = my_cursor.fetchall()
    number_of_columns = len(my_cursor.description)
    column_keys = [i[0] for i in my_cursor.description]

    column_values = [""] * number_of_columns

    print(f'len(table_data)={len(table_data)}')
    if len(table_data) == 1:
        column_values = table_data[0]

    return column_keys, column_values


def get_table_relations_to_others(table_name):
    query = f"""
        SELECT REFERENCED_TABLE_NAME, COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
        WHERE TABLE_SCHEMA = SCHEMA()
        AND REFERENCED_TABLE_NAME IS NOT NULL
        AND TABLE_NAME = '{table_name}'
        ORDER BY REFERENCED_TABLE_NAME ASC;
    """
    print(query)
    my_cursor.execute(query)
    data = my_cursor.fetchall()

    relations = {}
    for d in data:
        relations[d[1]] = d[0]

    return relations

def get_list_of_other_tables_relating_to_this(other_table_name, other_table_column_key, other_table_column_value):
    query = f"""
        SELECT *
        FROM {other_table_name}
        WHERE {other_table_column_key}={other_table_column_value}
    """
    print(query)
    my_cursor.execute(query)
    data = my_cursor.fetchall()


def get_table_relations_from_others(table_name):
    to_this_query = f"""
        SELECT TABLE_NAME, COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
        WHERE TABLE_SCHEMA = SCHEMA()
        AND REFERENCED_TABLE_NAME IS NOT NULL
        AND REFERENCED_TABLE_NAME= '{table_name}'
        ORDER BY REFERENCED_TABLE_NAME ASC;
    """
    my_cursor.execute(to_this_query)
    data = my_cursor.fetchall()

    relations = {}
    for d in data:
        relations[d[0]] = d[1]

    return relations


def toggle_node(event):
    parent_path = tree.selection()[0]  # table1/table2/(key=value) or table1/table2(key=value)
    print(parent_path)
    tables = parent_path.split("/")  # [table1, table2, (key=value)] or [table1, table2(key=value)]
    table_and_id = tables[-1]  # (key=value) or table2(key=value)
    if table_and_id[0] == "(":  # (key=value)
        return
    parent_table_name = table_and_id.split("(")[0]  # table2
    column = table_and_id.split("(")[1][0:-1]  # key=value
    parent_column_key = column.split("=")[0]  # key
    parent_column_value = column.split("=")[1]  # value

    if tree.exists(f'{parent_path}/(double-click)'):
        tree.delete(f'{parent_path}/(double-click)')

    column_keys, column_values = get_table_data(parent_table_name, parent_column_value)
    relations_to_others = get_table_relations_to_others(parent_table_name)
    relations_from_others = get_table_relations_from_others(parent_table_name)
    print(f"relations_to_others: {relations_to_others}")

    print(f'table_name: {parent_table_name}')
    print(f'column_keys: {column_keys}')
    print(f'column_values: {column_values}')
    print(f'relations_to_others: {relations_to_others}')

    for child_table_name in relations_from_others.keys():
        child_column_key = relations_from_others[child_table_name]
        print(f'{child_table_name}: {child_column_key}')
        child_path = f'{parent_path}/{child_table_name}({child_column_key}=)'
        add_to_tree(
            tree,
            parent_path,
            1,
            child_path,
            f'id <-- [{child_table_name}.{child_column_key}]',
            "<--",
            "primary_key"
        )
        add_to_tree(
            tree,
            child_path,
            1,
            f'{child_path}/(double-click)',
            f'(double click parent to fetch)',
            "---",
            "dummy"
        )

    for i in range(len(column_keys)):

        child_column_key = column_keys[i]
        child_column_value = column_values[i]

        if child_column_key in relations_to_others:
            child_table_name = relations_to_others[child_column_key]
            child_path = f'{parent_path}/{child_table_name}({child_column_key}={child_column_value})'
            node_text = f'{child_column_key}={child_column_value}'
            if child_column_value == "":
                node_text = f'{child_column_key}'
            add_to_tree(
                tree,
                parent_path,
                1,
                child_path,
                node_text,
                "-->",
                "foreign_key"
            )
            add_to_tree(
                tree,
                child_path,
                1,
                f'{child_path}/(double-click)',
                f'(double click parent to fetch)',
                "-->",
                "dummy"
            )

        else:
            node_text = f'{child_column_key}={child_column_value}'
            if child_column_value == "":
                node_text = f'{child_column_key}'
            add_to_tree(
                tree,
                parent_path,
                1,
                f'{parent_path}/({child_column_key}={child_column_value})',
                node_text,
                "---",
                "value_key"
            )


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
tree.tag_configure('value_key', foreground='black', background='white')
tree.tag_configure('foreign_key', foreground='black', background='#cccccc')
tree.tag_configure('primary_key', foreground='black', background='#f5c84c')
tree.bind("<Double-1>", toggle_node)
tree.bind("<<TreeviewOpen>>", toggle_node)
tree.insert("", 0, f"{table}(id={row_id})", text=table, tags=("foreign_key", ))
root.mainloop()
