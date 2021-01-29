""" Prediction of Users based on Tweet Embeddings """

import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.models import User
from twitoff.twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_txt):
    """
    Determine who is more likely to say a hypothetical tweet.
    Example: predict_user('elonmusk', 'jackblack', 'Gamestonks!!')
    Returns: 0 (user0_name: 'elonmusk') or 1 (user1_name: 'jackblack')
    """
    # grab both users and vectorized tweets
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    user0_vex = np.array([tweet.vect for tweet in user0.tweets])
    user1_vex = np.array([tweet.vect for tweet in user1.tweets])

    # combine vex & create y col
    vects = np.vstack([user0_vex, user1_vex])
    labels = np.concatenate([np.zeros(len(user0.tweets)),
                            np.ones(len(user1.tweets))])
    
    # create & fit model
    logreg = LogisticRegression().fit(vects, labels)

    # vectorize tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_txt)

    # reshape tweet & predict
    return logreg.predict(np.array(hypo_tweet_vect).reshape(1, -1))
