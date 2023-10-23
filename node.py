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
