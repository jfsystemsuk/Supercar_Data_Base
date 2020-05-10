import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Supercar_Data_Base'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@cluster0-y0jyu.mongodb.net/Supercar_Data_Base?retryWrites=true&w=majority'  # noqa

mongo = PyMongo(app)

# get facts and render the template
@app.route('/')
@app.route('/get_facts')
def get_facts():
    return render_template("facts.html",
                           facts=mongo.db.facts.find())

# add fact and render the template
@app.route('/add_fact')
def add_fact():
    return render_template('addfact.html',
                           supercars=mongo.db.supercars.find())   # noqa

# insert fact and render the template
@app.route('/insert_fact', methods=['POST'])
def insert_fact():
    facts = mongo.db.facts
    facts.insert_one(request.form.to_dict())
    return redirect(url_for('get_facts'))

# edit fact and render the template
@app.route('/edit_fact/<fact_id>')
def edit_fact(fact_id):
    the_fact = mongo.db.facts.find_one({"_id": ObjectId(fact_id)})
    all_supercars = mongo.db.supercars.find()
    return render_template('editfact.html', fact=the_fact,
                           supercars=all_supercars)

# update fact and render the template
@app.route('/update_fact/<fact_id>', methods=["POST"])
def update_fact(fact_id):
    facts = mongo.db.facts
    facts.update({'_id': ObjectId(fact_id)},
    {
        'supercar_name': request.form.get('supercar_name'),
        'displacement': request.form.get('displacement'),
        'cylinders': request.form.get('cylinders'),
        'aspiration': request.form.get('aspiration'),
        'engine_position': request.form.get('engine_position'),
        'acceleration_time': request.form.get('acceleration_time'),
        'bhp': request.form.get('bhp'),
        'engine_torque': request.form.get('engine_torque'),
        'valves': request.form.get('valves'),
        'top_speed': request.form.get('top_speed'),
        'gearbox': request.form.get('gearbox'),
        'driven_wheels': request.form.get('driven_wheels'),
        'body_style': request.form.get('body_style'),
        'fuel_type': request.form.get('fuel_type'),
        'doors': request.form.get('doors'),
        'weight': request.form.get('weights'),
        'mpg': request.form.get('mpg'),
        'cost_new': request.form.get('cost_new'),
        'cost_used': request.form.get('cost_used')

    })
    return redirect(url_for('get_facts'))

# delete fact and render the template
@app.route('/delete_fact/<fact_id>')
def delete_fact(fact_id):
    mongo.db.facts.remove({'_id': ObjectId(fact_id)})
    return redirect(url_for('get_facts'))

# get supercars and render the template
@app.route('/get_supercars')
def get_supercars():
    return render_template('supercars.html',
                           supercars=mongo.db.supercars.find())

# add supercars and render the template
@app.route('/add_supercar')
def add_supercar():
    return render_template('addsupercar.html')

# edit supercars and render the template
@app.route('/edit_supercar/<supercar_id>')
def edit_supercar(supercar_id):
    return render_template('editsupercar.html',
                           supercar=mongo.db.supercars.find_one({'_id': ObjectId(supercar_id)}))  # noqa

# update supercars and render the template
@app.route('/update_supercar/<supercar_id>', methods=['POST'])
def update_supercar(supercar_id):
    mongo.db.supercars.update(
        {'_id': ObjectId(supercar_id)},
        {'supercar_name': request.form.get('supercar_name')})
    return redirect(url_for('get_supercars'))

# delete supercars and render the template
@app.route('/delete_supercar/<supercar_id>')
def delete_supercar(supercar_id):
    mongo.db.supercars.remove({'_id': ObjectId(supercar_id)})
    return redirect(url_for('get_supercars'))

# insert supercars and render the template
@app.route('/insert_supercar', methods=['POST'])
def insert_supercar():
    supercar_doc = {'supercar_name': request.form.get('supercar_name')}
    mongo.db.supercars.insert_one(supercar_doc)
    return redirect(url_for('get_supercars'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)