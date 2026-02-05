# 📊 Sales & Customer Data Analysis CLI

A Python-based Command Line Interface (CLI) tool for analyzing **customers, products, and sales data**.  
The project uses a modular structure with `argparse` to provide clean, scalable, and easy-to-use CLI commands.

---

## 🚀 Features

### 👥 Customer Analytics
- Total customers by location
- Customers from multiple locations
- Filter customers by age, address, and date
- Pagination, sorting, and column selection
- Top customers by number of orders

### 📦 Product Analytics
- Worst-performing products by sales quantity
- Quarterly product sales analysis
- Sort results in ascending or descending order

### 💰 Sales Analytics
- Customers with the most orders per month
- Purchase details of top customers  
  _(Return-rate is a placeholder due to missing return data)_

---

## 🧱 Project Structure

```bash
sales-cli/
│
├── utils/
│   └── cli_parser.py        # CLI argument and command definitions
│
├── services/
│   ├── customer_service.py # Customer-related logic
│   ├── product_service.py  # Product-related logic
│   └── sales_service.py    # Sales-related logic
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── sales.csv
│
├── main.py                 # Application entry point
├── requirements.txt
└── README.md
