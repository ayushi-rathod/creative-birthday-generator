# image.py

from PIL import Image
import awsconfig
from connection import Connections
from pprint import pprint
from text import main

# Trigger / make calls by birthdate///
#  - Create a queue of bday_users with birthdate. 
#  - Call AWS S3 folders by bday_users
#  - Process each folder
#  - Map greeting texts with picture.

def createArtifactFor(s3_client, mongoconn, name):
    # s3_client
    # mongoconn
    users = mongoconn.findUsersByLink(name)
    all_urls = awsconfig.get_s3_bucket_contents(s3_client)

    filter(lambda x: x.startswith(name), all_urls)

    pprint(all_urls)

    userx = []
    user_names = []
    greeting_texts = []
    user_urls = []
    for user in users:
        # pprint(user)
        print(user['name'], user['email'], user['text'], user['url_user'])
        urlendswith = user['url_user'].split('-').pop()
        urlx = ''
        for url in all_urls:
            if urlendswith in url:
                urlx = 'https://birthday-engine.s3-us-west-1.amazonaws.com/'+url
        userx.append((user['name'], user['email'], user['text'], urlx))
        
        user_names.append(user['name'])
        greeting_texts.append(user['text'])
        user_urls.append(urlx)

        # to get picture = match first part of email in image name.
    # bday_person_name
    # user_names
    # greeting_texts
    # user_urls

    print(name)
    print()
    print(userx)
    if len(userx) > 0:
        main(name, user_names, greeting_texts, user_urls)
    else:
        # Create case of default output using some default inputs
        main(name, ['user_names'], ['Happy Birthday!'], ['user_urls'])
        print("Create case of default output")

    # name is albumName / unilink.
    # get album from aws
    # get users from mongo
    # map / match user regex with picture name in album
    # and there greetings
    # And send to users emails.

# def openFolder(username):
#     Image.open(username + "*" +'.jpg')

# def downloadFolderFromAWS():
#     print("")

# if __name__ == "__main__":
#     s3_client = awsconfig.connect_s3()
