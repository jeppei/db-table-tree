import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from node.node import Node
from node_tags import NodeTags
from node_types import NodeTypes
from settings_tab import SettingsTab


class TableExplorerTree:

    def __init__(self, root, settings_tab: SettingsTab, table, row_id):

        self.nodes = {}
        self.settings_tab = settings_tab
        self.show_already_visited_parents = False

        self.tree = tkb.Treeview(root, height=20, show="tree")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Use grid layout and sticky option

        self.change_theme(self.settings_tab.settings.get_theme())

        self.tree.bind("<<TreeviewOpen>>", self.toggle_node)
        style_name = "Custom.Treeview"
        tkb.Style().configure(style=style_name, indent=30)
        self.tree.config(style=style_name)

        if table is None and row_id is None:
            return

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
        if (
                parent_node.node_type == NodeTypes.LEAF or
                parent_node.node_type == NodeTypes.DUMMY or
                parent_node.node_type == NodeTypes.PARENT_LIST_NODE
        ):
            return

        if self.tree.exists(f'{parent_path}/(double-click)'):
            self.tree.delete(f'{parent_path}/(double-click)')

        if parent_node.node_type == NodeTypes.PARENT:
            self.add_parent_rows_to_tree(parent_node, parent_path)

        if parent_node.node_type == NodeTypes.CHILDREN_WITH_CHILDREN:
            db_navigator = self.settings_tab.settings.my_db_navigator
            column_keys, column_values = db_navigator.get_children(parent_node.table_name, parent_node.node_id)
            new_parent_children_with_children = db_navigator.get_children_with_children(parent_node.table_name)
            new_parent_parents = db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)

            self.add_children_to_tree(
                new_parent_parents,
                parent_node,
                column_keys,
                column_values[0],
                new_parent_children_with_children,
                parent_node.parent_column_name
            )

    def add_parent_rows_to_tree(self, parent_node, parent_path):
        db_navigator = self.settings_tab.settings.my_db_navigator
        primary_keys = db_navigator.get_primary_key_of_table(parent_node.table_name)
        new_parent_columns, new_parents, has_parents = db_navigator.get_parents(
            parent_node.table_name,
            parent_node.parent_column_name,
            parent_node.parent_column_name_value
        )
        new_parent_children_with_children = db_navigator.get_children_with_children(parent_node.table_name)
        new_parent_parents = db_navigator.get_parent_table_names_and_column_relation(parent_node.table_name)
        parent_list_number = 1
        for new_parent in new_parents:

            parent_list_number = self.add_parent_row_to_tree(
                new_parent,
                parent_node,
                parent_path,
                has_parents,
                primary_keys,
                new_parent_children_with_children,
                new_parent_parents,
                new_parent_columns,
                parent_list_number
            )

    def add_parent_row_to_tree(
            self,
            new_parent,
            parent_node,
            parent_path,
            has_parents,
            primary_keys,
            new_parent_children_with_children,
            new_parent_parents,
            new_parent_columns,
            parent_list_number
    ):
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
            return

        self.add_children_to_tree(
            new_parent_parents,
            parent_list_node,
            new_parent_columns,
            new_parent,
            new_parent_children_with_children,
            parent_node.parent_column_name
        )
        return parent_list_number + 1

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
            self.add_child_parent_to_tree(
                child_table_name,
                child_column_key,
                parent_node,
                explored_column
            )

        for child_column_key in column_keys:

            child_column_value = row[child_column_key]

            if child_column_key in relations_to_others:
                child_table_name = relations_to_others[child_column_key]
                self.add_children_with_children_to_tree(
                    child_column_key,
                    child_table_name,
                    parent_node,
                    child_column_value,
                    explored_column
                )

            else:
                self.add_leaf_to_tree(child_column_key, child_column_value, parent_node)

    def add_child_parent_to_tree(
            self,
            child_table_name,
            child_column_key,
            parent_node,
            explored_column
    ):
        child_node_type = NodeTypes.PARENT
        visited = child_column_key == explored_column

        count_text = ""
        if parent_node.node_id is not None and parent_node.node_id != "":
            db_navigator = self.settings_tab.settings.my_db_navigator
            parent_rows_count = db_navigator.get_row_count_of_table(
                child_table_name,
                child_column_key,
                parent_node.node_id
            )
            count_text = f"({parent_rows_count})"

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
        self.add_to_tree(child_node, f'[{child_table_name}] {count_text}')

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

    def add_children_with_children_to_tree(
            self,
            child_column_key,
            child_table_name,
            parent_node,
            child_column_value,
            explored_column
    ):
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

    def add_leaf_to_tree(self, child_column_key, child_column_value, parent_node):
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

    def toggle_node(self, _):
        parent_path = self.tree.selection()[0]
        self.fetch_children(parent_path)

    def change_theme(self, theme):
        self.tree.tag_configure(NodeTypes.LEAF.name,                   foreground=theme.color.fg)
        self.tree.tag_configure(NodeTypes.CHILDREN_WITH_CHILDREN.name, foreground=theme.color.info)
        self.tree.tag_configure(NodeTypes.PARENT.name,                 foreground=theme.color.primary)
        self.tree.tag_configure(NodeTypes.PARENT_LIST_NODE.name,       foreground=theme.color.primary)
        self.tree.tag_configure(NodeTags.NO_VALUE,                     foreground=theme.color.secondary)
        self.tree.tag_configure(NodeTags.VISITED,                      foreground=theme.color.success)