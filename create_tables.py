import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Load MySQL credentials from environment variables
mysql_host = os.getenv('MYSQL_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

# MySQL connection configuration
config = {
    'host': mysql_host,
    'user': mysql_user,
    'password': mysql_password,
    'database': mysql_database
}

def create_sentiment_lookup_table(cursor):
    """Function to create sentiment_lookup table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_lookup (
        id INT PRIMARY KEY,
        description VARCHAR(20)
    )
    """
    cursor.execute(create_table_query)
    print("Created 'sentiment_lookup' table.")

def insert_sentiment_lookup_data(cursor):
    """Function to insert data into sentiment_lookup table."""
    insert_data_query = """
    INSERT IGNORE INTO sentiment_lookup (id, description)
    VALUES (0, 'Negative'), (1, 'Neutral'), (2, 'Positive')
    """
    cursor.execute(insert_data_query)
    print("Inserted sentiment data into 'sentiment_lookup' table.")

def create_sentiment_analysis_table(cursor):
    """Function to create sentiment_analysis table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_analysis (
        id INT AUTO_INCREMENT PRIMARY KEY,
        video_id VARCHAR(255),
        comment TEXT,
        sentiment INT,
        FOREIGN KEY (sentiment) REFERENCES sentiment_lookup(id)
    )
    """
    cursor.execute(create_table_query)
    print("Created 'sentiment_analysis' table.")

def setup_database():
    """Main function to set up the database with tables."""
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Create tables and insert data
        create_sentiment_lookup_table(cursor)
        insert_sentiment_lookup_data(cursor)
        create_sentiment_analysis_table(cursor)

        connection.commit()
        print("Tables created and data inserted successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


