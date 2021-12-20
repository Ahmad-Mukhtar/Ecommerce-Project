from .DBCONNECTION import DBConnection
from .Products import products
from .Customer import customer
from .Orders import Order


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
        return AllProducts

    def getuserinfo(self, email, password):
        query = "select * from Customer_table where Customer_table.email=? and Customer_table.password=?"
        values = (email, password)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        Customer_info = customer(result[0], result[1], result[2], result[4])
        self.db.closeConnection()
        return Customer_info

    def getuserinfofromId(self, Cust_Id):
        query = "select * from Customer_table where Customer_table.CustId=?"
        self.db.cursor.execute(query, Cust_Id)
        result = self.db.cursor.fetchone()
        Customer_info = customer(result[0], result[1], result[2], result[4])
        return Customer_info

    def validate_login(self, username, password, usertype):
        query = """\
            DECLARE @out int;
            EXEC [dbo].[Signin] @email= ?,@pass= ?,@type= ?, @flag=@out OUTPUT;
            SELECT @out AS the_output;
            """
        values = (username, password, usertype)
        result = self.db.executeproc(query, values)
        if result != 1:
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

    def addtoCart(self, custid, productid):
        query = "Insert into Cart values(?,?)"
        values = (productid, custid)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def Update_Customer(self, username, email, password, cust_id):
        query = "Update Customer_table set cust_name=?,password=?,email=? where CustId=?"
        values = (username, password, email, cust_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def getCart(self, Cust_Id, Prod_id):
        query = "select * from Cart where customerId=? and productId=?"
        values = (Cust_Id, Prod_id)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        return result

    def Remove_From_Cart(self, Cust_Id, Prod_id):
        query = "Delete from Cart where customerId=? and productId=?"
        values = (Cust_Id, Prod_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def Empty_Cart(self, Cust_Id):
        query = "Delete from Cart where customerId=?"
        self.db.cursor.execute(query, Cust_Id)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def getCartitemslength(self, Cust_Id):
        query = "select * from Cart where customerId=?"
        self.db.cursor.execute(query, Cust_Id)
        result = self.db.cursor.fetchall()
        return len(result)

    def addorder(self, cust_id, addr, phoneno, order_status, price):
        proc_query = """\
                   DECLARE @out int;
                    EXEC [dbo].[insert_order] @cust_id= ?,@addr=?,@status=?,@phno=?,@price=?, @flag=@out OUTPUT;
                    SELECT @out AS the_output;
                   """
        values = (cust_id, addr, order_status, phoneno, price)
        result = self.db.executeproc(proc_query, values)
        return result

    def addorderdetails(self, order_id, product_id):
        query = "Insert into orders values(?,?)"
        values = (order_id, product_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def get_orders(self, cust_id):
        query = "select * from user_Order where custId=?"
        self.db.cursor.execute(query, cust_id)
        result = self.db.cursor.fetchall()
        orders_list = []
        for order in result:
            user_order = Order(order[0], order[1], order[2], order[3], order[4], order[5])
            orders_list.append(user_order)
        return orders_list

    def get_order_products(self, order_id):
        query = "select prodtsId from orders where orderid=?"
        self.db.cursor.execute(query, order_id)
        result = self.db.cursor.fetchall()
        prodids_list = []
        for ids in result:
            prodids_list.append(int(ids[0]))
        return prodids_list

    def cancel_order(self, orderid):
        query = "update user_Order set order_status='Cancelled' where order_id=?"
        self.db.cursor.execute(query, orderid)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def getCartitems(self, Cust_Id):
        query = "select * from Cart where customerId=?"
        self.db.cursor.execute(query, Cust_Id)
        cart_table = self.db.cursor.fetchall()
        AllProducts = []

        for item in cart_table:
            query = "Select * from products where prodId=?"
            self.db.cursor.execute(query, item[0])
            result = self.db.cursor.fetchall()
            prod = products(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
            AllProducts.append(prod)
        return AllProducts

    def deleteAccount(self, cusid):
        query = "Delete From Customer_table where CustId=?"
        self.db.cursor.execute(query, cusid)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def add_editReview(self, cust_id, order_id, review_txt):
        # Add review
        flag = 0
        query = "select * from Reviews where OrderId=? and CustId=?"
        values = (order_id, cust_id)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchall()
        if len(result) == 0:
            print("Iam None")
            query = "Insert into Reviews values(?,?,?)"
            values = (cust_id, review_txt, order_id)
            self.db.cursor.execute(query, values)
            self.db.cons.commit()
            return flag
        else:
            query = "Update Reviews set CustReview=? where CustId=? and OrderId=?"
            values = (review_txt, cust_id, order_id)
            self.db.cursor.execute(query, values)
            self.db.cons.commit()
            flag = 1
            return flag

    def getAlluseremails(self):
        query = "Select email from Customer_table"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        Allemails = []
        for mail in result:
            Allemails.append(mail[0])
        return Allemails

    def CloseConnection(self):
        self.db.closeConnection()
