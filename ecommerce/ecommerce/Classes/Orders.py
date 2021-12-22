
class Order:
    def __init__(self ,order_id ,cust_id ,order_address ,order_status ,phoneno ,Total_price,order_date):
        self.orderid =order_id
        self.custid =cust_id
        self.order_addr =order_address
        self.order_Status =order_status
        self.phone_no =phoneno
        self.Totalprice =Total_price
        self.order_date=order_date
        self.products=""
