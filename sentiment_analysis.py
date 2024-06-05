from textblob import TextBlob
import pandas as pd

# Load comments from CSV file
df = pd.read_csv('youtube_comments.csv')

# Function to get sentiment
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Apply sentiment analysis
df['Sentiment'] = df['Comment'].apply(get_sentiment)

# Display results
print(df.head())

# Save the results
df.to_csv('youtube_comments_with_sentiment.csv', index=False)
print("Sentiment analysis results saved to youtube_comments_with_sentiment.csv")
