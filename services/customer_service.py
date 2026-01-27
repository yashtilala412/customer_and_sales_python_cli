# services/customer_service.py
from utils.data_loader import DataStore
from utils.helpers import apply_pagination_and_sorting
from datetime import datetime

class CustomerService:
    def __init__(self):
        self.data_store = DataStore()
        self.customer_data = self.data_store.get_customer_data()
        self.sales_data = self.data_store.get_sales_data()
        self.customer_headers = self.data_store.get_customer_headers() # Get original headers for print_table

    def get_total_customers_by_location(self, location):
        """
        Provides the total number of customers by location.
        Location match is case-insensitive and partial.
        """
        count = 0
        location_lower = location.lower()
        for customer in self.customer_data:
            if customer.get('cust_address') and location_lower in customer['cust_address'].lower():
                count += 1
        return count

    def find_customers_from_multiple_locations(self, locations, **kwargs):
        """
        Finds customers who reside in any of the specified locations.
        """
        found_cust_ids = set() # Use a set to store unique customer IDs to avoid duplicates
        results = []
        for loc in locations:
            loc_lower = loc.lower()
            for customer in self.customer_data:
                cust_id = customer.get('cust_id')
                cust_address = customer.get('cust_address')
                if cust_id is not None and cust_address and loc_lower in cust_address.lower() and cust_id not in found_cust_ids:
                    results.append(customer)
                    found_cust_ids.add(cust_id)
        return apply_pagination_and_sorting(results, **kwargs)

    def list_customers(self, age=None, address=None, date=None, **kwargs):
        """
        Lists customers based on specified criteria (age, address, date).
        Applies pagination and sorting.
        """
        filtered_customers = []
        for customer in self.customer_data:
            match = True

            if age is not None and customer.get('cust_age') != age:
                match = False
            
            if address:
                cust_address_lower = customer.get('cust_address', '').lower()
                if address.lower() not in cust_address_lower:
                    match = False
            
            if date:
                try:
                    query_date = datetime.strptime(date, '%Y-%m-%d')
                    start_date = customer.get('effective_start_date')
                    end_date = customer.get('effective_end_date')

                    # Check if query_date falls within the effective date range
                    if not (start_date and end_date and start_date <= query_date <= end_date):
                        match = False
                except ValueError:
                    print(f"Warning: Invalid date format for --date: '{date}'. Expected YYYY-MM-DD. Skipping date filter for this customer.")
                    match = False

            if match:
                filtered_customers.append(customer)

        return apply_pagination_and_sorting(filtered_customers, **kwargs)

    def get_top_customers_by_orders(self, limit=10, order='desc'):
        """
        Lists the top N customers with the most orders.
        """
        customer_order_counts = {} # {cust_id: count}
        for sale in self.sales_data:
            cust_id = sale.get('cust_id')
            if cust_id is not None:
                customer_order_counts[cust_id] = customer_order_counts.get(cust_id, 0) + 1

        # Convert to a list of dictionaries for sorting
        customer_counts_list = [{'cust_id': k, 'order_count': v} for k, v in customer_order_counts.items()]

        # Sort based on order_count
        customer_counts_list.sort(key=lambda x: x['order_count'], reverse=(order == 'desc'))

        # Merge with customer details from customer_dim
        top_customers_details = []
        for item in customer_counts_list[:limit]:
            cust_id = item['cust_id']
            order_count = item['order_count']
            # Find the corresponding customer details
            customer_info = next((c for c in self.customer_data if c.get('cust_id') == cust_id), None)
            if customer_info:
                top_customers_details.append({
                    'cust_id': cust_id,
                    'cust_address': customer_info.get('cust_address'),
                    'cust_age': customer_info.get('cust_age'),
                    'order_count': order_count
                })
        return top_customers_details