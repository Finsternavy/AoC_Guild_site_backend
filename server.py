import json
from urllib import response
from flask import Flask, Response, abort, request, send_from_directory
# from mock_data import budgets
from config import database
from bson import ObjectId
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
# @cross_origin()
def serve():
    return 'this page intentionally left blank'


@app.post("/api/user-response")
def post_response():
    
    data = request.get_json()
    
    if data:
        database.responses.insert_one(data)
    
    else:
        return abort(400, 'Response empty')
    
    print(data)
    
    data['_id'] = str(data['_id'])
    
    return json.dumps(data)


@app.get('/api/user-response')
def get_responses():
    
    results = []
    
    cursor = database.responses.find({})
    
    for response in cursor:
        response['_id'] = str(response['_id'])
        results.append(response)
    
    return json.dumps(results)


@app.post('/api/guild-data')
def update_guild_data():
    
    data = request.get_json()
    print(data)
    old_data = database.guild_data.find_one({'title': 'guild_data'})
    
    if not old_data:
        database.guild_data.insert_one(data)
        
    else:
        database.guild_data.find_one_and_delete({'title': 'guild_data'})
        database.guild_data.insert_one(data)
        
    data['_id'] = str(data['_id'])
    
    
    return json.dumps(data)


@app.get('/api/guild-data')
def get_guild_data():
    
    result = {}
    
    cursor = database.guild_data.find({'title': 'guild_data'})
    
    for data in cursor:
        data['_id'] = str(data['_id'])
        result = data
    
    return json.dumps(result)

app.run(debug=True)