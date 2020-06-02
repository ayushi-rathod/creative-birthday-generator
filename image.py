# image.py

from PIL import Image
import awsconfig

# Trigger / make calls by birthdate///
#  - Create a queue of bday_users with birthdate. 
#  - Call AWS S3 folders by bday_users
#  - Process each folder
#  - Map greeting texts with picture.

def createArtifactFor(name):
    # name is albumName / unilink.
    print(name)

def openFolder(username):
    Image.open(username + "*" +'.jpg')

def downloadFolderFromAWS():
    print("")

if __name__ == "__main__":
    s3_client = awsconfig.connect_s3()
