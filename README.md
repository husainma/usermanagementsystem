# User Management System

This is a simple user management system implemented in Python. It allows you to add, update, delete, and read users from an SQLite database. The passwords are hashed using bcrypt for security.

## Features
- Add new users with a valid username and password.
- Update existing users.
- Delete users.
- Read and display all users in the database

## Prerequisites
- SQLite
- bcrypt library

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/husainma/usermanagementsystem.git
    ```

2. Install requirements:
    ```bash
    pip install bcrypt
    ```
## Usage
1. Run the program:
    ```bash
    python main.py
    ```

2. Menu options:
    - 1. Add user: Prompts for a username and password, validates them, hashes the password, and adds the user to the database.
    - 2. Update user: Prompts for a user ID, and if found, allows updating the username and password.
    - 3. Delete user: Prompts for a user ID and deletes the user if found.
    - 4. Read database: Displays all users in the database.
    - 5. Exit: Exits the program.

