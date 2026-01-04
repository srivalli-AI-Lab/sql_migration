import os
import json

def load_schema(file_path="data/mortgage.txt"):
    """Load the database schema from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Schema file {file_path} not found.")
    with open(file_path, "r") as f:
        return f.read()
    
def load_old_schema(file_path="data/old_mortgage.txt"):
    """Load the old database schema from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Old schema file {file_path} not found.")
    with open(file_path, "r") as f:
        return f.read() 
    
def load_mapping(file_path="data/column_mapping.json"):
    """
    Load the column mapping from a JSON file.
    Returns a dictionary mapping old column names to new column names.
    
    Args:
        file_path (str): Path to the column mapping JSON file (default: 'data/column_mapping.json').
    
    Returns:
        dict: Dictionary of old_column -> new_column mappings.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not valid JSON or has an incorrect format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Column mapping file {file_path} not found.")
    
    with open(file_path, "r") as f:
        try:
            mapping = json.load(f)
            if not isinstance(mapping, dict):
                raise ValueError("Column mapping file must contain a JSON object with key-value pairs.")
            return mapping
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {str(e)}")
        

def load_tbl_mapping(file_path="data/table_mapping.json"):
    """
    Load the table mapping from a JSON file.
    Returns a dictionary mapping old table names to new table names.
    
    Args:
        file_path (str): Path to the table mapping JSON file (default: 'data/table_mapping.json').

    Returns:
        dict: Dictionary of old_table -> new_table mappings.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not valid JSON or has an incorrect format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Table mapping file {file_path} not found.")

    with open(file_path, "r") as f:
        try:
            mapping = json.load(f)
            if not isinstance(mapping, dict):
                raise ValueError("Table mapping file must contain a JSON object with key-value pairs.")
            return mapping
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {str(e)}")
