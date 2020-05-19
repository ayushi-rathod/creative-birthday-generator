from flask import Flask
from flask import request
from flask import jsonify
from pymongo import MongoClient
from pprint import pprint
from time import time
import random
import json

app = Flask(__name__)

secret = {}
try:
    json.loads(open('credential.json').read())
except FileNotFoundError as err:
    print('FileNotFoundError')
    secret['host'] = 'localhost'
    secret['port'] = '27017'
    secret['db'] = 'creativeengine'

connection = MongoClient('mongodb://{host}:{port}/{db}'.format(host=secret['host'], port=secret['port'], db=secret['db']))
def dbInit():
    try:
        dbnames = connection.list_database_names()
        if secret['db'] not in dbnames:
            db_api = connection[secret['db']].releaseinfo
            db_api.insert_one({
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
        print ("Database creation Failed!!")

@app.route('/genlink', methods = ['POST'])
def genlink():
    if request.method == 'POST':
        data = request.get_json()
        uniqueLink = ""
        mongoId = ""
        if data is not None:
            bdayEmail = data['bday_email']
            bdayName = data['bday_name']
            urlPhotoBday = data['bday_photo']
            
            userName = data['name_user']
            greetingText = data['greeting']
            urlPhotoUser = data['photo_user']

            uniqueInfo = connection[secret['db']].bdayusers.find_one({
                "email" : bdayEmail
            })

            if uniqueInfo is None:
                uniqueLink = str(bdayEmail).split('@')[0]
                bdayInfo = connection[secret['db']].bdayusers.insert_one({
                    "email" : bdayEmail,
                    "name" : bdayName,
                    "url" : urlPhotoBday,
                    "unilink" : uniqueLink
                })
                mongoId = bdayInfo.inserted_id

            if uniqueInfo is not None:
                return jsonify({"link": uniqueInfo["unilink"]})

            connection[secret['db']].bdayusers.insert_one({
                "bday_id": mongoId,
                "name": userName,
                "text": greetingText,
                "url_bday": urlPhotoBday,
                "url_user": urlPhotoUser
            })

        return jsonify({"unilink": uniqueLink})


@app.route('/bday/<unilink>')
def unique(uniqueLink):
    # Allows creation of new link
    uniqueInfo = connection[secret['db']].bdayusers.find_one({
        "unilink" : uniqueLink
    })
    if uniqueInfo is None:
        return index()
    return app.send_static_file('index.html?bday={}'.format(uniqueLink))

@app.route('/')
def index():
    # Allows creation of new link
    return app.send_static_file('index.html')

if __name__ == '__main__':
    dbInit()
    app.run(host='127.0.0.1', port=5001)
