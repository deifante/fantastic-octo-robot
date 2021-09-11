DROP TABLE IF EXISTS products;
CREATE TABLE products (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   price REAL NOT NULL,
   description TEXT NOT NULL,
   views INTEGER NOT NULL DEFAULT 0,
   is_deleted INTEGER NOT NULL DEFAULT 0,
   created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
