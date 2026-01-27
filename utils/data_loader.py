# utils/data_loader.py
import csv
import os
from datetime import datetime

class DataLoader:
    def __init__(self, data_dir='data'):
        # Construct the absolute path to the data directory relative to the current script
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(current_script_dir, '..', data_dir)

    def _load_csv(self, filename, column_types=None):
        """
        Loads a CSV file into a list of dictionaries.
        Args:
            filename (str): The name of the CSV file.
            column_types (dict): A dictionary mapping column names to their target types (e.g., {'age': int, 'date': datetime}).
        Returns:
            list: A list of dictionaries, where each dictionary represents a row.
            list: A list of header names.
        """
        file_path = os.path.join(self.data_path, filename)
        data = []
        headers = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = [h.strip() for h in next(reader)] # Read headers from the first row

                for row_num, row in enumerate(reader):
                    if not row: # Skip empty rows
                        continue

                    item = {}
                    for i, header in enumerate(headers):
                        value = row[i].strip() if i < len(row) else '' # Handle rows potentially shorter than headers

                        # Apply type conversion if specified
                        if column_types and header in column_types:
                            try:
                                if column_types[header] == int:
                                    item[header] = int(value) if value else None
                                elif column_types[header] == float:
                                    item[header] = float(value) if value else None
                                elif column_types[header] == datetime:
                                    # Attempt to parse date in YYYY-MM-DD format
                                    item[header] = datetime.strptime(value, '%Y-%m-%d') if value else None
                                else:
                                    item[header] = value # Default to string if type not specified
                            except ValueError:
                                # Fallback to original string value if conversion fails
                                print(f"Warning: Could not convert '{value}' for column '{header}' in {filename} row {row_num + 2}. Storing as string.")
                                item[header] = value
                        else:
                            item[header] = value # Store as string if no type conversion specified

                    data.append(item)
        except FileNotFoundError:
            print(f"Error: Data file not found at {file_path}")
            return [], [] # Return empty data and headers
        except Exception as e:
            print(f"An error occurred while loading {filename}: {e}")
            return [], []

        return data, headers

    def load_customer_data(self):
        column_types = {
            'cust_id': int,
            'cust_age': int,
            'effective_start_date': datetime,
            'effective_end_date': datetime
        }
        return self._load_csv('customer_dim.csv', column_types)

    def load_product_data(self):
        column_types = {
            'product_id': int,
            'product_price': float,
            'effective_start_date': datetime,
            'effective_end_date': datetime
        }
        return self._load_csv('product_dim.csv', column_types)

    def load_sales_data(self):
        column_types = {
            'order_id': int,
            'product_id': int,
            'cust_id': int,
            'product_quantity': int,
            'order_date': datetime
        }
        return self._load_csv('sales_transactions.csv', column_types)


# Singleton DataStore to load data once and provide consistent access
class DataStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
            cls._instance.data_loader = DataLoader()
            print("Loading data...")
            # Store data and their original headers
            cls._instance.customer_data, cls._instance.customer_headers = cls._instance.data_loader.load_customer_data()
            cls._instance.product_data, cls._instance.product_headers = cls._instance.data_loader.load_product_data()
            cls._instance.sales_data, cls._instance.sales_headers = cls._instance.data_loader.load_sales_data()
            print("Data loaded.")
        return cls._instance

    def get_customer_data(self):
        return list(self.customer_data) # Return a shallow copy to prevent external modification

    def get_product_data(self):
        return list(self.product_data)

    def get_sales_data(self):
        return list(self.sales_data)

    def get_customer_headers(self):
        return list(self.customer_headers)

    def get_product_headers(self):
        return list(self.product_headers)

    def get_sales_headers(self):
        return list(self.sales_headers)