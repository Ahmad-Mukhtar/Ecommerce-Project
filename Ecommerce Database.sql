create database ShoppingHut

create table Seller
(
seller_id int IDEntity(1,1) not null,
name varchar(255) not null,
password varchar(255) not null,
DOB varchar(255) not null,
email varchar(255) not null,
primary key(seller_id),
)


create table Customer_table
(
CustId int IDEntity(1,1) not null,
cust_name varchar(255) not null,
password varchar(255) not null,
DOB varchar(255) not null,
email varchar(255) not null,
primary key(CustId)
)

create table user_Order
(
order_id int Identity(1,1) not null,
CustId int not null,
orderAddress varchar(255) not null,
order_status varchar(255) not null,
Phone_no bigint,
Total_price bigint,
order_date varchar(255),
primary key(order_id),
Foreign key (CustId) references Customer_table(CustId) on update cascade On delete cascade
)


create table orders
(
orderid int  not null,
prodtsId int not null,
primary key(orderid,prodtsId),
Foreign key (orderid) references user_Order(order_id) on update cascade On delete cascade
)


create table SuperAdmin
(
superAdminId int IDEntity(1,1) not null,
password varchar(255) not null,
super_admin_name varchar(255) not null,
super_admin_email varchar(255) not null,
primary key(superAdminId)
)

create table Admin
(
AdminId int IDEntity(1,1) not null,
password varchar(255) not null,
admin_name varchar(255) not null,
admin_email varchar(255) not null,
primary key(AdminId)
)

create table BanUser
(
UserId int not null,
userType varchar(255) not null,
primary key(UserId,userType)
)


create table products
(
prodId int IDEntity(1,1) not null,
sellerId int not null,
productName varchar(255) not null,
price int not null,
category varchar(255) not null,
productImg varchar(255) not null,
primary key(prodId),
Foreign key(sellerId) references Seller(seller_id) on update cascade On delete cascade
)

create table Cart
(
productId int not null,
customerId int not null,
Foreign key(customerId) references Customer_table(CustId) on update cascade On delete cascade
)
create table Reviews
(
CustId int not null,
CustReview varchar(max),
OrderId int not null,
primary key(CustId,orderId),
Foreign key(CustId) references Customer_table(CustId) on update cascade On delete cascade
)


 
select * from Customer_table
select * from Admin
select * from Seller
select * from SuperAdmin
select * from user_Order
select * from products
select * from BanUser 
select * from Cart
select * from orders
Insert into products 


go
create procedure SignUp
@name varchar(50),
@pass varchar(50),
@mail varchar(50),
@date varchar(50),
@type varchar(50),
@flag int output
as
Begin
SET NOCOUNT ON
if @type='Customer'
Begin
if Exists(select Customer_table.email from Customer_table where Customer_table.email=@mail)
Begin
set @flag=0
End
else
Begin
Insert into Customer_table(cust_name,password,DOB,email)
values(@name,@pass,@date,@mail)
commit
set @flag=1
End
End

if @type='Seller'
Begin
if Exists(select Seller.email from Seller where Seller.email=@mail)
Begin
set @flag=0
End
else
begin
Insert into Seller(name,password,DOB,email)
values(@name,@pass,@date,@mail)
commit
set @flag=1
End
End

End
go

go
create procedure Signin
@email varchar(50),
@pass varchar(50),
@type varchar(50),
@flag int output
as
BEGIN
if @type='Admin'
Begin
if Exists(select Admin.admin_email,Admin.password from Admin where Admin.admin_email=@email and Admin.password=@pass)
begin
set @flag=1
end
else
Begin
set @flag=0
End
END
else if @type='Super Admin'
BEGIN
if Exists(select SuperAdmin.super_admin_email,SuperAdmin.password from SuperAdmin where SuperAdmin.super_admin_email=@email and SuperAdmin.password=@pass)
Begin
set @flag=1
End
else
Begin
set @flag=0
End
END

else if @type='Customer'
BEGIN
if Exists(select Customer_table.email,Customer_table.password from Customer_table where Customer_table.email=@email and Customer_table.password=@pass)
Begin
if Exists(select BanUser.UserId from BanUser join Customer_table on BanUser.UserId=Customer_table.CustId where Customer_table.email=@email and Customer_table.password=@pass and BanUser.userType='Customer')
begin
set @flag=2
end
else
begin
set @flag=1
end
End
else
Begin
set @flag=0
End
END
else if @type='Seller'
BEGIN
if Exists(select Seller.email,Seller.password from Seller where Seller.email=@email and Seller.password=@pass)
Begin
if Exists(select BanUser.UserId from BanUser join Seller on BanUser.UserId=Seller.seller_id where Seller.email=@email and Seller.password=@pass and BanUser.userType='Seller')
begin
set @flag=2
end
else
begin
set @flag=1
end
End
else
Begin
set @flag=0
End
End

End
go


go
create procedure insert_order
@cust_id int,
@addr varchar(50),
@status varchar(50),
@phno bigint,
@price bigint,
@order_date varchar(255),
@flag int output
as
BEGIN
SET NOCOUNT ON
begin
Insert into user_order(CustId,orderAddress,order_status,Phone_no,Total_price,order_date)
values(@cust_id,@addr,@status,@phno,@price,@order_date)
commit
set @flag=SCOPE_IDENTITY();
end
End
go
