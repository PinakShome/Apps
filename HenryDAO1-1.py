#!/usr/bin/env python
# coding: utf-8

# In[2]:

"""
This script, HenryDAO.py, serves as the Data Access Object (DAO) for the Henry Bookstore application. 
It's responsible for all direct interactions with the MySQL database, abstracting the database operations 
from the main application logic. This script is crucial for retrieving and managing data such as authors, 
books, publishers, etc., and is used by the main application script (which includes the GUI components) to 
display this data to the user. The script uses the mysql.connector library to establish and manage database connections.
"""

import mysql.connector
from HenryInterfaceClasses import Author, Book, Branch, Category, Publisher
class HenryDAO:
        """
    HenryDAO class for handling all database interactions.
    This class encapsulates all SQL queries and provides methods for the main application
    to retrieve and manipulate data without needing to directly handle SQL statements.
    """

    def __init__(self):
        """
        Initialize the DAO class by establishing a database connection.
        """
        self.conn = self._create_connection()

    def _create_connection(self):
        """Create and return a new database connection."""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="PinakShome12",
            database="Henry")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def getAllAuthors(self):
        """
        Retrieve all authors from the database.
        Returns a list of Author objects.
        """
        with self.conn.cursor() as cursor:
            query = "SELECT HA.author_num, HA.author_last, HA.author_first FROM henry_author AS HA JOIN henry_wrote AS HW ON HA.author_num = HW.author_num GROUP BY HA.author_num, HA.author_last, HA.author_first"
            try:
                print("Executing query:", query)
                cursor.execute(query)
                results = [Author(*row) for row in cursor.fetchall()]
                print("Fetched results:", results)
                while cursor.nextset():
                    pass
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []
            
    def getBooksByAuthor(self, author):
        with self.conn.cursor() as cursor:
            query = """SELECT bk.title from henry_book as bk 
                       join henry_wrote as hw on bk.book_code=hw.book_code 
                       join henry_author as ha on ha.author_num=hw.author_num 
                       where author_last=%s and author_first=%s"""
            try:
                print("Executing query:", query)
                cursor.execute(query, (author.author_last, author.author_first))
                results = [row[0] for row in cursor.fetchall()]
                print("Fetched results:", results)
                while cursor.nextset():
                    pass
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []
            
    def getBookAvailability(self, book_title):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = """SELECT B.BRANCH_NAME, I.ON_HAND FROM HENRY_BRANCH B 
                       JOIN HENRY_INVENTORY I ON B.BRANCH_NUM = I.BRANCH_NUM 
                       JOIN HENRY_BOOK BK ON I.BOOK_CODE = BK.BOOK_CODE 
                       WHERE BK.TITLE = %s"""
            try:
                print("Executing query:", query)
                cursor.execute(query, (book_title,))
                results = {row[0]: row[1] for row in cursor.fetchall()}
                print("Fetched results:", results)
                while cursor.nextset():
                    pass
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return {}
    def getBookPrice(self, book_title):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = "SELECT price FROM henry_book WHERE title = %s"
            try:
                print("Executing query:", query)
                cursor.execute(query, (book_title,))
                result = cursor.fetchone()[0]
                print("Fetched result:", result)
                while cursor.nextset():
                    pass
                conn.close()
                return result
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return None
            
    def getAllCategories(self):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = "SELECT DISTINCT TYPE FROM henry_book"
            try:
                print("Executing query:", query)
                cursor.execute(query)
                results = [Category(row[0]) for row in cursor.fetchall()]
                print("Fetched results:", results)
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return []
            
    def getBooksByCategory(self, category):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = "SELECT TITLE FROM henry_book WHERE TYPE = %s"
            try:
                print("Executing query:", query)
                cursor.execute(query, (category.type_,))
                results = [row[0] for row in cursor.fetchall()]
                print("Fetched results:", results)
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return []
            
    def getAllPublishers(self):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = "SELECT p.PUBLISHER_CODE, p.PUBLISHER_NAME, p.CITY FROM HENRY_PUBLISHER AS p JOIN HENRY_BOOK AS b ON p.PUBLISHER_CODE = b.PUBLISHER_CODE GROUP BY p.PUBLISHER_CODE, p.PUBLISHER_NAME, p.CITY"

            try:
                print("Executing query:", query)
                cursor.execute(query)
                results = [Publisher(*row) for row in cursor.fetchall()]
                print("Fetched results:", results)
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return []
            
    def getBooksByPublisher(self, publisher):
        conn = self._create_connection()
        with conn.cursor() as cursor:
            query = "SELECT TITLE FROM henry_book WHERE PUBLISHER_CODE = %s"
            try:
                print("Executing query:", query)
                cursor.execute(query, (publisher.publisher_code,))
                results = [row[0] for row in cursor.fetchall()]
                print("Fetched results:", results)
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.close()
                return []

