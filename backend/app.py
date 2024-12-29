from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from datetime import datetime
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)

CORS(app)

# app.config['MONGODB_SETTINGS'] = {
#     'host': os.environ['MONGODB_HOST'],
#     'username': os.environ['MONGODB_USERNAME'],
#     'password': os.environ['MONGODB_PASSWORD'],
#     'db': 'webapp'
# }

def get_db():
    client = MongoClient(host=os.environ['MONGODB_HOST'],
                         port=27017, 
                         username=os.environ['MONGODB_USERNAME'], 
                         password=os.environ['MONGODB_PASSWORD'],
                        authSource="admin")
    db = client["tutorials"]
    return db


#def get_db():
#     client = MongoClient(host='localhost',
#                          port=27017, 
#                          username='admin', 
#                          password='password',
#                         authSource="admin")
#     db = client["tutorials"]
#     return db

@app.route('/')
def ping_server():
    return "Welcome to the Tutorials API for Containers."

@app.route('/tutorials', methods=["GET"])
def get_all_tutorials():
    db = get_db()
    args = request.args
    print(args)
    _title = args.get("title")
    print(_title)

    if _title:
        _titleQuery = {"title": { "$regex": "^" + _title }}
    else:
        _titleQuery = ""

    _tutorials = db.tutorials_tab.find(_titleQuery)
    tutorials = [{"id": str(tutorial["_id"]), "title": tutorial["title"], "description": tutorial["description"], "published": tutorial["published"], "updatedAt": tutorial["updatedAt"], "createdAt": tutorial["createdAt"]} for tutorial in _tutorials]
    return jsonify(tutorials)

@app.route("/tutorials/<id>", methods=["GET"])
def get_tutorial(id):

    db = get_db()
    tutorial = db.tutorials_tab.find_one({'_id': ObjectId(id)})
    _tutorial = {"id": str(tutorial["_id"]), "title": tutorial["title"], "description": tutorial["description"], "published": tutorial["published"], "updatedAt": tutorial["updatedAt"], "createdAt": tutorial["createdAt"]}
    response = dumps(_tutorial)
    return response

@app.route("/tutorials", methods=["DELETE"])
def delete_all_tutorial():
    db = get_db()
    tutorial = db.tutorials_tab.delete_many({});
    _tutorial = {"message": "All records deleted successfully."}
    response = jsonify(_tutorial)
    response.status_code = 201
    return response

@app.route("/health", methods=["GET"])
def get_health():
    _tutorial = {"message": "Service is UP and Running fine."}
    response = jsonify(_tutorial)
    response.status_code = 200
    return response

@app.route("/tutorials/<id>", methods=["DELETE"])
def delete_tutorial(id):
    db = get_db()
    db.tutorials_tab.delete_one({'_id': ObjectId(id)})
    response = jsonify("User Deleted Successfully.")
    response.status_code = 200
    return response

@app.route("/tutorials/<id>", methods=['PUT'])
def update_tutorial(id):
    _id = id
    _json = request.json
    _title = _json['title']
    _description = _json['description']
    _published = _json['published']

    if _title and _description and _id and request.method == 'PUT':
        db = get_db()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        myquery = ({"_id": ObjectId(id)})
        newvalues = { "$set": { "title": _title, "description": _description, "updatedAt": dt_string, "published": _published} }
        db.tutorials_tab.update_one(myquery, newvalues)


        response = jsonify("User record updated successfully.")
        response.status_code = 200

        return response
    else:
        return not_found()

@app.route("/tutorials",methods=['POST'])
def add_user():
    _json = request.json
    _title = _json['title']
    _description = _json['description']
    _published = False
    # _published = _json['published']
    # _createdAt = _json['createdAt']
    # _updatedAt = _json['updatedAt']

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	

    if _title and _description and request.method == 'POST':
        db = get_db()
        id = db.tutorials_tab.insert_one({'title':_title, 'description': _description, 'published': _published, 'createdAt': dt_string, 'updatedAt': dt_string})

        response = jsonify("Tutorial added successfully.")
        response.status_code = 201
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Input values are not provided.'
    }

    response = jsonify(message)
    response.status_code = 404

    return response

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)