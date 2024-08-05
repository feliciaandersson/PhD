# coding=utf-8

import os
from ase.db import connect

def find_databases(folder_path):
    """
    Find databases (files with '.db' extension) in the given folder.

    Args:
        folder_path (str): Path to the folder to search for databases.

    Returns:
        dict: A dictionary mapping index to database file names.
    """
    print("Databases found:")
    databases = {}
    for i, file in enumerate(os.listdir(folder_path)):
        if file.endswith(".db"):
            print(f"{i}: {file}")
            databases[i] = file

    return databases

def process_user_input(user_input, folder_path, databases):
    """
    Process user input to select a database file.

    Args:
        user_input (str): User input (either database ID or name).
        folder_path (str): Path to the folder containing databases.
        databases (dict): Dictionary mapping index to database file names.

    Returns:
        str or None: Absolute path of the selected database file, or None if invalid input.
    """
    if user_input.isdigit():
        selected_id = int(user_input)
        if selected_id in databases:
            database = databases[selected_id]
            input_db = os.path.join(folder_path, database)
            print(f"Selected database: {input_db}")
        else:
            return "Invalid database ID."
        
    else:
        matching_files = [file for file in databases.values() if user_input in file]

        if matching_files:
            if len(matching_files) == 1:
                input_db = os.path.join(folder_path, matching_files[0])
                print(f"Selected database: {input_db}")
            else:
                print("Multiple databases match the input. Please specify further.")
                return None
        else:
            print("Invalid database name.")
            return None

    return database, input_db


def main():
    folder_path = "./db/"
    databases = find_databases(folder_path)

    user_input = input("Enter the ID or name of the database: ")
    database, input_db_path = process_user_input(user_input, folder_path, databases)
    input_db = connect(input_db_path)

    for row in input_db.select():
        atoms = row.toatoms()
        if hasattr(row, 'name') and row.name:
            name = row.name
        else:
            print("Database row does not have a 'name'. Using name from database.")
            name = database[:-3]
            
        print(f"analyzing {name}")
            

        # Call the function(s) on what to do with the database here!


if __name__ == "__main__":
    main()