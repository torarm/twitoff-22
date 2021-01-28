""" Main App/ Routing file for Twitoff """

from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user

def create_app():
    app = Flask(__name__) # name is telling it to use the directory we r in basically

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route("/") # this is an endpoint. function below is ran whenever we go to path
    def root():
        return render_template('base.html', title='Home',
                                users=User.query.all()) # second argument matches var in base.html
    
    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} was successfully added!".format(name)
            
            tweets = User.query.filter(User.name == name).one().tweets

            if name == "elonmusk":
                message = "Sorry, elonmusk is banned for being annoying and ugly."
                tweets = []
        
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        
        return render_template("user.html", title=name,
                                tweets=tweets, message=message)

    @app.route("/compare", methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values["user1"], request.values["user2"]])
        
        if user0 == user1:
            message = "Cannot compare users to themselves"
        else:
            # predicts the user
            prediction = predict_user(user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be tweeted by {} than {}".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )
        return render_template("prediction.html",
                                title="Prediction", message=message)

    @app.route("/update")
    def update():
        update_all_users()
        return render_template('base.html', title='Home',
                                users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')
    
    return app
