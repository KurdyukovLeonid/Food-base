import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
         )
     ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT title, description, price FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products


def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()

    connection.close()
    return user is not None


def populate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    products = [
        ('Product 1', 'Описание продукта 1', 100),
        ('Product 2', 'Описание продукта 2', 200),
        ('Product 3', 'Описание продукта 3', 300),
        ('Product 4', 'Описание продукта 4', 400),
    ]

    cursor.executemany('''
        INSERT INTO Products (title, description, price) VALUES (?, ?, ?)
    ''', products)

    connection.commit()
    connection.close()
