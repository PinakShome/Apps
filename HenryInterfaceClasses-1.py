#!/usr/bin/env python
# coding: utf-8

# In[5]:
"""
This script, HenryInterfaceClasses.py, defines the data models for the Henry Bookstore application.
It includes classes such as Author, Book, Branch, Category, and Publisher, which are used to represent 
and manage data throughout the application. These classes are utilized by the HenryDAO.py script for 
creating objects from database query results, allowing for an object-oriented approach to handle the data.
These models also interface with the GUI components, enabling the display and manipulation of data in a 
structured manner. Each class includes a __str__ method for easy string representation of its instances.
"""


class Author:
    """
    Author class to represent an author in the bookstore database.
    Attributes include the author's number, last name, and first name.
    """
    def __init__(self, author_num, author_last, author_first):
        self.author_num = author_num
        self.author_last = author_last
        self.author_first = author_first

    def __str__(self):
        return f"{self.author_first} {self.author_last}"

class Book:
    """
    Book class to represent a book in the bookstore database.
    Attributes include the book's title and price.
    """
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return self.title

class Branch:
    def __init__(self, name, on_hand):
        self.name = name
        self.on_hand = on_hand

    def __str__(self):
        return self.name
    
class Category:
    def __init__(self, type_):
        self.type_ = type_

    def __str__(self):
        return self.type_
    
class Publisher:
    def __init__(self, publisher_code, publisher_name, city):
        self.publisher_code = publisher_code
        self.publisher_name = publisher_name
        self.city = city

    def __str__(self):
        return self.publisher_name


# In[ ]:




