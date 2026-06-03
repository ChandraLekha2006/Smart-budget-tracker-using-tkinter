# Budget Tracker using Python Tkinter and MySQL

## Project Overview

Budget Tracker is a desktop application developed using Python, Tkinter, and MySQL. The application helps users track their income and expenses, maintain transaction records, and monitor their current balance.

The system provides a simple graphical user interface (GUI) where users can enter transaction amounts and reasons, perform cash-in and cash-out operations, and store transaction history in a MySQL database.

---

## Features

* User-friendly GUI built with Tkinter
* Record income (Cash In)
* Record expenses (Cash Out)
* Automatic balance calculation
* Store transaction history in MySQL database
* Display complete transaction history
* Save transaction history to a text file
* Low balance warning when balance falls below ₹100
* Automatic loading of previous transactions from database

---

## Technologies Used

* Python 3.x
* Tkinter (GUI)
* MySQL Database
* mysql-connector-python

---

## Software Requirements

* Python 3.x
* Visual Studio Code (optional)
* MySQL Server
* mysql-connector-python package

Install the MySQL connector using:

```bash
pip install mysql-connector-python
```

---

## Database Setup

### Create Database

```sql
CREATE DATABASE budget;
```



### Table Structure

The application automatically creates the following table:

```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    type VARCHAR(20),
    amount DECIMAL(10,2),
    reason VARCHAR(255)
);
```

---

## Project Structure

```
Budget Tracker/
│
├── budget_tracker.py 
└── README.md
```

---

## How to Run

1. Start MySQL Server.
2. Create the database named `budget`.
3. Update MySQL credentials in the Python file if required.
4. Open the project in VS Code.
5. Run the application:

```bash
python budget_tracker.py
```

---

## Working of the Application

### Cash In

* User enters an amount and reason.
* Amount is added to the current balance.
* Transaction is stored in the MySQL database.

### Cash Out

* User enters an amount and reason.
* Amount is deducted from the current balance.
* Transaction is stored in the MySQL database.

### Transaction History

* All transactions are displayed in the history section.
* History can be exported to a text file.

### Balance Monitoring

* Current balance is displayed continuously.
* Warning message appears when balance becomes low.

---

## Sample Output

```
2025-05-01 10:15:20 : Cash In - Amount: ₹5000.00 - Reason: Salary

2025-05-02 14:10:45 : Cash Out - Amount: ₹1500.00 - Reason: Food

Present Amount: ₹3500.00
```

---

## Future Enhancements

* Monthly expense reports
* Pie chart and graphical analysis
* User authentication system
* Export to Excel and PDF
* Category-wise expense tracking
* Search and filter transactions

---

## Conclusion

The Budget Tracker application provides an efficient way to manage personal finances. By combining Python Tkinter for the graphical interface and MySQL for data storage, the application offers a reliable and easy-to-use solution for tracking income, expenses, and maintaining transaction records.
