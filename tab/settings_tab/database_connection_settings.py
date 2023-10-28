import ttkbootstrap as tkb

class DatabaseConnectionSettings:

    def __init__(self, name, host, port, database, user, password):
        self.name = tkb.StringVar()
        self.host = tkb.StringVar()
        self.port = tkb.StringVar()
        self.database = tkb.StringVar()
        self.user = tkb.StringVar()
        self.password = tkb.StringVar()

        self.name.set(name)
        self.host.set(host)
        self.port.set(port)
        self.database.set(database)
        self.user.set(user)
        self.password.set(password)

