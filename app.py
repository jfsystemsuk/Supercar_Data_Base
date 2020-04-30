import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Supercar_Data_Base'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@cluster0-y0jyu.mongodb.net/Supercar_Data_Base?retryWrites=true&w=majority'  # noqa

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_facts')
def get_facts():
    return render_template("facts.html", facts=mongo.db.facts.find())


@app.route('/add_fact')
def add_fact():
    return render_template('addfact.html', supercars=mongo.db.supercars.find())   # noqa
        

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)