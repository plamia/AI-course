# 1. Notebook install command: %pip install --quiet duckdb pandas numpy

# 2. Import the necessary libraries
import duckdb
import pandas as pd
import os
import random
import numpy as np
from datetime import datetime

# 3. Create an in-memory DuckDB connection
conn = duckdb.connect(':memory:')

# 4 & 5. Create a test table and insert 3 rows of sample data
conn.execute("""
    CREATE TABLE hello_world (
        id INTEGER, 
        message VARCHAR, 
        created_at TIMESTAMP
    );
    
    INSERT INTO hello_world VALUES 
        (1, 'Hello from Bronze layer!', current_timestamp),
        (2, 'Hello from Silver layer!', current_timestamp),
        (3, 'Hello from Gold layer!', current_timestamp);
""")

# 6. Run a SELECT query and fetch the results as a Pandas DataFrame
result_df = conn.execute("SELECT * FROM hello_world").df()

# Print the results
print("--- Query Results ---")
print(result_df)
print("-" * 20)

# 7. Print success message
print("\nEnvironment ready ✓")