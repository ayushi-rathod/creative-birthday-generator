import json

secret = {}
try:
    secret = json.loads(open('credentials.json').read())
except FileNotFoundError as err:
    print('FileNotFoundError')
    secret['host'] = 'localhost'
    secret['port'] = '27017'
    secret['db'] = 'creativeengine'

class Connections:
    connect = ""
    def __init__(self, connect):
        self.connect = connect

    def addUser(self, uniqueLink, userName, userEmail, greetingText, urlPhotoBday, urlPhotoUser):
        return self.connect[secret['db']].users.insert_one({
            "unilink": uniqueLink,
            "name": userName,
            "email": userEmail,
            "text": greetingText,
            "url_bday": urlPhotoBday,
            "url_user": urlPhotoUser
        })

    def addBdayUser(self, uniqueLink, bdayName, bdayEmail, bdayDate, urlPhotoBday):
        return self.connect[secret['db']].bdayusers.insert_one({
            "unilink" : uniqueLink,
            "name" : bdayName,
            "email" : bdayEmail,
            "date" : bdayDate,
            "url" : urlPhotoBday
        })

    def findBdayUserByEmail(self, bdayEmail):
        return self.connect[secret['db']].bdayusers.find_one({
            "email" : bdayEmail
        })

    def findBdayUserByLink(self, unilink):
        return self.connect[secret['db']].bdayusers.find_one({
            "unilink" : unilink
        })

    def findUsersByLink(self, unilink):
        return self.connect[secret['db']].users.find({
            "unilink" : unilink
        })
