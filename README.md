# BookstoreManagementSystem

A simple bookstore management system is developed by using Python.

The repository contains two main folders as **application** and **database**. 

- **application** folder contains **app.py** file which is the source code of the bookstore management system developed in Python. 
- **database** folder contains **bookstore.sql** file which is the dump file for the bookstore database used for bookstore management system. At database desing phase, normalization steps are followed. So, the bookstore database is in the 3NF form. 
- **database** folder also includes **EntityRelationDiagram.jpg** file which shows the relationships between tables and columns in the bookstore database. 

In the context of the bookstore management system, it is assumed that:
- only new users will be registered
- only new orders will be added
- only stocks will be updated
- new books will not be added
- existing books will not be deleted

In order to launch the bookstore management system the app.py and bookstore.sql files should be downloaded. bookstore.sql file should be used so as to create the database. Then the connection should be set. After that the app.py should be run by taking into account the credentials of the database connection.
