from .DBCONNECTION import DBConnection
from .Products import products


class Dal:
    def __init__(self):
        self.db = DBConnection()

    def getAllProducts(self):
        query = "Select * from products"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        AllProducts = []
        for product in result:
            prod = products(product[0], product[1], product[2], product[3], product[4], product[5])
            AllProducts.append(prod)
        self.db.closeConnection()

        return AllProducts

    def checkuseremail(self, User_Email):
        query = "Select Count(email) from Customer_table where Customer_table.email =?"
        self.db.cursor.execute(query, User_Email)
        result = self.db.cursor.fetchone()
        return result[0]

    def validate_login(self, username, password, usertype):
        query = """\
            DECLARE @out int;
            EXEC [dbo].[Signin] @email= ?,@pass= ?,@type= ?, @flag=@out OUTPUT;
            SELECT @out AS the_output;
            """
        values = (username, password, usertype)
        result = self.db.executeproc(query, values)
        self.db.closeConnection()
        return result

    def register(self, username, email, password, DOB, usertype):
        query = """\
                    DECLARE @out int;
                    EXEC [dbo].[SignUp] @name= ?,@pass= ?,@mail=?,@date=?,@type= ?,@flag=@out OUTPUT;
                    SELECT @out AS the_output;
                    """
        values = (username, password, email, DOB, usertype)
        result = self.db.executeproc(query, values)
        self.db.closeConnection()
        return result
