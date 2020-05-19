from flask import Flask
from flask import request
from flask import jsonify
from pymongo import MongoClient
from pprint import pprint
from time import time

app = Flask(__name__)


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
connection = MongoClient('mongodb://localhost:27017/creativeengine')
def dbInit():
    try:
        dbnames = connection.list_database_names()
        if 'engine' not in dbnames:
            db_api = connection.engine.releaseinfo
            db_api.insert( {
                "Author1":"Ayushi Rathod",
                "Author2":"Prateek Rokadiya",
                "buildtime": str(time()),
                "methods": "get, post, put, delete",
                "version": "v1"
            })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")

@app.route('/genlink', methods = ['POST'])
def genlink():
    if request.method == 'POST':
        data = request.get_json()
        output = ""
        if data is not None:
            output = data['name']
            # Create a link
            # Add to db
            # send back page link
        return jsonify({"res": output})

@app.route('/')
def index():
    # Allows creation of new link
    return app.send_static_file('index.html')

if __name__ == '__main__':
    dbInit()
    app.run(host='127.0.0.1', port=5001)
