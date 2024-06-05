import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('youtube_comments_with_sentiment.csv')

# Calculate average sentiment
average_sentiment = df['Sentiment'].mean()
print(f"Average Sentiment Polarity: {average_sentiment}")

# Count positive, negative, and neutral comments
positive_comments = df[df['Sentiment'] > 0].shape[0]
negative_comments = df[df['Sentiment'] < 0].shape[0]
neutral_comments = df[df['Sentiment'] == 0].shape[0]

print(f"Positive Comments: {positive_comments}")
print(f"Negative Comments: {negative_comments}")
print(f"Neutral Comments: {neutral_comments}")

# Plot sentiment distribution
labels = ['Positive', 'Neutral', 'Negative']
sizes = [positive_comments, neutral_comments, negative_comments]
colors = ['green', 'grey', 'red']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Sentiment Distribution of YouTube Comments')
plt.show()