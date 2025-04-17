use BookStore


-- Ma'lumotlar bazasini yaratish
CREATE DATABASE BookStore;
GO

-- Ma'lumotlar bazasini tanlash
USE BookStore;
GO

-- Foydalanuvchilar jadvali
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    phone NVARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Kitoblar jadvali
CREATE TABLE books (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    genre NVARCHAR(50) NOT NULL,
    stock_qty INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    added_at DATETIME DEFAULT GETDATE()
); 

-- Buyurtmalar jadvali
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10, 2) NOT NULL,
    status NVARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')) NOT NULL,
    ordered_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Buyurtma elementlari jadvali
CREATE TABLE order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT,
    book_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Inventar o'zgarishlar jadvali
CREATE TABLE inventory_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    book_id INT,
    change_qty INT NOT NULL,
    reason NVARCHAR(255) NOT NULL,
    changed_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Foydalanuvchi sharhlari jadvali
CREATE TABLE reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    book_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);


-- Foydalanuvchilar jadvaliga ma'lumotlar kiritish
INSERT INTO users (name, email, phone) VALUES
('Ali Karimov', 'ali.karimov@mail.com', '998901234567'),
('Nodira Xusanova', 'nodira.xusanova@mail.com', '998912345678'),
('Javlon Tursunov', 'javlon.tursunov@mail.com', '998931234589');

-- Kitoblar jadvaliga ma'lumotlar kiritish
INSERT INTO books (title, author, genre, stock_qty, price) VALUES
('Python for Beginners', 'John Doe', 'Programming', 100, 25.99),
('The Data Scientist Handbook', 'Jane Smith', 'Data Science', 50, 45.00),
('The Art of War', 'Sun Tzu', 'Philosophy', 200, 12.99);

-- Buyurtmalar jadvaliga ma'lumotlar kiritish
INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 25.99, 'completed'),
(2, 91.99, 'pending'),
(3, 55.99, 'cancelled');

-- Buyurtma elementlari jadvaliga ma'lumotlar kiritish
INSERT INTO order_items (order_id, book_id, quantity, price) VALUES
(1, 1, 1, 25.99),
(2, 1, 2, 25.99),
(2, 2, 1, 45.00),
(3, 2, 1, 45.00);

-- Inventar o'zgarishlar jadvaliga ma'lumotlar kiritish
INSERT INTO inventory_logs (book_id, change_qty, reason) VALUES
(1, -1, 'Sale'),
(2, -3, 'Sale'),
(3, -5, 'Sale');

-- Foydalanuvchi sharhlari jadvaliga ma'lumotlar kiritish
INSERT INTO reviews (user_id, book_id, rating, comment) VALUES
(1, 1, 5, 'Excellent book for beginners!'),
(2, 2, 4, 'Very informative, but a bit difficult to follow.'),
(3, 3, 5, 'A timeless classic!');

select * from users

select * from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'users'

select * from order_items

GO
ALTER PROCEDURE dbo.GetUserOrders 
    @user_name varchar(35)
AS
	select id,dbo.InitCap(@user_name) as user_name,total_amount,status from orders
	where user_id in (
	select id from users
	where lower(name) = @user_name) and status = 'completed'
RETURN 0 
GO
exec dbo.GetUserOrders 'ali karimov'

GO
CREATE FUNCTION dbo.InitCap (@input NVARCHAR(MAX))
RETURNS NVARCHAR(MAX)
AS
BEGIN
    DECLARE @result NVARCHAR(MAX) = '',
            @i INT = 1,
            @c CHAR(1),
            @prev CHAR(1) = ' '

    WHILE @i <= LEN(@input)
    BEGIN
        SET @c = SUBSTRING(@input, @i, 1)

        IF @prev = ' '
            SET @result = @result + UPPER(@c)
        ELSE
            SET @result = @result + LOWER(@c)

        SET @prev = @c
        SET @i = @i + 1
    END

    RETURN @result
END;
GO

select * from users
GO
CREATE PROCEDURE dbo.user_exists 
    @user_name varchar(35),
    @user_email varchar(50)
AS
	select * from users
	where name = @user_name and email = @user_email
RETURN 0 



select * from books
select * from inventory_logs
select * from order_items
select * from orders 
select * from reviews

GO
CREATE PROCEDURE dbo.get_user_info 
    @user_name varchar(35),
	@user_email varchar(45)
AS
	select id,name,email,phone from users
	where name = @user_name and email = @user_email
RETURN 0 

exec dbo.get_user_info 'Nodira Xusanova', 'nodira.xusanova@mail.com'

select * from users	
GO
CREATE PROCEDURE dbo.insert_user
    @user_name varchar(35),
	@user_email varchar(45),
	@user_phone bigint
