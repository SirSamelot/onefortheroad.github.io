---
layout: post
title:  "Working with SQL Databases"
subtitle:   "Getting Data Out"
date:   2017-07-02 21:26:22
author:     "Sam Wong"
header-img: "img/2017-07-02-working-with-sql-databases.jpg"
categories: tutorial pandas
comments: true
---
# Introduction

Rarely is data given to us in the form of neat CSV files.  In the real world, data can come a bewildering variety of sources.  A very common data source are the **databases** used in many companies to store, well, just about everything.  In this tutorial we will show one method of bringing data stored in a database into our Python environment.

We'll connect to a local MySQL database, but the same principles apply to other SQL databases.  MySQL is open source and freely available in a Commmunity Edition making it easy to use for learning and demonstration.

## Contents

1. [Requirements](#1-requirements)
2. [Import Libraries](#2-import-libraries)
3. [Connect to Database](#3-connect-to-database)
4. [Read from Database](#4-read-from-database)
5. [Datatypes](#5-datatypes)
6. [Cleanup](#6-cleanup)
7. [Conclusion](#conclusion)

# 1. Requirements
* MySQL Server installed
* MySQL sample database installed
* SQLAlchemy installed
* MySQL Python connector installed

Besides a running MySQL server, we'll use two additional libraries.  **SQLAlchemy** has a host of benefits that make working with databases in Python much easier, and *bonus* it plays nicely with *pandas*.  A connector is also needed so that Python can talk to the database; in our case, we will be using the **PyMySQL** connector.

You can install both these libraries with the following command:

```shell
pip install sqlalchemy pymysql
```

See [Resources](#Resources) for download links and installation instructions.

# 2. Import Libraries
From SQLAlchemy we will import just a single object, `create_engine()`, which is used to build our connection to MySQL.


```python
from sqlalchemy import create_engine
import pandas as pd

pd.set_option('display.width', 1000)
```

# 3. Connect to Database
Let's assume the following:
- the MySQL server has a user `sam` with password `secret`
- the MySQL server is located at `localhost` on the (default) port of `3306`
- the database we are connecting to is named `employees`, and the user `sam` has privileges on this database

SQLAlchemy and PyMySQL is used to create the connection to the database; the exact connect string depends on what database and driver combo you are using.  For the officially documented SQLAlchemy and MySQL combinations connect strings, click [here](http://docs.sqlalchemy.org/en/latest/dialects/mysql.html).


```python
# MySQL connect
user = 'sam'
password = 'secret'
host = 'localhost'
port = '3306'
dbname = 'employees'

mysql_engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + port + '/' + dbname)

conn = mysql_engine.connect()
```

> An example of a **Teradata** connect string: `td_engine = create_engine('teradata://sam:secret@localhost:22/)`
{:.blockquote}

Unless something goes wrong, nothing obvious happens after the connection is created.  But now we can use the connection object `conn` directly in *pandas*!

# 4. Read from Database
We are going to use the MySQL command `SHOW TABLES` to list all the tables in the current database.  Thanks to the magic of SQLAlchemy and *pandas*, we can pass SQL commands to the connection object using `pandas.read_sql()`:


```python
print(pd.read_sql('SHOW TABLES', conn))
```

        Tables_in_employees
    0      current_dept_emp
    1           departments
    2              dept_emp
    3  dept_emp_latest_date
    4          dept_manager
    5             employees
    6              salaries
    7                titles


Notice two things:
- the typical semicolon `;` is not required to end the SQL statement
- `read_sql()` converts the table directly into a dataframe

See what I mean about SQLAlchemy and *pandas* playing nice together?

If we want to look more closely at a specific table, we can use the following command:


```python
print(pd.read_sql('departments', conn))
```

      dept_no           dept_name
    0    d009    Customer Service
    1    d005         Development
    2    d002             Finance
    3    d003     Human Resources
    4    d001           Marketing
    5    d004          Production
    6    d006  Quality Management
    7    d008            Research
    8    d007               Sales


The line above read the entire `departments` table.  It is the *pandas* equivalent of the SQL query `SELECT * FROM departments`.

> `pd.read_sql('SELECT * FROM departments', conn)` would have done the same thing, just with more typing.
{:.blockquote}

# 5. Datatypes
Let's read another table in and take a closer look at the datatypes.


```python
df = pd.read_sql('employees', conn)
print(df.head())
```

       emp_no birth_date first_name last_name gender  hire_date
    0   10001 1953-09-02     Georgi   Facello      M 1986-06-26
    1   10002 1964-06-02    Bezalel    Simmel      F 1985-11-21
    2   10003 1959-12-03      Parto   Bamford      M 1986-08-28
    3   10004 1954-05-01  Chirstian   Koblick      M 1986-12-01
    4   10005 1955-01-21    Kyoichi  Maliniak      M 1989-09-12



```python
print(df.info())
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 300024 entries, 0 to 300023
    Data columns (total 6 columns):
    emp_no        300024 non-null int64
    birth_date    300024 non-null datetime64[ns]
    first_name    300024 non-null object
    last_name     300024 non-null object
    gender        300024 non-null object
    hire_date     300024 non-null datetime64[ns]
    dtypes: datetime64[ns](2), int64(1), object(3)
    memory usage: 13.7+ MB
    None


In most cases, *pandas* can correctly deduce the type of each column.  For example, it knows that the `emp_no` is of type `int64`, `birthdate` is of type `datetime64`, etc.  In the cases where the type can't be deduced (perhaps there are a lot of `NULL` values in the first few rows of data that *pandas*  looks at), you can pass in additional parameters to `read_sql()` like `coerce_float` and `parse_dates`.

# 6. Cleanup
Once you've finished accessing the database, it's good practice to release any connections back to the pool and to explicitly dispose of the engine object.


```python
conn.close()
mysql_engine.dispose()
```

# Conclusion
*pandas* and **SQLAlchemy** make it easy to work with databases.  You don't even need to write any SQL at all!  (Although I still recommend knowing *some* SQL due to its ubiquity.)  So can you completely rely on *pandas* and forget about SQL?  I would say no.  Both tools have their strengths, and the deciding factor has as much to do with your intended application as it does with your comfort level using the tool.  So as always, keep trying, breaking, and fixing. Thanks for reading!

> Have a question about this topic, or a suggestion for a future topic?  Please, leave a comment below!
{:.blockquote}

### Resources
- [MySQL Community Edition](https://www.mysql.com/products/community/)
- MySQL [Employees](https://dev.mysql.com/doc/employee/en/) sample database
- SQLAlchemy
- PyMySQL
- *pandas* [comparison with SQL](https://pandas.pydata.org/pandas-docs/stable/comparison_with_sql.html)
