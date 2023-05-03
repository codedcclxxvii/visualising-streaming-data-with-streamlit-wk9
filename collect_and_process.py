import pandas as pd
import tweepy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Twitter API authentication
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define function to collect real-time tweets related to telecoms fraud
def get_tweets():
    tweets = []
    for tweet in tweepy.Cursor(api.search, q='telecoms fraud', lang='en', tweet_mode='extended').items(100):
        tweets.append(tweet)
    return tweets

# Define function to process tweets and extract useful information
def process_tweets(tweets):
    data = pd.DataFrame(columns=['text', 'user', 'location', 'date'])
    for tweet in tweets:
        row = {
            'text': tweet.full_text,
            'user': tweet.user.screen_name,
            'location': tweet.user.location,
            'date': tweet.created_at
        }
        data = data.append(row, ignore_index=True)
    return data


# Get real-time tweets and process the data
tweets = get_tweets()
df = process_tweets(tweets)


# Extract the date and time from the 'created_at' column
df['datetime'] = pd.to_datetime(df['date'])
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

# Count the number of tweets by date
date_counts = df.groupby('date')['id'].count()

# Calculate the hourly distribution of tweets
hourly_counts = df.groupby(['date', 'time'])['id'].count()
hourly_counts = hourly_counts.groupby('time').mean()

# Calculate the top 10 users with the most tweets
user_counts = df.groupby('user')['id'].count()
top_users = user_counts.nlargest(10)

# Calculate the top 10 locations with the most tweets
location_counts = df.groupby('location')['id'].count()
top_locations = location_counts.nlargest(10)

# Create a bar chart showing the number of tweets by date
plt.figure(figsize=(10, 6))
plt.bar(date_counts.index, date_counts.values)
plt.title('Number of Telecoms Fraud Tweets by Date')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.show()

# Create a line chart showing the hourly distribution of tweets
plt.figure(figsize=(10, 6))
plt.plot(hourly_counts.index, hourly_counts.values)
plt.title('Hourly Distribution of Telecoms Fraud Tweets')
plt.xlabel('Time')
plt.ylabel('Average Number of Tweets per Hour')
plt.show()

# Create a horizontal bar chart showing the top 10 users with the most tweets
plt.figure(figsize=(10, 6))
plt.barh(top_users.index, top_users.values)
plt.title('Top 10 Users with the Most Telecoms Fraud Tweets')
plt.xlabel('Number of Tweets')
plt.show()

# Create a horizontal bar chart showing the top 10 locations with the most tweets
plt.figure(figsize=(10, 6))
plt.barh(top_locations.index, top_locations.values)
plt.title('Top 10 Locations with the Most Telecoms Fraud Tweets')
plt.xlabel('Number of Tweets')
plt.show()

