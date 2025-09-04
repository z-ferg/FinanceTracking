-- Instantiate All Tables --
CREATE TABLE expense_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE income_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    balance DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    category_id INT NOT NULL,
    account_id INT NOT NULL,
    recur_id INT DEFAULT 0,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- View All Tables --

SELECT *
FROM accounts;

SELECT *
FROM expense_categories;

SELECT *
FROM income_categories;

SELECT *
FROM transactions;

-- Insert Starting Values --

INSERT INTO Personal_Finance_DB.income_categories(name)
VALUES
("Paycheck"),
("Allowance"),
("Other");

INSERT INTO Personal_Finance_DB.expense_categories(name)
VALUES
("Rent"),
("Utilities"),
("Groceries"),
("Transportation"),
("Entertainment"),
("Personal");

-- Deletions for Testing Purposes --

DELETE FROM transactions WHERE id != 0;