import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy

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

# Define function to visualize data in a meaningful way
def visualize_data(data):
    st.write("Number of fraud mentions by location")
    location_counts = data['location'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=location_counts.values, y=location_counts.index, ax=ax)
    ax.set_xlabel('Number of mentions')
    ax.set_ylabel('Location')
    st.pyplot(fig)

# Set up Streamlit app
st.title("Telecoms Fraud Dashboard")

# Get real-time tweets and process the data
tweets = get_tweets()
data = process_tweets(tweets)

# Visualize the data
visualize_data(data)
