""" SQLAlchemy models and utility functions for Twitoff """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from os import getenv

# create instance of sqlalchemy
#engine = SQLAlchemy.create_engine(getenv("DATABASE_URI"))
#Session = sessionmaker(bind=engine)
DB = SQLAlchemy()

# flask tables == classes in python. make it subclass of DB.Model
class User(DB.Model): # user table
    """ Twitter Users corresponding to tweets """
    id = DB.Column(DB.BigInteger, primary_key=True)
    
    name = DB.Column(DB.String, nullable=False)

    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """ Tweets corresponding to users """
    id = DB.Column(DB.BigInteger, primary_key=True) # tweet id column

    text = DB.Column(DB.Unicode(300)) # text of the tweet column. unicode allows for emojis, links ,etc

    vect = DB.Column(DB.PickleType, nullable=False)

    user_id = DB.Column(DB.ForeignKey('user.id'), nullable=False) # user_id col
    
    user = DB.relationship('User', backref=DB.backref("tweets", lazy=True))
    # creating relationship btwn tweets and the user. creates attribute of Users called 'tweets' we can go back and reference

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
