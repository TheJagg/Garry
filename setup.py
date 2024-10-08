import sqlite3
import os

# Creates users database for level progression
def create_database(file_name):
    try:
        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                    guild_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    xp INTEGER NOT NULL,
                    level_up_xp INTEGER NOT NULL
                )
            ''')
        conn.commit()
        conn.close()
        print(f"Database successfully created with a 'Users' table.")
    except Exception as e:
        print(f"Failed to create database with error: {e}")

# Creates the config.py file where you will place your bot token.
def create_config_file(file_name):
    code = '''# This file was generated by the install script.
# Tokens
token = '<Paste your Token here>'
'''
    try:
        with open(file_name, 'w') as file:
            file.write(code)
        print(f"Python file successfully generated")
    except Exception as e:
        print(f'Failed to create config script with error: {e}')

# Write all files to directory (use direct paths)
db_filepath = './cogs/levels.db'  # Update if your structure is different
py_filepath = './config.py'       # Update if your structure is different

create_database(db_filepath)
create_config_file(py_filepath)