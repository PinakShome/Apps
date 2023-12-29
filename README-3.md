# Book-Store-App
Modular Henry Bookstore manager with GUI and database layers, built for flexible UI/database interchangeability.

# Overview

The Henry Bookstore Application is a GUI-based tool for managing and querying a bookstore database. This application allows users to search for books by authors, categories, or publishers and displays relevant information such as book availability, price, and more. The application is built using Python and interfaces with a MySQL database.

 # Technical Components

The application consists of three main Python scripts, each serving a distinct role:

- **HenryDAO.py**
  - **Purpose**: Acts as the Data Access Object (DAO) for the application.
  - **Functionality**: Manages all direct interactions with the MySQL database.
  - **Details**: Contains methods to perform database operations like fetching all authors, books by a specific author, book availability, etc.
  - **Database Connection**: Uses `mysql.connector` to establish and manage database connections.

- **HenryInterfaceClasses.py**
  - **Purpose**: Defines the data models used in the application.
  - **Classes**: Includes `Author`, `Book`, `Branch`, `Category`, and `Publisher`.
  - **Usage**: These models are instantiated by `HenryDAO.py` when fetching data from the database. They represent and manage data in an object-oriented manner.
  - **String Representation**: Each class has a `__str__` method for easy string representation of its instances, aiding in displaying data in the GUI.

- **Main Application Script** (e.g., `Henry-1.py`)
  - **Purpose**: Provides the GUI for the application.
  - **Technology**: Uses `tkinter` for the graphical user interface.
  - **Integration**: Utilizes `HenryDAO.py` for database operations and `HenryInterfaceClasses.py` for data representation.
  - **Features**: Allows users to select authors, categories, or publishers from dropdown menus and displays relevant information such as book titles, availability, and prices.

# How to Run the Application

- To run the Henry Bookstore Application:

  - Ensure Python and mysql.connector are installed on your system.
  - Set up a MySQL database named "Henry" and configure it as per the application's requirements.
  - Clone/download the repository containing the three scripts.
  - Execute the main application script (e.g., Henry-1.py).
  - The GUI should launch, allowing you to interact with the Henry Bookstore database.

# Dependencies
 - Python (3.x recommended)
 - mysql.connector
 - MySQL Database

## Additional Notes
Before running the application, ensure the database connection details in HenryDAO.py (such as host, user, password) are correctly set for your MySQL setup. The application is designed with a modular approach, allowing for easy updates to the GUI or database backend without extensive reworking of the entire codebase.
