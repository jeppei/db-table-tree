from db import DB


def has_no_value(variable):
    return variable == "" or variable == "None" or variable is None


class DBNavigator:
    def __init__(self, db: DB):
        self._db = db

    def get_children(self, table_name, property_value):
        if property_value == "" or property_value == "None" or property_value is None:
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

        with self._db:
            resulting_rows, columns = self._db.execute_query(query)

        rows = []
        if len(resulting_rows) == 0:
            rows.append({})
            for c in range(len(columns)):
                rows[0][columns[c]] = ""
        else:
            for r in range(len(resulting_rows)):
                rows.append({})
                for c in range(len(columns)):
                    rows[r][columns[c]] = resulting_rows[r][c]

        return columns, rows

    def get_children_with_children(self, table_name):
        query = f"""
                SELECT REFERENCED_TABLE_NAME, COLUMN_NAME
                FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
                WHERE TABLE_SCHEMA = SCHEMA()
                AND REFERENCED_TABLE_NAME IS NOT NULL
                AND TABLE_NAME = '{table_name}';
        """
        with self._db:
            resulting_rows, _ = self._db.execute_query(query)

        relations = {}
        for d in resulting_rows:
            relations[d[1]] = d[0]

        return relations

    def get_primary_key_of_table(self, table_name):
        query = f"""
            SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'
        """

        with self._db:
            resulting_rows, _ = self._db.execute_query(query)

        primary_keys = []
        for row in resulting_rows:
            primary_keys.append(row[4])

        return primary_keys

    def get_parents(self, other_table_name, other_table_column_key, other_table_column_value):

        if has_no_value(other_table_column_value):
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

        with self._db:
            resulting_rows, columns = self._db.execute_query(query)

        rows = []
        if len(resulting_rows) == 0:
            rows.append({})
            for c in range(len(columns)):
                rows[0][columns[c]] = ""
        else:
            for r in range(len(resulting_rows)):
                rows.append({})
                for c in range(len(columns)):
                    rows[r][columns[c]] = resulting_rows[r][c]

        return columns, rows

    def get_parent_table_names_and_column_relation(self, table_name):
        query = f"""
                SELECT TABLE_NAME, COLUMN_NAME
                FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`
                WHERE TABLE_SCHEMA = SCHEMA()
                AND REFERENCED_TABLE_NAME IS NOT NULL
                AND REFERENCED_TABLE_NAME= '{table_name}';
        """

        with self._db:
            resulting_rows, _ = self._db.execute_query(query)

        relations = {}
        for d in resulting_rows:
            parent_table = d[0]
            parent_table_column = d[1]
            relations[parent_table] = parent_table_column

        return relations

    def get_all_table_names(self):
        query = "SHOW TABLES"

        with self._db:
            resulting_rows, _ = self._db.execute_query(query)

        table_names = []
        for row in resulting_rows:
            table_names.append(row[0])

        return table_names


