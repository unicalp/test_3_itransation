import re
import json
import mysql.connector

def ingest_to_db(books: list):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          
        database="task3_5"
    )
    cursor = conn.cursor()

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id VARCHAR(30) PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            genre VARCHAR(255),
            publisher VARCHAR(255),
            year INT,
            price VARCHAR(20)
        )
    """)

    #list of dicts executemany to tuple for easy ingest
    #fetch to one by one book patterns
    rows_to_insert = [
        (str(b["id"]), b["title"], b["author"], b["genre"], b["publisher"], int(b["year"]), b["price"])
        for b in books
    ]

    #commit data
    sql_insert = """
        INSERT IGNORE INTO books (id, title, author, genre, publisher, year, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql_insert, rows_to_insert)
    conn.commit()

    print(f"Count of ingested row data: {cursor.rowcount}")
    cursor.close()
    conn.close()

def convert_ruby_to_json(input_file_path: str):
    #data reading in straight text format and keep the currencies
    with open(input_file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
        
    #also pattern convertend from ruby to json format
    sub_data = re.sub(r':(\w+)\s*=>', r'"\1": ', raw_text)
    
    #clean text reading with json.loads and retrieve a clean code
    clean_data = json.loads(sub_data)
    return clean_data

def build_summary_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="task3_5"
    )
    cursor = conn.cursor()

    #Synch summary table
    cursor.execute("DROP TABLE IF EXISTS summary_table")

    #Build summary table
    sql_transform = """
        CREATE TABLE summary_table AS
        SELECT 
            year AS publication_year,
            COUNT(*) AS book_count,
            ROUND(AVG(
                CASE 
                    WHEN price LIKE '€%' THEN CAST(SUBSTRING(price, 2) AS DECIMAL(10, 4)) * 1.2
                    ELSE CAST(SUBSTRING(price, 2) AS DECIMAL(10, 4))
                END
            ), 2) AS average_price
        FROM books
        GROUP BY year
        ORDER BY publication_year;
    """
    cursor.execute(sql_transform)
    conn.commit()

    # Get response about summary table
    print("Summary table created successfully in RDBMS.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    books_data = convert_ruby_to_json("task1_d.json")
    print(f"Total parsed books:{len(books_data)}")
    ingest_to_db(books_data)
    build_summary_table()