from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from pymongo import MongoClient
from pprint import pprint
from time import time
import random
import json

app = Flask(__name__)

secret = {}
try:
    secret = json.loads(open('credentials.json').read())
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
    uniqueLink = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        # pprint(data)
        if data is not None:
            bdayName = data['bday_name']
            bdayEmail = data['bday_email']
            bdayDate = data['bday_date']
            urlPhotoBday = data['bday_photo']

            userName = data['user_name']
            userEmail = data["user_email"]
            greetingText = data['greeting']
            urlPhotoUser = data['user_photo']
            
            uniqueInfo = connection[secret['db']].bdayusers.find_one({
                "email" : bdayEmail
            })

            if uniqueInfo is None:
                uniqueLink = str(bdayEmail).split('@')[0]
                print('Print uniqueLink: ', uniqueLink)
                connection[secret['db']].bdayusers.insert_one({
                    "unilink" : uniqueLink,
                    "name" : bdayName,
                    "email" : bdayEmail,
                    "date" : bdayDate,
                    "url" : urlPhotoBday
                })

            if uniqueInfo is not None:
                return Response(json.dumps({'unilink':uniqueInfo['unilink']}), status=201, mimetype='application/json')

            connection[secret['db']].users.insert_one({
                "unilink": uniqueLink,
                "name": userName,
                "email": userEmail,
                "text": greetingText,
                "url_bday": urlPhotoBday,
                "url_user": urlPhotoUser
            })

    return jsonify({"unilink": uniqueLink})


@app.route('/bday/<unilink>')
def unique(unilink):
    # Allows creation of new link
    uniqueInfo = connection[secret['db']].bdayusers.find_one({
        "unilink" : unilink
    })
    if uniqueInfo is None:
        return index()
    return app.send_static_file('index.html?bday={}'.format(unilink))

@app.route('/bday/<unilink>', methods = ['POST'])
def saveData(unilink):
    if request.method == 'POST':
        # pprint(request)
        data = request.get_json()
        if data is not None:
            urlPhotoBday = data['bday_photo']
            
            userEmail = data['user_email']
            userName = data['user_name']
            greetingText = data['greeting']
            urlPhotoUser = data['user_photo']

            connection[secret['db']].bdayusers.insert_one({
                "unilink": unilink,
                "name": userName,
                "email": userEmail,
                "text": greetingText,
                "url_bday": urlPhotoBday,
                "url_user": urlPhotoUser
            })
    return jsonify({"unilink": unilink})



@app.route('/')
def index():
    # Allows creation of new link
    return app.send_static_file('index.html')

if __name__ == '__main__':
    dbInit()
    app.run(host='127.0.0.1', port=5001)
