# utils/cli_parser.py
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Python CLI for Sales Data Analysis")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # --- Common Pagination and Sorting Arguments (Helper Function) ---
    def add_common_list_args(parser_obj):
        parser_obj.add_argument("--skip", type=int, default=0,
                                help="Number of records to skip (for pagination).")
        parser_obj.add_argument("--limit", type=int, default=None,
                                help="Maximum number of records to return (for pagination).")
        parser_obj.add_argument("--order", choices=["asc", "desc"], default=None,
                                help="Order of sorting: 'asc' (ascending) or 'desc' (descending).")
        parser_obj.add_argument("--order-by", type=str, default=None,
                                help="Column name to sort the results by.")
        parser_obj.add_argument("--selects", type=str, default=None,
                                help="Comma-separated list of columns to display (e.g., 'col1,col2').")

    # --- Customer Commands ---
    customer_parser = subparsers.add_parser("customers", help="Customer related operations.")
    customer_subparsers = customer_parser.add_subparsers(dest="customer_command", help="Customer commands", required=True)

    # Command: customers total-by-location --location "Los Angeles, CA"
    total_by_location_parser = customer_subparsers.add_parser(
        "total-by-location", help="Provide the total number of customers by location."
    )
    total_by_location_parser.add_argument("--location", type=str, required=True,
                                         help="Specify the customer location (e.g., 'Los Angeles, CA').")

    # Command: customers from-multiple-locations --locations "Los Angeles, CA" "New York City, NY"
    from_multiple_locations_parser = customer_subparsers.add_parser(
        "from-multiple-locations", help="Find customers from multiple locations."
    )
    from_multiple_locations_parser.add_argument("--locations", type=str, nargs='+', required=True,
                                                help="Specify multiple customer locations (space-separated).")
    add_common_list_args(from_multiple_locations_parser) # Apply common args

    # Command: customers list --age 15 --address "Meadow St" --date 1900-01-01 --skip 0 --limit 10 --order asc --order-by cust_id --selects cust_id,cust_address
    list_customers_parser = customer_subparsers.add_parser(
        "list", help="List customers based on specified data (age, address, date)."
    )
    list_customers_parser.add_argument("--age", type=int, help="Filter customers by exact age.")
    list_customers_parser.add_argument("--address", type=str, help="Filter customers by partial address match (case-insensitive).")
    list_customers_parser.add_argument("--date", type=str,
                                        help="Filter customers by effective date (YYYY-MM-DD). Checks if the date falls within effective_start_date and effective_end_date.")
    add_common_list_args(list_customers_parser) # Apply common args

    # Command: customers top-orders --order desc
    top_customers_orders_parser = customer_subparsers.add_parser(
        "top-orders", help="List the top 10 customers with the most orders."
    )
    top_customers_orders_parser.add_argument("--order", choices=["asc", "desc"], default="desc",
                                             help="Order of sorting by number of orders (asc for least orders, desc for most orders). Defaults to 'desc'.")


    # --- Product Commands ---
    product_parser = subparsers.add_parser("products", help="Product related operations.")
    product_subparsers = product_parser.add_subparsers(dest="product_command", help="Product commands", required=True)

    # Command: products worst-performing --limit 5
    worst_performing_products_parser = product_subparsers.add_parser(
        "worst-performing", help="Provide a list of the worst-performing products by total sales quantity."
    )
    worst_performing_products_parser.add_argument("--limit", type=int, default=5,
                                                  help="Limit the number of worst-performing products to display. Defaults to 5.")

    # Command: products quarterly-sales --quarters 1 2 --order desc
    quarterly_sales_parser = product_subparsers.add_parser(
        "quarterly-sales", help="List products by quarterly sales from highest to lowest."
    )
    quarterly_sales_parser.add_argument("--quarters", type=int, nargs='+', choices=[1, 2, 3, 4],
                                        help="Specify one or more quarters (1, 2, 3, or 4) to include in the analysis (e.g., '--quarters 1 2').")
    quarterly_sales_parser.add_argument("--order", choices=["asc", "desc"], default="desc",
                                        help="Order of sorting by total quarterly sales (asc/desc). Defaults to 'desc'.")


    # --- Sales Commands ---
    sales_parser = subparsers.add_parser("sales", help="Sales related operations.")
    sales_subparsers = sales_parser.add_subparsers(dest="sales_command", help="Sales commands", required=True)

    # Command: sales most-orders-per-month
    most_orders_per_month_parser = sales_subparsers.add_parser(
        "most-orders-per-month", help="List customers who place the most orders in any single month."
    )

    # Command: sales return-rate-top-customers
    # NOTE: The "return rate" part requires data not present in your CSVs (e.g., a return flag or separate returns data).
    # For this exercise, I will interpret this as "List the top 3 customers and all products they purchased."
    return_rate_parser = sales_subparsers.add_parser(
        "return-rate-top-customers", help="Provides purchase details for the top 3 customers by total orders. (Note: 'Return Rate' concept is placeholder as no return data is available.)"
    )

    return parser