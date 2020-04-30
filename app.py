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
    return render_template("facts.html",
                           facts=mongo.db.facts.find())


@app.route('/add_fact')
def add_fact():
    return render_template('addfact.html',
        supercars=mongo.db.supercars.find())   # noqa


@app.route('/insert_fact', methods=['POST'])
def insert_fact():
    facts = mongo.db.fact
    facts.insert_one(request.form.to_dict())
    return redirect(url_for('get_facts'))


@app.route('/edit_fact/<fact_id>')
def edit_fact(fact_id):
    the_fact = mongo.db.facts.find_one({"_id": ObjectId(fact_id)})
    all_supercars = mongo.db.supercars.find()
    return render_template('editfact.html', fact=the_fact,
                           supercars=all_supercars)


@app.route('/update_fact/<fact_id>', methods=["POST"])
def update_fact(fact_id):
    facts = mongo.db.fact
    facts.update({'_id': ObjectId(fact_id)},
    {
        'fact_name': request.form.get('fact_name'),
        'supercar_name': request.form.get('supercar_name'),
        'displacement': request.form.get('displacement'),
        'cylinders': request.form.get('cylinders'),
        'acceleration_time': request.form.get('acceleration_time'),
        'bhp': request.form.get('bhp'),
        'top_speed': request.form.get('top_speed'),
        'description': request.form.get('description')

    })
    return redirect(url_for('get_facts'))


@app.route('/delete_fact/<fact_id>')
def delete_fact(fact_id):
    mongo.db.facts.remove({'_id': ObjectId(fact_id)})
    return redirect(url_for('get_facts'))


@app.route('/get_supercars')
def get_supercars():
    return render_template('supercars.html',
                           supercars=mongo.db.supercars.find())


@app.route('/add_supercar')
def add_supercar():
    return render_template('addsupercar.html')


@app.route('/edit_supercar/<supercar_id>')
def edit_supercar(supercar_id):
    return render_template('editsupercar.html',
                           supercar=mongo.db.supercars.find_one({'_id': ObjectId(supercar_id)}))  # noqa


@app.route('/update_supercar/<supercar_id>', methods=['POST'])
def update_supercar(supercar_id):
    mongo.db.supercars.update(
        {'_id': ObjectId(supercar_id)},
        {'supercar_name': request.form.get('supercar_name')})
    return redirect(url_for('get_supercars'))


@app.route('/delete_supercar/<supercar_id>')
def delete_supercar(supercar_id):
    mongo.db.supercars.remove({'_id': ObjectId(supercar_id)})
    return redirect(url_for('get_supercars'))


@app.route('/insert_supercar', methods=['POST'])
def insert_supercar():
    supercar_doc = {'supercar_name': request.form.get('supercar_name')}
    mongo.db.supercars.insert_one(supercar_doc)
    return redirect(url_for('get_supercars'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)