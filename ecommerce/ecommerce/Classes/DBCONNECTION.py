import pyodbc


# This is the Helping module for Handling Connections

class DBConnection:
    # Connect With database
    def __init__(self):
        self.cons = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=DESKTOP-QNGQB0F\SQLEXPRESS;DATABASE=ShoppingHut; trusted_connection=YES;')
        self.cursor = self.cons.cursor()

    # Execute Procedure and return output
    def executeproc(self, query, values):
        self.cursor.execute(query, values)
        flag = self.cursor.fetchone()
        return flag[0]

    # Close the Connection with DataBase
    def closeConnection(self):
        self.cons.close()
