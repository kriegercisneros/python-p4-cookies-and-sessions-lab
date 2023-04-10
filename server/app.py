#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

#creating a migration object that will be used to make db schema changes
migrate = Migrate(app, db)

#initializing the db connection with the Flask app instance
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

#creating a flask route decorator for the /articles endpoint
@app.route('/articles')
#defining a funciton that returns a list of articles as JSON when this endpoint is accessed
def index_articles():
    #querying the db for all Article records, converting each to a dict , and returning a list of dicts
    articles=[article.to_dict() for article in Article.query.all()]
    #creating a flask response object converting the list of dictionaries toJSON and setting the heep status code to 200 or ok

    return make_response(jsonify(articles), 200)
#creating a flask route decorator for the below endpoint where id is a dynamic value 
@app.route('/articles/<int:id>')
def show_article(id):
    #if this is the first request, set session['page_views'] to an initial value of 0 (use a ternary operator)
        #setting the page views key in the user's session to either the current vlaue (if it exists ) or to 0 
    session['page_views'] = session.get('page_views') or 0
    #for every request, increment to value of session['page_views'] by 1
    session['page_views'] += 1
    #if the user has viewed 3 or fewer pages, render a json respoonse with the article data
    #if page views is less than or equal to 3, we can allow the user to view the 
    if session['page_views']<=3:
        return Article.query.filter(Article.id==id).first().to_dict(), 200
    
    return {'message': 'Max pageview limit reached'}, 301
    #if the user has viewed more than 3 pages, render a JSON resp including the error message:
        #{'message':'Max pageview limit reached'} and a status of 401 unauthorized
    #an api endpoint at /clean is available to clear your session
    pass

if __name__ == '__main__':
    app.run(port=5555)
