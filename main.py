import googleapiclient.discovery
import os
import pandas as pd
from textblob import TextBlob
from create_graph import create
import create_tables
from insert_values import insert_data_into_mysql
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
# Load API key from environment variable
youtube_api_key = os.getenv("YT_API")

# Step 1: Fetch comments from YouTube
def get_latest_comments(video_id, api_key, max_results=1000):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None

    while len(comments) < max_results:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=min(max_results - len(comments), 100),
            pageToken=next_page_token,
            order='time'  # Order by latest comments
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

# Step 2: Clean the comments
def clean_comments(comments):
    comments_df = pd.DataFrame(comments, columns=["Comment"])
    
    # Convert text to lowercase and remove special characters
    comments_df["CleanedComment"] = comments_df["Comment"].str.lower()
    comments_df["CleanedComment"] = comments_df["CleanedComment"].str.replace("[^a-zA-Z0-9\s]", "", regex=True)

    return comments_df

# Step 3: Sentiment analysis using TextBlob
def textblob_sentiment_analysis(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity < -0.05:
        return 0  # Negative sentiment
    elif polarity > 0.05:
        return 2  # Positive sentiment
    else:
        return 1  # Neutral sentiment

# # Main function to check the process
# def main(video_id):
#     # Fetch and preprocess comments
#     comments = get_latest_comments(video_id, youtube_api_key)
#     logging.info(f"Fetched {len(comments)} comments for video ID: {video_id}")
#     preprocessed_df = clean_comments(comments)
#     logging.info("Comments cleaned successfully")   
#     # Perform sentiment analysis
#     preprocessed_df["Sentiment"] = preprocessed_df["CleanedComment"].apply(textblob_sentiment_analysis)
#     logging.info("Sentiment analysis completed successfully")
#     #Current graph
#     #create(preprocessed_df)
#     logging.info("Graph created successfully")
#     #Create table if doesn't exist
#     create_tables.setup_database()
#     # Insert the processed data into MySQL
#     insert_data_into_mysql(preprocessed_df, video_id)
#     logging.info("Data inserted successfully into MySQL")

