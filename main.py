# main.py
import sys
from utils.cli_parser import create_parser
from services.customer_service import CustomerService
from services.product_service import ProductService
from services.sales_service import SalesService
from utils.helpers import print_table

def main():
    parser = create_parser()
    args = parser.parse_args()

    # Instantiate services
    customer_service = CustomerService()
    product_service = ProductService()
    sales_service = SalesService()

    try:
        if args.command == "customers":
            if args.customer_command == "total-by-location":
                count = customer_service.get_total_customers_by_location(args.location)
                print(f"Total customers in '{args.location}': {count}")
            elif args.customer_command == "from-multiple-locations":
                customers = customer_service.find_customers_from_multiple_locations(
                    args.locations,
                    skip=args.skip, limit=args.limit, order=args.order,
                    order_by=args.order_by, selects=args.selects
                )
                print("Customers from multiple locations:")
                # Pass specific headers if you want a fixed display order
                print_table(customers, headers=['cust_id', 'cust_address', 'cust_age', 'effective_start_date', 'effective_end_date', 'current_ind'])
            elif args.customer_command == "list":
                customers = customer_service.list_customers(
                    age=args.age, address=args.address, date=args.date,
                    skip=args.skip, limit=args.limit, order=args.order,
                    order_by=args.order_by, selects=args.selects
                )
                print("Filtered customers:")
                # Use the original headers to ensure correct column order if not 'selects'
                print_table(customers, headers=customer_service.customer_headers)
            elif args.customer_command == "top-orders":
                top_customers = customer_service.get_top_customers_by_orders(
                    limit=10, # As per problem statement "top 10"
                    order=args.order
                )
                print("Top 10 customers by most orders:")
                print_table(top_customers)

        elif args.command == "products":
            if args.product_command == "worst-performing":
                worst_products = product_service.get_worst_performing_products_by_quarter(limit=args.limit)
                print(f"Worst performing products (lowest total quantity sold, top {args.limit}):")
                print_table(worst_products)
            elif args.product_command == "quarterly-sales":
                sales_data = product_service.get_products_by_quarterly_sales(
                    quarters=args.quarters,
                    order=args.order
                )
                print("Products by quarterly sales:")
                print_table(sales_data)

        elif args.command == "sales":
            if args.sales_command == "most-orders-per-month":
                customers_most_orders = sales_service.get_customers_most_orders_per_month()
                print("Customers with the most orders in any single month:")
                print_table(customers_most_orders)
            elif args.sales_command == "return-rate-top-customers":
                # As noted, this lists purchased products for top customers due to lack of return data
                top_customer_details = sales_service.get_return_rate_for_top_customers()
                if top_customer_details:
                    print("Top 3 Customers and Their Purchased Product Details:")
                    for customer in top_customer_details:
                        print(f"\n--- Customer ID: {customer['cust_id']} ({customer['cust_age']} yrs, {customer['cust_address']}) ---")
                        if customer['purchased_products']:
                            print("  Purchased Products:")
                            # Print sub-table for products
                            product_headers_for_display = ['product_id', 'product_name', 'product_price']
                            print_table(customer['purchased_products'], headers=product_headers_for_display)
                        else:
                            print("  No purchased products found for this customer.")
                else:
                    print("Could not retrieve top customer details or no sales data available.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    main()