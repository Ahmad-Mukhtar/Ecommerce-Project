import pyodbc


class DBConnection:
    def __init__(self):
        self.cons = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=DESKTOP-QNGQB0F\SQLEXPRESS;DATABASE=ShoppingHut; trusted_connection=YES;')
        self.cursor = self.cons.cursor()

    def executeproc(self, query, values):
        self.cursor.execute(query, values)
        flag = self.cursor.fetchone()
        return flag[0]

    def closeConnection(self):
        self.cons.close()
