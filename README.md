# Coffee Shop Management System

## Overview

The Coffee Shop Management System is a web application designed to streamline the operations of a coffee shop. It provides functionalities for managing orders, tracking ingredients, generating sales reports, and more. The system is built using Flask for the backend, Materialize CSS for the frontend, and Chart.js for visualizing sales data.

## Features

- **Order Management**: Place orders and track the total sales.
- **Inventory Management**: Track the quantities of ingredients and update them as orders are placed.
- **Sales Reporting**: Generate daily, weekly, and monthly sales reports.
- **User-Friendly Interface**: An intuitive and mobile-friendly interface for users.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS (Materialize)
  - JavaScript (Chart.js)
  
- **Backend**:
  - Flask
  - Flask-CORS
  
- **Database**:
  - SQLite

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/coderainforever/coffeeshop.git
   cd coffeeshop
2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies:**
  ```sh
    pip install -r requirements.txt
  ```
4. Set up the database:
  ```sh
    python create_db.py
  ```
5. Run the Flask application:
  ```sh
    python app.py
  ```
**Project Structure**
```
coffeeshop/
│
├── venv/                  # Virtual environment (ignored)
├── app.py                 # Flask application
├── create_db.py           # Script to create and populate the database
├── coffeeshop.db          # SQLite database file (ignored)
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore file
├── styles.css             # Custom CSS
└── templates/             # HTML templates
    ├── index.html         # Main page
    └── sales_report.html  # Sales report page
```






