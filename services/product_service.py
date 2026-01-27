# services/product_service.py
from utils.data_loader import DataStore
from utils.helpers import apply_pagination_and_sorting
from datetime import datetime

class ProductService:
    def __init__(self):
        self.data_store = DataStore()
        self.product_data = self.data_store.get_product_data()
        self.sales_data = self.data_store.get_sales_data()
        self.product_headers = self.data_store.get_product_headers()

    def get_worst_performing_products_by_quarter(self, limit=5):
        """
        Provides a list of the worst-performing products by total sales quantity.
        'Worst-performing' is defined by the lowest total quantity sold across all time.
        """
        product_sales_quantity = {} # {product_id: total_quantity_sold}

        for sale in self.sales_data:
            product_id = sale.get('product_id')
            quantity = sale.get('product_quantity', 0)
            if product_id is not None:
                product_sales_quantity[product_id] = product_sales_quantity.get(product_id, 0) + quantity

        product_sales_list = []
        for prod_id, total_quantity in product_sales_quantity.items():
            # Find product name for the product_id from product_dim
            product_name = None
            for p in self.product_data:
                if p.get('product_id') == prod_id:
                    product_name = p.get('product_name')
                    break # Found the name, no need to search further
            
            product_sales_list.append({
                'product_id': prod_id,
                'product_name': product_name if product_name else f"Unknown Product ({prod_id})",
                'total_quantity_sold': total_quantity
            })

        # Sort by total_quantity_sold in ascending order for "worst-performing"
        product_sales_list.sort(key=lambda x: x['total_quantity_sold'], reverse=False)

        return product_sales_list[:limit]

    def get_products_by_quarterly_sales(self, quarters=None, order='desc'):
        """
        Lists products by quarterly sales from the highest to the lowest.
        Can filter by specific quarters.
        """
        sales_by_product_quarter = {} # {(product_id, year, quarter): total_quantity}

        for sale in self.sales_data:
            product_id = sale.get('product_id')
            order_date = sale.get('order_date')
            quantity = sale.get('product_quantity', 0)

            if product_id is not None and order_date:
                # Calculate quarter (1-based)
                year = order_date.year
                quarter = (order_date.month - 1) // 3 + 1

                if quarters is None or quarter in quarters:
                    key = (product_id, year, quarter)
                    sales_by_product_quarter[key] = sales_by_product_quarter.get(key, 0) + quantity

        results = []
        for (prod_id, year, quarter), total_quantity in sales_by_product_quarter.items():
            product_name = None
            for p in self.product_data:
                if p.get('product_id') == prod_id:
                    product_name = p.get('product_name')
                    break
            results.append({
                'product_id': prod_id,
                'product_name': product_name if product_name else f"Unknown Product ({prod_id})",
                'year': year,
                'quarter': quarter,
                'total_quantity_sold': total_quantity
            })

        # Sort by total_quantity_sold
        results.sort(key=lambda x: x['total_quantity_sold'], reverse=(order == 'desc'))

        return results