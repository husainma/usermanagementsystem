import re
import sqlite3
import sys
import bcrypt

def is_valid_username(username):
    pattern = r"^[A-Za-z][A-Za-z0-9]{2,}$"
    return re.match(pattern, username) is not None

def get_username():
    while True:
        user_username = input("Enter username: ")
        if is_valid_username(user_username):
            return user_username
        else:
            print("\nUsername must be at least 3 characters long, start with a letter, and contain only letters and numbers.\n")

def is_valid_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    return re.match(pattern, password) is not None

def get_password():
    while True:
        user_password = input("Enter password: ")
        if is_valid_password(user_password):
            return user_password
        else:
            print("\nPassword must be at least 8 characters long and include at least one letter, one number, and one special character.\n")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def insert_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    print("\nUser added successfully!\n")

def has_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def update_user():
    if not has_users():
        print("\nNo users available to update.\n")
        return
    while True:
        try:
            user_id = int(input("Enter the ID of the user to update: "))
            break
        except ValueError:
            print("\nPlease enter a valid integer ID.\n")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        print(f"\nNo user found with ID: {user_id}\n")
        conn.close()
        return

    new_username = get_username()
    new_password = get_password()
    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (new_username, hashed_password, user_id))
    conn.commit()
    conn.close()
    print("\nUser updated successfully!\n")

def delete_user():
    if not has_users():
        print("\nNo users available to delete.\n")
        return
    while True:
        try:
            user_id = int(input("Enter the ID of the user to delete: "))
            break
        except ValueError:
            print("\nPlease enter a valid integer ID.\n")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        print(f"\nNo user found with ID: {user_id}\n")
    else:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        print("\nUser deleted successfully!\n")

    conn.close()

def read_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if not users:
        print("\nNo users in the database.\n")
    else:
        for user in users:
            print()
            print(f"ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"Password: {user[2]}")
        print()
    conn.close()

def initialize_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def menu():
    options = [
        "1. Add user",
        "2. Update user",
        "3. Delete user",
        "4. Read database",
        "5. Exit",
    ]

    while True:
        print("\nMenu:")
        for option in options:
            print(option)

        try:
            user_choice = int(input("\nEnter your option: "))
            match user_choice:
                case 1:
                    insert_user(get_username(), get_password())
                case 2:
                    update_user()
                case 3:
                    delete_user()
                case 4:
                    read_database()
                case 5:
                    print("Exiting program...")
                    sys.exit()
                case _:
                    print("\nEnter a valid choice\n")
        except ValueError:
            print("\nPlease enter a valid option number.\n")
        except KeyboardInterrupt:
            print("\n\nKeyboard Interrupted.")
            print("Exiting program...\n")
            sys.exit()

def main():
    initialize_db()
    menu()

if __name__ == "__main__":
    main()
