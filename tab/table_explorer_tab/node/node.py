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
        self.full_path = full_path      # The full path to the node
        self.parent_node = parent_node  # the parent node in the tree view
        self.node_type = node_type
        self.table_name = table_name    # Table or column name of the node
        self.node_id = node_id          # The table primary key value or column value of the node

        # If the node corresponds to an existing value or not,
        # should also be null if the column value is None/null/empty string/etc

        self.exist = parent_node is None or (parent_node.exist and self.has_value(node_id))

        # For parents
        self.visited = visited
        self.parent_column_name = parent_column_name
        self.parent_column_name_value = parent_column_name_value

    @staticmethod
    def has_value(variable):
        return (
            variable is not None and
            variable != "" and
            variable != "None"
        )
