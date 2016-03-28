from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.elasticsearch import FlaskElasticsearch
from elasticsearch import Elasticsearch
from sqlalchemy.ext.declarative import declarative_base
import json
from flask.json import JSONEncoder
from flask import jsonify
from flask.ext.jsontools import jsonapi
from flask.ext.jsontools import JsonSerializableBase
from flask.ext.restless import APIManager
from flask import Response

app = Flask(__name__)

app.config.from_pyfile('configalchemy.cfg')
#es = Elasticsearch()
 #   res = es.search(index="test", doc_type="articles", body={"query": {"match": {"content": "fox"}}})
  #  print("%d documents found:" % res['hits']['total'])
   # for doc in res['hits']['hits']:
    #    print("%s) %s" % (doc['_id'], doc['_source']['content']))
   #es = FlaskElasticsearch(app)
   #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://abcd:abcd@localhost:3306/quotes'

db=SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hello world'
class Author(db.Model):
    Author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(40))
    quote = db.relationship('Quotes', backref='author', lazy='dynamic')

quotecategory =  db.Table('quotecategory',
                 db.Column('category_id', db.Integer, db.ForeignKey('category.category_id')),
                 db.Column('Quote_id', db.Integer, db.ForeignKey('quotes.Quote_id'))
                 )


    #quote_id= db.Column(db.Integer,db.ForeignKey('quotes.Quote_id'))
class Quotes(db.Model):
        Quote_id = db.Column(db.Integer, primary_key=True)
        quote = db.Column(db.String(100))
        author_name = db.Column(db.String(40))
        author_id = db.Column(db.Integer,db.ForeignKey('author.Author_id'))
        categories = db.relationship('Category', secondary = quotecategory, backref=db.backref('quotes', lazy = 'dynamic'))
        #category_quote = db.relationship('Category', backref='category', lazy='dynamic')
class Category(db.Model):
    category_id= db.Column(db.Integer, primary_key=True)
    category_name= db.Column(db.String(20))
Base = declarative_base(cls=(JsonSerializableBase,))

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
me = Object()






@app.route('/author', methods=['GET'])
def get_students():
    authors = Author.query.all()

    formatted_authors = []
    for a in authors:
        formatted_authors({

            'author_id' : a.Author_id,
            'author_name' : a.author_name,
            'quote' : a.quote,
        })
    #return formatted_authors
    return json.dumps({'author': formatted_authors}),200, {'Content-Type': 'application/json'}

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Category, methods=['GET', 'POST'])
manager.create_api(Author, methods=['GET', 'POST'])
manager.create_api(Quotes, methods=['GET', 'POST'])

if __name__=="__main__":
    app.run(debug=True)