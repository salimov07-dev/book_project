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
select * from users
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

select * from 