AS
	insert into users (name,email,phone) values (@user_name,@user_email,@user_phone)
RETURN 0 

select * from users


exec dbo.insert_user 'salimov','salimov@gmail.com',9099999

GO


CREATE PROCEDURE dbo.get_user_info_v2 
    @user_name varchar(35),
	@user_email varchar(45),
	@user_phone bigint
AS
	select id,name,email,phone from users
	where name = @user_name and email = @user_email and phone = @user_phone
RETURN 0 


select id,name,email from users

update users
set name = 'Salimov Mironshoh'
where id = 7

exec dbo.get_user_info 'Javlon Tursunov','javlon.tursunov@mail.com'

select * from orders
select * from users	


select id,title,author,genre,stock_qty,price from books
where stock_qty > 0

select top 1 with ties id,title,author,genre,stock_qty,price from books
where stock_qty > 0
--order by 



GO
ALTER VIEW dbo.view_top_books
AS
with cte as(
	select top 1 with ties * from order_items
	order by quantity
), cte_2 as (
	select book_id,SUM(quantity) as sum from cte
	group by book_id
), cte_3 as(
	select top 1 with ties book_id from cte_2
	order by sum desc
)

select id,title,author,genre,stock_qty,price from books
where id in (select * from cte_3)
GO
select * from dbo.view_top_books

select * from books

select * from users



GO
CREATE PROCEDURE dbo.insert_book 
	@book_title varchar(45),
	@book_author varchar(35),
	@genre varchar(30),
	@stock_qty int,
	@price float
AS
	insert into books (title,author,genre,stock_qty,price) values (@book_title,@book_author,@genre,@stock_qty,@price)
RETURN 0 

GO
exec dbo.insert_book 

select * from books

select * from inventory_logs

select s1.id,s2.title,change_qty,reason,changed_at from inventory_logs s1
join books s2
on s1.book_id = s2.id


select id,title,author,genre,stock_qty,price from books
where stock_qty < 10




select * from users
GO
CREATE PROCEDURE dbo.get_user_orders 
	@user_email varchar(45)
AS
	select id,total_amount,status,ordered_at from orders
	where user_id = (
	select id from users
		where email = @user_email
	)
RETURN 0

exec dbo.get_user_orders 'ali.karimov@mail.com'


GO
CREATE PROCEDURE dbo.get_user_p_orders
	@user_email varchar(45)
AS
	select id,total_amount,status,ordered_at from orders
	where status = 'pending' and user_id = (
	select id from users
	where email = @user_email
)
RETURN 0

select * from users
select * from orders

exec dbo.get_user_p_orders 'nodira.xusanova@mail.com'
GO
exec dbo.get_user_p_orders
GO
CREATE PROCEDURE dbo.cancel_orders 
    @product_id int
AS
	update orders
	set status = 'cancelled'
	where id = @product_id
RETURN 0 



select * from books
select * from inventory_logs -- bu yerga tushishi kerak orderlar
select * from order_items -- bu yerga tushishi kerak orderlar
select * from orders -- bu yerga tushishi kerak orderlar
select * from reviews
select * from users
GO
CREATE TRIGGER trg_insert_inventory_log
ON order_items
AFTER INSERT
AS
BEGIN
    INSERT INTO inventory_logs (book_id, change_qty, reason, changed_at)
    SELECT book_id, -quantity, 'Sale', GETDATE()
    FROM inserted
END


select * from orders
select * from users

GO
ALTER VIEW dbo.select_top_buyers
AS
	with cte as(
	select s1.id,status,ordered_at,s5.price from users s1
	join orders s2
	on s1.id = s2.user_id
	join inventory_logs s3
	on s2.id = s3.id
	join order_items s4
	on s2.id = s4.book_id
	join books s5
	on s4.book_id = s5.id
	where ordered_at between DATEADD(MONTH,-1,getdate()) and GETDATE()
	),cte2 as (
		select top 2 with ties id,COUNT(status) as cnt from cte
		group by id
		order by cnt desc
	)

	select s2.id,s2.name,s2.email,s2.phone,cnt as 'orders_count' from cte2 s1
	join users s2
	on s1.id = s2.id

select * from dbo.select_top_buyers

select * from users
select * from books
select * from reviews

select * from books

select * from order_items
select * from inventory_logs


select * from reviews
    SELECT b.id, b.title, COUNT(r.rating) AS total_ratings, AVG(r.rating) AS avg_rating
    FROM books b
    JOIN reviews r ON b.id = r.book_id
    GROUP BY b.id, b.title
    ORDER BY total_ratings DESC, avg_rating DESC
