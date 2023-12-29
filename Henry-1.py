#!/usr/bin/env python
# coding: utf-8

# In[1]:

"""
This script creates a GUI application for managing and querying a bookstore database.
It allows users to search for books by author, category, or publisher and displays relevant information.
The GUI is built using tkinter and connects to a MySQL database through a DAO (Data Access Object) layer.
This modular design facilitates easy changes to both the GUI and the database backend.
"""


import tkinter as tk
from tkinter import ttk
from HenryDAO1 import HenryDAO # DAO class for database operations

# Class to handle the Search By Author functionality
class HenrySBA(tk.Frame):
    def __init__(self, master=None, dao=None):
        super().__init__(master)
        self.dao = dao   # Data Access Object for database interaction
        self.grid(sticky="nsew")
        self.create_widgets()  # Method to create widgets in the GUI

    def create_widgets(self):
        # Author Selection Frame
        author_frame = ttk.LabelFrame(self, text="Author Selection")
        author_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Label and combobox for selecting an author
        ttk.Label(author_frame, text="Select Author:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.authors = self.dao.getAllAuthors() # Fetch all authors from the database
        author_names = [f"{author.author_first} {author.author_last}" for author in self.authors]
        self.author_var = tk.StringVar()
        self.author_combobox = ttk.Combobox(author_frame, textvariable=self.author_var, values=author_names)
        self.author_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.author_combobox.bind("<<ComboboxSelected>>", self.on_author_selected)

        # Book Selection Frame
        book_frame = ttk.LabelFrame(self, text="Book Selection")
        book_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(book_frame, text="Select Book:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.book_var = tk.StringVar()
        self.book_combobox = ttk.Combobox(book_frame, textvariable=self.book_var)
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)

        # Book Availability Frame
        availability_frame = ttk.LabelFrame(self, text="Book Availability")
        availability_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.branches_tree = ttk.Treeview(availability_frame, columns=("Branch", "Availability"), show="headings")
        self.branches_tree.heading("Branch", text="Branch")
        self.branches_tree.heading("Availability", text="Availability")
        self.branches_tree.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Book Price Frame
        price_frame = ttk.LabelFrame(self, text="Book Price")
        price_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.price_var = tk.StringVar(value="Price: ")
        price_label = ttk.Label(price_frame, textvariable=self.price_var)
        price_label.grid(row=0, column=0, padx=5, pady=5)

        # Setting the first author as default and populating the related information
        self.author_combobox.current(0)
        self.on_author_selected(None) 

    def on_author_selected(self, event):
        print("Author selection event triggered!")
        # Event handler for when an author is selected
        selected_author_name = self.author_combobox.get()
        print("Selected author name:", selected_author_name)
        # Fetch books by the selected author and update the GUI accordingly
        selected_author = next(author for author in self.authors if f"{author.author_first} {author.author_last}" == selected_author_name) 
        books = self.dao.getBooksByAuthor(selected_author)
        print("Books for selected author:", books)

        self.book_combobox['values'] = books
        if books:
            self.book_combobox.set(books[0])  
            self.on_book_selected(None)
        else:
            self.book_combobox.set('')
            self.branches_tree.delete(*self.branches_tree.get_children())
            self.price_var.set('Price: ')

    def on_book_selected(self, event):
        selected_book_title = self.book_combobox.get()
        branches_availability = self.dao.getBookAvailability(selected_book_title)
        self.branches_tree.delete(*self.branches_tree.get_children())
        for branch, availability in branches_availability.items():
            self.branches_tree.insert("", "end", values=(branch, availability))

        price = self.dao.getBookPrice(selected_book_title)
        self.price_var.set(f'Price: ${price:.2f}')


# In[2]:


class HenrySBC(tk.Frame):
    def __init__(self, master=None, dao=None):
        super().__init__(master)
        self.dao = dao
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Category Selection Frame
        category_frame = ttk.LabelFrame(self, text="Category Selection")
        category_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(category_frame, text="Select Category:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.categories = self.dao.getAllCategories()
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(category_frame, textvariable=self.category_var, values=self.categories)
        self.category_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self.on_category_selected)

        # Book Selection Frame
        book_frame = ttk.LabelFrame(self, text="Book Selection")
        book_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(book_frame, text="Select Book:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.book_var = tk.StringVar()
        self.book_combobox = ttk.Combobox(book_frame, textvariable=self.book_var)
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)

        # Book Availability Frame
        availability_frame = ttk.LabelFrame(self, text="Book Availability")
        availability_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.branches_tree = ttk.Treeview(availability_frame, columns=("Branch", "Availability"), show="headings")
        self.branches_tree.heading("Branch", text="Branch")
        self.branches_tree.heading("Availability", text="Availability")
        self.branches_tree.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Book Price Frame
        price_frame = ttk.LabelFrame(self, text="Book Price")
        price_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.price_var = tk.StringVar(value="Price: ")
        price_label = ttk.Label(price_frame, textvariable=self.price_var)
        price_label.grid(row=0, column=0, padx=5, pady=5)

        # Setting the first category as default and populating the related information
        self.category_combobox.current(0)
        self.on_category_selected(None)
        
    def on_category_selected(self, event):
        selected_category_name = self.category_combobox.get()
        # Finding the Category instance corresponding to the selected category name
        selected_category = next(category for category in self.categories if str(category) == selected_category_name)
        books = self.dao.getBooksByCategory(selected_category)

        self.book_combobox['values'] = books
        if books:
            self.book_combobox.set(books[0])
            self.on_book_selected(None)
        else:
            self.book_combobox.set('')
            self.branches_tree.delete(*self.branches_tree.get_children())
            self.price_var.set('Average Price: ')

    def on_book_selected(self, event):
        selected_book_title = self.book_combobox.get()
        branches_availability = self.dao.getBookAvailability(selected_book_title)
        self.branches_tree.delete(*self.branches_tree.get_children())
        for branch, availability in branches_availability.items():
            self.branches_tree.insert("", "end", values=(branch, availability))

        price = self.dao.getBookPrice(selected_book_title)
        self.price_var.set(f'Price: ${price:.2f}')
        



# In[3]:


import tkinter as tk
from tkinter import ttk

class HenrySBP(tk.Frame):
    def __init__(self, master=None, dao=None):
        super().__init__(master)
        self.dao = dao
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Publisher Selection Frame
        publisher_frame = ttk.LabelFrame(self, text="Publisher Selection")
        publisher_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(publisher_frame, text="Select Publisher:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.publishers = self.dao.getAllPublishers()
        publisher_names = [publisher.publisher_name for publisher in self.publishers]
        self.publisher_var = tk.StringVar()
        self.publisher_combobox = ttk.Combobox(publisher_frame, textvariable=self.publisher_var, values=publisher_names)
        self.publisher_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.publisher_combobox.bind("<<ComboboxSelected>>", self.on_publisher_selected)

        # Book Selection Frame
        book_frame = ttk.LabelFrame(self, text="Book Selection")
        book_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(book_frame, text="Select Book:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.book_var = tk.StringVar()
        self.book_combobox = ttk.Combobox(book_frame, textvariable=self.book_var)
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)
        
        # Book Availability Frame
        availability_frame = ttk.LabelFrame(self, text="Book Availability")
        availability_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.branches_tree = ttk.Treeview(availability_frame, columns=("Branch", "Availability"), show="headings")
        self.branches_tree.heading("Branch", text="Branch")
        self.branches_tree.heading("Availability", text="Availability")
        self.branches_tree.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Book Price Frame
        price_frame = ttk.LabelFrame(self, text="Book Price")
        price_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.price_var = tk.StringVar(value="Price: ")
        price_label = ttk.Label(price_frame, textvariable=self.price_var)
        price_label.grid(row=0, column=0, padx=5, pady=5)

        # Setting the first publisher as default and populating the related information
        self.publisher_combobox.current(0)
        self.on_publisher_selected(None)
        
        

    def on_publisher_selected(self, event):
        print("Publisher selection event triggered!")
        selected_publisher_name = self.publisher_combobox.get()
        print("Selected publisher name:", selected_publisher_name)
        selected_publisher = next(publisher for publisher in self.publishers if publisher.publisher_name == selected_publisher_name)
        books = self.dao.getBooksByPublisher(selected_publisher)
        print("Books for selected publisher:", books)

        self.book_combobox['values'] = books
        if books:
            self.book_combobox.set(books[0])  
            self.on_book_selected(None)
        else:
            self.book_combobox.set('')
            
    def on_book_selected(self, event):
        selected_book_title = self.book_combobox.get()
        branches_availability = self.dao.getBookAvailability(selected_book_title)
        self.branches_tree.delete(*self.branches_tree.get_children())
        for branch, availability in branches_availability.items():
            self.branches_tree.insert("", "end", values=(branch, availability))

        price = self.dao.getBookPrice(selected_book_title)
        self.price_var.set(f'Price: ${price:.2f}')

    


# In[5]:


def main():
    # Main method to create and run the GUI application

    # Sets up the root window, tabs for each search type, and handles database connection
    
    def on_exit():
        dao.close_connection()  # Close the database connection
        root.destroy()  # Close the GUI window

    root = tk.Tk()
    root.title("Henry's Bookstore")
    
    root.protocol("WM_DELETE_WINDOW", on_exit)

    # Create the main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create the tabbed notebook
    notebook = ttk.Notebook(main_frame)

    # Create an instance of the DAO
    dao = HenryDAO()

    # Create the Search by Author (SBA) tab
    sba_frame = ttk.Frame(notebook)
    app_sba = HenrySBA(master=sba_frame, dao=dao)
    app_sba.pack(fill=tk.BOTH, expand=True)
    notebook.add(sba_frame, text="Search By Author")

    # Create the Search by Category (SBC) tab
    sbc_frame = ttk.Frame(notebook)
    app_sbc = HenrySBC(master=sbc_frame, dao=dao)
    app_sbc.pack(fill=tk.BOTH, expand=True)
    notebook.add(sbc_frame, text="Search By Category")

    # Create the Search by Publisher (SBP) tab
    sbp_frame = ttk.Frame(notebook)
    app_sbp = HenrySBP(master=sbp_frame, dao=dao)
    app_sbp.pack(fill=tk.BOTH, expand=True)
    notebook.add(sbp_frame, text="Search By Publisher")


    # Pack the notebook
    notebook.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


# In[ ]:


if __name__ == "__main__":
    main()

