from .DBCONNECTION import DBConnection
from .Products import products
from .Customer import customer
from .Orders import Order
from .Admin import Admin
from .SuperAdmin import superAdmin
from .Seller import Seller
from datetime import datetime


# In this Module All the Database related functions are handled
class Dal:
    # Open The Cooinection with DataBase
    def __init__(self):
        self.db = DBConnection()

    # get All the Products in the database
    def getAllProducts(self):
        query = "Select * from products"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        # Create list of products and return it
        AllProducts = []
        for product in result:
            # Set the resultant product to product object
            prod = products(product[0], product[1], product[2], product[3], product[4], product[5])
            AllProducts.append(prod)
        return AllProducts

    # Get Customer informantion from email and password
    def getuserinfo(self, email, password):
        query = "select * from Customer_table where Customer_table.email=? and Customer_table.password=?"
        values = (email, password)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        Customer_info = customer(result[0], result[1], result[2], result[4])
        self.db.closeConnection()
        return Customer_info

    # Get Userinfo by id
    def getuserinfofromId(self, Cust_Id):
        query = "select * from Customer_table where Customer_table.CustId=?"
        self.db.cursor.execute(query, Cust_Id)
        result = self.db.cursor.fetchone()
        Customer_info = customer(result[0], result[1], result[2], result[4])
        return Customer_info

    # validate Login
    def validate_login(self, username, password, usertype):
        # Query to execute Stored procedure
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

    # Register the user based upon user Type
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

    # Add the Selected item to cart
    def addtoCart(self, custid, productid):
        query = "Insert into Cart values(?,?)"
        values = (productid, custid)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Update the Customer profile
    def Update_Customer(self, username, email, password, cust_id):
        query = "Update Customer_table set cust_name=?,password=?,email=? where CustId=?"
        values = (username, password, email, cust_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # get The Cart items of the respective Customer
    def getCart(self, Cust_Id, Prod_id):
        query = "select * from Cart where customerId=? and productId=?"
        values = (Cust_Id, Prod_id)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        return result

    # Remove the items From the Cart
    def Remove_From_Cart(self, Cust_Id, Prod_id):
        query = "Delete from Cart where customerId=? and productId=?"
        values = (Cust_Id, Prod_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Clear the Whole  Cart
    def Empty_Cart(self, Cust_Id):
        query = "Delete from Cart where customerId=?"
        self.db.cursor.execute(query, Cust_Id)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Get Cart items length for specific user
    def getCartitemslength(self, Cust_Id):
        query = "select * from Cart where customerId=?"
        self.db.cursor.execute(query, Cust_Id)
        result = self.db.cursor.fetchall()
        return len(result)

    # Add the Order to DB
    def addorder(self, cust_id, addr, phoneno, order_status, price):
        proc_query = """\
                   DECLARE @out int;
                    EXEC [dbo].[insert_order] @cust_id= ?,@addr=?,@status=?,@phno=?,
                    @price=?,@order_date=?, @flag=@out OUTPUT;
                    SELECT @out AS the_output;
                   """
        order_date = datetime.today().strftime('%d-%m-%Y')
        values = (cust_id, addr, order_status, phoneno, price,order_date)
        result = self.db.executeproc(proc_query, values)
        return result

    # Add the Requested order details
    def addorderdetails(self, order_id, product_id):
        query = "Insert into orders values(?,?)"
        values = (order_id, product_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # get the Orders of the Customer
    def get_orders(self, cust_id):
        query = "select * from user_Order where custId=?"
        self.db.cursor.execute(query, cust_id)
        result = self.db.cursor.fetchall()
        orders_list = []
        for order in result:
            user_order = Order(order[0], order[1], order[2], order[3], order[4], order[5],order[6])
            orders_list.append(user_order)
        return orders_list

    # get All the products in the order
    def get_order_products(self, order_id):
        query = "select prodtsId from orders where orderid=?"
        self.db.cursor.execute(query, order_id)
        result = self.db.cursor.fetchall()
        prodids_list = []
        for ids in result:
            prodids_list.append(int(ids[0]))
        return prodids_list

    # Cancel the Customer order
    def cancel_order(self, orderid):
        query = "update user_Order set order_status='Cancelled' where order_id=?"
        self.db.cursor.execute(query, orderid)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Retrieve All the Cart items
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

    # Delete The Account of the User
    def deleteAccount(self, cusid):
        query = "Delete From Customer_table where CustId=?"
        self.db.cursor.execute(query, cusid)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Add or Edit the Review of the Order
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

    # Ban the user seller or Customer depending upon user_type
    def Ban_User(self, userId, UserType):
        if UserType == "Customer":
            query = "Select * From Customer_table where CustId=?"
        else:
            query = "Select * From Seller where seller_id=?"
        self.db.cursor.execute(query, userId)
        user_table = self.db.cursor.fetchall()
        # user Exists
        if len(user_table) > 0:
            query = "Select * From BanUser where UserId=? and userType=?"
            values = (userId, UserType)
            self.db.cursor.execute(query, values)
            result = self.db.cursor.fetchall()
            # User is not Banned Already
            if len(result) == 0:
                query = "Insert into BanUser values(?,?)"
                values = (userId, UserType)
                self.db.cursor.execute(query, values)
                self.db.cons.commit()
                if self.db.cursor.rowcount > 0:
                    return 1
                else:
                    return 0
            else:
                # User is Already Banned
                return 2
        else:
            # User Does Not Exist
            return 3

    # Ban the user seller or Customer depending upon user_type
    def Unban_User(self, userId, UserType):
        if UserType == "Customer":
            query = "Select * From Customer_table where CustId=?"
        else:
            query = "Select * From Seller where seller_id=?"
        self.db.cursor.execute(query, userId)
        user_table = self.db.cursor.fetchall()
        # user Exists
        if len(user_table) > 0:
            query = "Select * From BanUser where UserId=? and userType=?"
            values = (userId, UserType)
            self.db.cursor.execute(query, values)
            result = self.db.cursor.fetchall()
            # User is not Banned Already
            if len(result) == 0:
                # User is Not Banned
                return 2
            else:
                # Unban the user
                query = "Delete From BanUser where UserId=? and userType=?"
                values = (userId, UserType)
                self.db.cursor.execute(query, values)
                self.db.cons.commit()
                if self.db.cursor.rowcount > 0:
                    return 1
                else:
                    return 0

        else:
            # User Does Not Exist
            return 3

    # Retreive all the Emails of the Registered Customers
    def getAlluseremails(self):
        query = "Select email from Customer_table"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        Allemails = []
        for mail in result:
            Allemails.append(mail[0])
        return Allemails

    # Close the Connection with DataBase
    def CloseConnection(self):
        self.db.closeConnection()

    # Integrated WORK

    # Function for Seller information
    def getSellerinfo(self, email, password):
        query = "select * from Seller where Seller.email=? and Seller.password=?"
        values = (email, password)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        seller_info = Seller(result[0], result[1], result[2], result[4])
        self.db.closeConnection()
        return seller_info

    # Function for seller information through seller id
    def getSellerinfothroughId(self, seller_id):
        query = "select * from Seller where Seller.seller_id=?"
        self.db.cursor.execute(query, seller_id)
        result = self.db.cursor.fetchone()
        seller_info = Seller(result[0], result[1], result[2], result[4])
        return seller_info

    # function for updating information in Seller
    def Update_Seller(self, seller_name, email, password, seller_id):
        query = "update Seller set name=?,password=?,email=? where seller_id=?"
        values = (seller_name, password, email, seller_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for updating admin
    def Update_admin(self, admin_name, admin_email, admin_password, admin_id):
        query = "update Admin set admin_name=?,password=?,admin_email=? where AdminId=?"
        values = (admin_name, admin_password, admin_email, admin_id)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for updating super Admin
    def updateSuperAdmin(self, name, email, password, superAdminId):
        query = "update SuperAdmin set super_admin_name=?,password=?,super_admin_email=? where superAdminId=?"
        values = (name, password, email, superAdminId)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for getting Seller Email Information
    def getSellerEmailInformation(self):
        query = "Select email from Seller"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        Allemails = []
        for mail in result:
            Allemails.append(mail[0])
        return Allemails

        # function for getting Admin Email Information

    def getAdminEmailInformation(self):
        query = "Select admin_email from Admin"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        Allemails = []
        for mail in result:
            Allemails.append(mail[0])
        return Allemails

    # function for getting super Admin Email Information
    def getSuperAdminEmailInformation(self):
        query = "select super_admin_email from SuperAdmin"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        Allemails = []
        for mail in result:
            Allemails.append(mail[0])
        return Allemails

    # function for getting adminId information:
    def getAdminIds(self):
        query = "select AdminId from Admin"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        AllIds = []
        for adminid in result:
            print(adminid)
            AllIds.append(adminid[0])
        return AllIds

    # function for removing admin
    def removeAdmin(self, adminId):
        query = "Delete from Admin where AdminId=?"
        self.db.cursor.execute(query, adminId)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # Function to determine the length of Seller
    def getSellerProductsLength(self, seller_id):
        query = "select * from products where sellerId=?"
        self.db.cursor.execute(query, seller_id)
        result = self.db.cursor.fetchall()
        return len(result)

    # Function to find the products of Seller
    def getSellerProducts(self, seller_id):
        query = "select * from products where sellerId=?"
        self.db.cursor.execute(query, seller_id)
        result = self.db.cursor.fetchall()
        AllProducts = []
        for product in result:
            # Set the resultant product to product object
            prod = products(product[0], product[1], product[2], product[3], product[4], product[5])
            AllProducts.append(prod)
        return AllProducts

    # function for deleting a seller
    def deleteSellerAccount(self, seller_id):
        query = "Delete From Seller where seller_id=?"
        self.db.cursor.execute(query, seller_id)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for getting Admin Information:
    def getAdminInformation(self, email, password):
        query = "Select * from Admin where Admin.admin_email=? and Admin.password=?"
        values = (email, password)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        Admin_info = Admin(result[0], result[1], result[2], result[3])
        self.db.closeConnection()
        return Admin_info

    # function to get admin Information through id:
    def getAdminInfothroughid(self, admin_id):
        query = "Select * from Admin where Admin.AdminId=?"
        self.db.cursor.execute(query, admin_id)
        result = self.db.cursor.fetchone()
        Admin_info = Admin(result[0], result[1], result[2], result[3])
        return Admin_info

    # function to get Super Admin Information
    def getSuperAdminInformation(self, email, password):
        query = "select * from SuperAdmin where SuperAdmin.super_admin_email=? and SuperAdmin.password=?"
        values = (email, password)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        Super_Admin_info = superAdmin(result[0], result[1], result[2], result[3])
        return Super_Admin_info

    # function to get Super Admin Information through id
    def getSuperAdminInfofromid(self, superAdminId):
        query = "Select * from SuperAdmin where SuperAdmin.superAdminId=?"
        self.db.cursor.execute(query, superAdminId)
        result = self.db.cursor.fetchone()
        Super_Admin_info = superAdmin(result[0], result[1], result[2], result[3])
        return Super_Admin_info

    # function for adding product
    def addProduct(self, seller_id, name, product_price, product_category, image):
        query = "insert into products(sellerId,productName,price,category,productImg)" \
                "values (?,?,?,?,?)"
        values = (seller_id, name, product_price, product_category, image)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for add admin
    def addAdmin(self, adminPassword, adminName, adminEmail):
        query = "insert into Admin(password,admin_name,admin_email)" \
                "values (?,?,?)"
        values = (adminPassword, adminName, adminEmail)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for valid seller
    def checkValidSeller(self, productId, sellerId):
        query = "Select * from products where prodId=? and sellerId=?"
        values = (productId, sellerId)
        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchall()
        return len(result)

    # function for update Product
    def updateProduct(self, productId, newname, newPrice, newCategory):
        query = "Update products set productName=?,price=?,category=? where prodId=?"
        values = (newname, newPrice, newCategory, productId)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    # function for remove Product
    def removeProduct(self, product_id):
        query = "Delete from products where prodId=?"
        self.db.cursor.execute(query, product_id)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0

    def getAllorders(self):
        query = "select * from user_Order"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchall()
        orders_list = []
        for order in result:
            user_order = Order(order[0], order[1], order[2], order[3], order[4], order[5],order[6])
            orders_list.append(user_order)
        return orders_list

    def update_order_status(self,orderid,Order_status):
        query = "update user_Order set order_status=? where order_id=?"
        values = (Order_status,orderid)
        self.db.cursor.execute(query, values)
        self.db.cons.commit()
        if self.db.cursor.rowcount > 0:
            return 1
        else:
            return 0


