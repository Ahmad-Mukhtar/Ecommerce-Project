

class products:
    def __init__(self,productid,sellerid,prodname,price,category,prodimage):
        self.prodid=productid
        self.sellerid=sellerid
        self.prodname=prodname
        self.__price=price
        self.category=category
        self.prodimg=prodimage

    def getprice(self):
        return self.__price


