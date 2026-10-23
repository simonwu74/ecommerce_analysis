import duckdb

# Match each table name with its CSV file.
csv_files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# Connect to the database.
connection = duckdb.connect("data/ecommerce.duckdb")

# Create the schema for raw data.
connection.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Load each CSV into a table.
for table_name, file_name in csv_files.items():
    connection.execute(f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT *
        FROM read_csv(
            'data/raw/{file_name}',
            header = true,
            all_varchar = true
        )
    """)

    result = connection.execute(
        f"SELECT COUNT(*) FROM raw.{table_name}"
    ).fetchone()

    print(table_name, "loaded:", result[0], "rows")

# Close the database connection.
connection.close()