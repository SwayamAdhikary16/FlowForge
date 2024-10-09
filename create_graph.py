import matplotlib.pyplot as plt

def create(pandas_df):
    sentiment_counts = pandas_df.groupby('Sentiment').size().reset_index(name='count')
    sentiment_counts.head()
    # Collect the aggregated data for visualization
    plt.figure(figsize=(8, 5))
    plt.bar(sentiment_counts['Sentiment'], sentiment_counts['count'], color=['gray','green','red'])
    plt.xticks([0, 1, 2], ['Negative', 'Neutral', 'Positive'])
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    plt.show()
