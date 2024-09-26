import mysql.connector
from mysql.connector import Error
import os
import pandas as pd

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

def insert_data_into_mysql(pandas_df, video_id):

    try:
        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            cursor = connection.cursor()

            # Define the insert query
            insert_query = """
            INSERT INTO sentiment_analysis (video_id, comment, sentiment)
            VALUES (%s, %s, %s)
            """

            # Insert each row from the Pandas DataFrame
            for row in pandas_df.itertuples(index=False):
                cursor.execute(insert_query, (video_id, row.CleanedComment, row.Sentiment))

            connection.commit()
            print("Data inserted successfully into sentiment_analysis table")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

