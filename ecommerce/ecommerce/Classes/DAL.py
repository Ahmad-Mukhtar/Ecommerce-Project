from .DBCONNECTION import DBConnection
from .Products import products


class Dal:
    def __init__(self):
        self.db = DBConnection()

    def getAllProducts(self):
        query = "Select * from products"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        AllProducts=[]
        for product in result:
            prod=products(product[0],product[1],product[2],product[3],product[4],product[5])
            AllProducts.append(prod)

        self.db.closeConnection()

        return AllProducts
