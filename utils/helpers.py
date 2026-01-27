# utils/helpers.py
from datetime import datetime

def apply_pagination_and_sorting(data_list, skip=0, limit=None, order=None, order_by=None, selects=None):
    """
    Applies sorting, pagination, and column selection to a list of dictionaries.

    Args:
        data_list (list): The list of dictionaries to process.
        skip (int): Number of records to skip from the beginning.
        limit (int): Maximum number of records to return after skipping.
        order (str): 'asc' for ascending, 'desc' for descending.
        order_by (str): The key (column name) to sort by.
        selects (str): Comma-separated string of column names to include in the output.

    Returns:
        list: The processed list of dictionaries.
    """
    if not data_list:
        return []

    processed_data = list(data_list) # Work on a copy of the list

    # 1. Sorting
    if order_by and order:
        # Validate if order_by column exists in the data
        if order_by not in processed_data[0]:
            print(f"Warning: Sorting column '{order_by}' not found. Skipping sort.")
        else:
            # Custom sort key to handle None values (put None at the end for asc, start for desc)
            # and ensure proper comparison for different types (numbers, dates, strings)
            def sort_key_func(item):
                value = item.get(order_by)
                if value is None:
                    # Put None values at the end for ascending, beginning for descending
                    return (float('inf') if order == 'asc' else float('-inf'))
                return value

            processed_data.sort(key=sort_key_func, reverse=(order == "desc"))

    # 2. Pagination (Skip and Limit)
    if skip is not None and skip > 0:
        processed_data = processed_data[skip:]

    if limit is not None and limit >= 0:
        processed_data = processed_data[:limit]

    # 3. Column Selection
    if selects:
        selected_columns = [col.strip() for col in selects.split(',') if col.strip()] # Split and clean
        if not selected_columns:
            print("Warning: No valid columns specified for --selects. Returning all columns.")
            return processed_data

        # Validate selected columns against the actual keys of the first item
        available_columns = processed_data[0].keys()
        valid_selects = []
        for col in selected_columns:
            if col in available_columns:
                valid_selects.append(col)
            else:
                print(f"Warning: Selected column '{col}' does not exist in the data.")

        if not valid_selects: # If no valid columns remain after validation
            print("Warning: No valid selected columns found. Returning original data.")
            return processed_data

        result = []
        for item in processed_data:
            new_item = {col: item.get(col) for col in valid_selects}
            result.append(new_item)
        processed_data = result

    return processed_data

def print_table(data, headers=None):
    """
    Prints a list of dictionaries as a formatted table.
    If headers are not provided, it infers them from the first dictionary's keys.
    """
    if not data:
        print("No data to display.")
        return

    if headers is None:
        # Use keys from the first dictionary as headers if not provided
        headers = list(data[0].keys())

    # Calculate maximum width for each column
    column_widths = {header: len(str(header)) for header in headers}
    for row in data:
        for header in headers:
            # Handle cases where a key might be missing in a row (though data should be consistent)
            value = str(row.get(header, ''))
            column_widths[header] = max(column_widths[header], len(value))

    # Print header row
    header_line_parts = []
    for header in headers:
        header_line_parts.append(header.ljust(column_widths[header]))
    print(" | ".join(header_line_parts))

    # Print separator line
    separator_line_parts = []
    for header in headers:
        separator_line_parts.append("-" * column_widths[header])
    print("-+-".join(separator_line_parts))

    # Print data rows
    for row in data:
        row_line_parts = []
        for header in headers:
            value = str(row.get(header, '')).ljust(column_widths[header])
            row_line_parts.append(value)
        print(" | ".join(row_line_parts))