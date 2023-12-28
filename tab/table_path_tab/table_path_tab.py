import sys
import networkx as nx
import mysql.connector
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tkb  # sudo apt-get install python3-pil python3-pil.imagetk

from tab.settings_tab.settings_tab import SettingsTab


class TablePathTab:
    def __init__(self, root, settings_tab: SettingsTab):
        self.settings_tab = settings_tab
        self.root = root

        self.log_text = None
        self.depth_entry = None
        self.draw_all_entry = None
        self.draw_all_var = None
        self.ignore_entry = None
        self.end_table_entry = None
        self.start_table_entry = None
        self.env_entry = None

        self.result_frame = None
        self.canvas = None
        self.canvas_widget = None

        self.create_input_fields()
        self.create_graph_canvas()

    def create_input_fields(self):
        input_frame = tkb.LabelFrame(self.root, text="Input")
        input_frame.pack(padx=10, pady=10, fill='both', expand=True)
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

        pad_y_space = 5
        pad_x_space = 10

        # Entry boxes for input
        tkb.Label(input_frame, text="Start Table:").grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.start_table_entry = tkb.Entry(input_frame)
        self.start_table_entry.grid(row=0, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")

        tkb.Label(input_frame, text="End Table:").grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.end_table_entry = tkb.Entry(input_frame)
        self.end_table_entry.grid(row=1, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")

        tkb.Label(input_frame, text="Environment:").grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.env_entry = tkb.Entry(input_frame)
        self.env_entry.grid(row=2, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")
        self.env_entry.insert(0, "local")  # Default value

        tkb.Label(input_frame, text="Ignore Tables:").grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.ignore_entry = tkb.Entry(input_frame)
        self.ignore_entry.grid(row=3, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")

        tkb.Label(input_frame, text="Draw All:").grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.draw_all_var = tkb.BooleanVar()
        self.draw_all_entry = tkb.Checkbutton(input_frame, text="Draw All Nodes", variable=self.draw_all_var)
        self.draw_all_entry.grid(row=4, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")

        tkb.Label(input_frame, text="Depth:").grid(row=5, column=0, padx=10, pady=10, sticky='ew')
        self.depth_entry = tkb.Entry(input_frame)
        self.depth_entry.grid(row=5, column=1, pady=pad_y_space, padx=pad_x_space, sticky="we")
        self.depth_entry.insert(0, "5")

        # Button to create the graph
        create_button = tkb.Button(input_frame, text="Create Graph", command=self.create_graph)
        create_button.grid(row=6, column=0, pady=pad_y_space, padx=pad_x_space, sticky="we", columnspan=2)

        # Log display
        self.log_text = tkb.Text(input_frame, height=10, width=40)
        self.log_text.grid(row=7, column=0, pady=pad_y_space, padx=pad_x_space, sticky="we", columnspan=2)
        self.log_text.config(state=tkb.DISABLED)  # Make it read-only

    def create_graph_canvas(self,):

        self.result_frame = tkb.LabelFrame(self.root, text="Path")
        self.result_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.columnconfigure(1, weight=1)

        self.canvas = FigureCanvasTkAgg(plt.figure(), master=self.result_frame)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, fill='both', expand=True)

    def debug(self, message):
        self.log_text.config(state=tkb.NORMAL)
        self.log_text.insert(tkb.END, message + "\n")
        self.log_text.config(state=tkb.DISABLED)
        self.log_text.see(tkb.END)

    def create_graph(self):
        start_table = self.start_table_entry.get()
        end_table = self.end_table_entry.get()
        env = self.env_entry.get()
        ignore = self.ignore_entry.get()
        draw_all = self.draw_all_var.get()
        depth = int(self.depth_entry.get())

        self.log_text.config(state=tkb.NORMAL)
        self.log_text.delete(1.0, tkb.END)  # Clear the log
        self.log_text.insert(tkb.END, "Creating the network graph...\n")

        self.canvas.get_tk_widget().pack_forget()

        if start_table != "none" and end_table != "none":
            mydb = self.get_my_db(env)
            self.find_path(mydb, start_table, end_table, ignore, depth, draw_all)
        else:
            self.log_text.insert(tkb.END, "Please enter valid start and end tables.\n")

        self.log_text.config(state=tkb.DISABLED)


    def get_my_db(self, env):
        print("Connecting to the database")

        if env == "dev" or env == "local":
            host = os.environ['LOCAL_DATABASE_HOST']
            port = os.environ['LOCAL_DATABASE_PORT']
            database = os.environ['LOCAL_DATABASE_NAME']
            user = os.environ['LOCAL_DATABASE_USER']
            password = os.environ['LOCAL_DATABASE_PASSWORD']

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

    def find_path(self, mydb, start_table, end_table, ignore, max_depth, draw_all_nodes):
        print("Initiating variables")
        tables = [start_table]

        all_edges = {}
        previous_edge = {}
        visited = set(ignore)
        visited.add(start_table)
        iteration = 0
        depth = {start_table: 1}
        nodes_with_depth = {1: 1}
        found_end_table = False

        print("Starting DFS:")
        while len(tables) != 0:

            table = tables.pop(0)

            if depth[table] == max_depth:
                break

            if table == end_table:
                break

            query = f"""
                SELECT TABLE_NAME, REFERENCED_TABLE_NAME 
                FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE` 
                WHERE TABLE_SCHEMA = SCHEMA() 
                AND REFERENCED_TABLE_NAME IS NOT NULL 
                AND (
                    TABLE_NAME = '{table}' 
                    OR 
                    REFERENCED_TABLE_NAME= '{table}' 
                ) 
                ORDER BY REFERENCED_TABLE_NAME ASC;
            """

            my_cursor = mydb.cursor()
            my_cursor.execute(query)
            db_relations = my_cursor.fetchall()

            neighbours = set()
            for x in db_relations:
                neighbours.add(x[0])
                neighbours.add(x[1])

                if x[0] not in all_edges:
                    all_edges[x[0]] = {x[1]}

                if x[1] not in all_edges[x[0]]:
                    all_edges[x[0]].add(x[1])

                not_visited = False
                if x[0] == table and x[1] not in visited:  # x[0] = table --> x[1]
                    from_table = x[0]
                    to_table = x[1]
                    not_visited = True
                elif x[1] == table and x[0] not in visited:  # x[1] = table <-- x[0]
                    from_table = x[1]
                    to_table = x[0]
                    not_visited = True

                if not_visited:
                    d = depth[from_table] + 1
                    depth[to_table] = d
                    if d in nodes_with_depth.keys():
                        nodes_with_depth[d] += 1
                    else:
                        nodes_with_depth[d] = 1

                    visited.add(to_table)
                    tables.append(to_table)
                    previous_edge[to_table] = from_table

                if end_table in neighbours:
                    found_end_table = True
                    break

            print(
                str(iteration) + "/" +
                str(depth[table]) + " - " +
                str(table) + ": " +
                str(neighbours)
            )
            iteration += 1
            if found_end_table:
                print("The end table was found!")
                break

        print("Here are the number of nodes in each depth")
        for d in nodes_with_depth.keys():
            print(str(d) + ": " + str(nodes_with_depth[d]))

        self.create_network_graph(
            draw_all_nodes,
            nodes_with_depth,
            depth,
            visited,
            all_edges,
            start_table,
            end_table,
            previous_edge
        )

    def create_network_graph(
        self,
        draw_all_nodes,
        nodes_with_depth,
        depth,
        visited,
        all_edges,
        start_table,
        end_table,
        previous_edge
    ):
        graph = nx.DiGraph()
        if draw_all_nodes:
            print("Calculating node positions")
            y = [0] * (len(nodes_with_depth) + 1)
            for node in visited:
                x = depth[node]
                yy = y[x] - nodes_with_depth[x] / 2
                graph.add_node(node, pos=(x, yy))
                y[x] += 1

            print("Adding all edges")
            for start in all_edges.keys():
                for end in all_edges[start]:
                    graph.add_edge(start, end, color='black', weight=1)

        print("Checking if there is a path to the end table")
        end = end_table
        start = start_table
        colored_nodes = [end]
        while end != start:
            if end not in previous_edge:
                break
            previous = previous_edge[end]
            colored_nodes.append(previous)
            if end in all_edges.keys() and previous in all_edges[end]:
                graph.add_edge(end, previous, color='green', weight=4)
            else:
                graph.add_edge(previous, end, color='green', weight=4)
            end = previous
        color_map = ['green' if node in colored_nodes else '#89CFF0'
                     for node in graph]

        print("Getting all data to be able to plot the graph")
        pos = nx.get_node_attributes(graph, 'pos')
        edges = graph.edges()
        colors = [graph[u][v]['color'] for u, v in edges]
        weights = [graph[u][v]['weight'] for u, v in edges]

        if len(edges) == 0:
            print("Could not find a path from " + start + " to " + end)

        print("Drawing the graph")
        fig, ax = plt.subplots(figsize=(5, 4))
        if draw_all_nodes:
            nx.draw(
                graph,
                pos=pos,
                edge_color=colors,
                node_color=color_map,
                width=weights,
                with_labels=True,
            )
        else:
            nx.draw(
                graph,
                edge_color=colors,
                node_color=color_map,
                width=weights,
                with_labels=True,
            )

        # Embed the Matplotlib figure in a tkinter window

        self.canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, fill='both', expand=True)

