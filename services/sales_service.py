# services/sales_service.py
from utils.data_loader import DataStore
from utils.helpers import apply_pagination_and_sorting
from datetime import datetime

class SalesService:
    def __init__(self):
        self.data_store = DataStore()
        self.sales_data = self.data_store.get_sales_data()
        self.customer_data = self.data_store.get_customer_data()
        self.product_data = self.data_store.get_product_data()

    def get_customers_most_orders_per_month(self):
        """
        Lists customers who place the most orders per month.
        Identifies the single month where each customer had their highest order count.
        """
        # Dictionary to store orders per customer per month: {(cust_id, year, month): order_count}
        customer_monthly_orders = {}

        for sale in self.sales_data:
            cust_id = sale.get('cust_id')
            order_date = sale.get('order_date')
            if cust_id is not None and order_date:
                year_month = (order_date.year, order_date.month)
                key = (cust_id, year_month)
                customer_monthly_orders[key] = customer_monthly_orders.get(key, 0) + 1

        # Find the maximum orders per month for each unique customer
        customer_max_monthly_orders = {} # {cust_id: {'max_orders': count, 'month_str': 'YYYY-MM'}}
        for (cust_id, (year, month)), order_count in customer_monthly_orders.items():
            current_max = customer_max_monthly_orders.get(cust_id, {'max_orders': 0})
            if order_count > current_max['max_orders']:
                customer_max_monthly_orders[cust_id] = {
                    'max_orders': order_count,
                    'month_str': f"{year}-{month:02d}" # Format month as MM
                }

        results = []
        for cust_id, info in customer_max_monthly_orders.items():
            customer_info = next((c for c in self.customer_data if c.get('cust_id') == cust_id), None)
            if customer_info:
                results.append({
                    'cust_id': cust_id,
                    'cust_address': customer_info.get('cust_address'),
                    'cust_age': customer_info.get('cust_age'),
                    'max_orders_in_month': info['max_orders'],
                    'month_of_max_orders': info['month_str']
                })

        # Sort by max_orders_in_month in descending order to show "most orders" first
        results.sort(key=lambda x: x['max_orders_in_month'], reverse=True)
        return results

    def get_return_rate_for_top_customers(self):
        """
        Provides purchase details for the top 3 customers by total orders.
        NOTE: The concept of "return rate" is not directly supported by the provided CSV data
        as there's no 'return' indicator. This function will list the top 3 customers
        by their total orders and then detail all products they purchased.
        """
        # Step 1: Identify top 3 customers by total orders (reusing logic from CustomerService concept)
        customer_order_counts = {}
        for sale in self.sales_data:
            cust_id = sale.get('cust_id')
            if cust_id is not None:
                customer_order_counts[cust_id] = customer_order_counts.get(cust_id, 0) + 1

        customer_counts_list = [{'cust_id': k, 'order_count': v} for k, v in customer_order_counts.items()]
        customer_counts_list.sort(key=lambda x: x['order_count'], reverse=True) # Sort descending
        
        top_3_customer_ids = [item['cust_id'] for item in customer_counts_list[:3]]

        results = []
        if not top_3_customer_ids:
            return []

        for cust_id in top_3_customer_ids:
            customer_info = next((c for c in self.customer_data if c.get('cust_id') == cust_id), None)
            if not customer_info:
                continue # Skip if customer details not found

            customer_purchases_summary = {
                'cust_id': cust_id,
                'cust_address': customer_info.get('cust_address'),
                'cust_age': customer_info.get('cust_age'),
                'purchased_products': []
            }

            # To avoid listing the same product multiple times if purchased repeatedly by the same customer
            purchased_product_ids_for_customer = set()

            for sale in self.sales_data:
                if sale.get('cust_id') == cust_id:
                    product_id = sale.get('product_id')
                    if product_id is not None and product_id not in purchased_product_ids_for_customer:
                        # Find product details for this product_id
                        product_details = next((p for p in self.product_data if p.get('product_id') == product_id), None)
                        if product_details:
                            customer_purchases_summary['purchased_products'].append({
                                'product_id': product_id,
                                'product_name': product_details.get('product_name'),
                                'product_price': product_details.get('product_price')
                                # For precise price at time of purchase, you'd need to match
                                # sales.order_date with product_dim effective dates, which is more complex.
                                # Here, it uses the product_dim entry found first.
                            })
                            purchased_product_ids_for_customer.add(product_id)
            results.append(customer_purchases_summary)

        return results