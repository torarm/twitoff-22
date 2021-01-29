""" Retrieve Tweets & Embeddings and put them in our database """

from os import getenv
import tweepy # allows us to interact w. twitter
import spacy # vectorizes the tweets
from twitoff.models import DB, Tweet, User
from sqlalchemy.sql import exists, text

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        # create user based on the username passed into the function
        twitter_user = TWITTER.get_user(username)
        # If they exist then update that user, if we get something back
        # then instantiate a new user
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)

        # Add the user to our database
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="Extended",
            since_id=db_user.newest_tweet_id
        )  # A list of tweets from "username"

        # empty tweets list == false, full tweets list == true
        if tweets:
            # updates newest_tweet_id
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # for each tweet we want to create an embedding
            vectorized_tweet = vectorize_tweet(tweet.text)
            # create tweet that will be added to our DB
            db_tweet = Tweet(id=tweet.id, text=tweet.text,
                             vect=vectorized_tweet)
            # append each tweet from "username" to username.tweets
            db_user.tweets.append(db_tweet)
            # Add db_tweet to Tweet DB
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        # commit everything to the database
        DB.session.commit()


def update_all_users():
    """Update all Tweets for all Users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)
