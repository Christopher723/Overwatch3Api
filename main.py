from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, session

import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
existing_db_path = 'OverwatchDB.db'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'OverwatchDB.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Product Class/Model
class Abilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=False)
    name = db.Column(db.String(255))
    imageURL = db.Column(db.String(255))
    description = db.Column(db.String(255))

# Update Results Class/Model
class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255))
    role = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    abilities = db.relationship('Abilities', backref='hero', lazy=True)
    story = db.Column(db.String(255))
    birthday = db.Column(db.String(255))
    base = db.Column(db.String(255))
    imageURL = db.Column(db.String(255))


class resultsSchema(ma.Schema):
    class Meta:
        fields = ('name','role', 'url')

class abilitiesSchema(ma.Schema):
    class Meta:
        fields = ('name', 'imageURL', 'description')

class singleSchema(ma.Schema):
    class Meta:
        fields = ('name', 'type', 'bio', 'abilities', 'story','birthday','base','imageURL')

    abilities = ma.Nested(abilitiesSchema, many=True)
# Init schema
result_schema = resultsSchema()
results_schema = resultsSchema(many=True)

# Get all products
@app.route('/heros', methods=['GET'])
def get_products():
    all_products = Results.query.all()
    result = {
        "Heros": results_schema.dump(all_products),
    }
    return jsonify(result)

# Get a single product with associated abilities
@app.route('/heros/<name>', methods=['GET'])
def get_product(name):
    # if name_lower:
    #     name = name_lower
    # product = Results.query.get(id)
    product = db.session.query(Results).filter_by(name=name).first()
    
    return singleSchema().jsonify(product)


## this allows us to add .png to the end of our images which looks more professional
@app.route('/image/<name>', methods=['GET'])
def get_ability_image(name):
    image_filename = f"{name}.png"
    image_path = os.path.abspath(os.path.join(basedir, 'AbilityIcons', image_filename))
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png') 
    else:
       return "Image not found", 404

@app.route('/heros/<name>/Icon', methods=['GET'])
def get_heroIcon_image(name):
    image_filename = f"{name}.png"
    image_path = os.path.abspath(os.path.join(basedir, 'HeroIcons', image_filename))
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png') 
    else:
       return "Image not found", 404


@app.route('/image/<role>/Icon', methods=['GET'])
def get_RoleIcon_image(role):
    print(role)
    image_filename = f"{role}.png"
    image_path = os.path.abspath(os.path.join(basedir, 'RoleIcon', image_filename))
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png') 
    else:
       return "Image not found", 404


# Run server
if __name__ == '__main__':
    app.run(debug=True)
