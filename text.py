from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from urllib.request import urlopen
from io import BytesIO, StringIO
import pathlib

from imageutil import resizeByWidth, pasteImage, writeGreeting, cropImageByHeight, writeEmojis
from textutil import breakTextIntoLines

# from helper import quotes,font_size_sort
import random
import os
import csv


fontPath = "experiment/Sofia-Regular.otf"
fontPathSymbola = "experiment/Symbola.ttf"
FONT_SIZE = 70

padding = 100

emojis = {
    1: '😊',
    2: '🥳',
    3:'🎁',
    4:'💥',
    5:'🎨',
    6:'🧁',
    7:'🍥',
    8:'🎂',
    9:'🍰',
    10:'👻',
    11:'😈',
    12:'😍',
    13:'🥳',
    14:'🤩',
    15:'👑',
    16:'🌟',
    17:'⭐',
    18:'💫',
    19:'🔥',
    20:'💥',
    21:'🚀',
    22:'🎡',
    23:'🏖',
    24:'📸',
    25:'🧨',
    26:'💖',
    27:'🎉',
    28:'🎊',
    29:'🎁',
}

def getEmoji(emojis=emojis):
    num = random.randint(1, 29)
    # print(emojis[num])
    return(emojis[num])

def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def Card_Prep(bday_person_name, user_name, url, card_no, greeting_text): # ,font_path):
    # baseImg = Image.open("All_cards/"+str(card_no)+".jpg")
    baseImg = Image.open("experiment/blank.jpg") # it will be default.

    if 'http' in url:
        response = requests.get(url)
        bday_person_img = Image.open(BytesIO(response.content))
    else:
        bday_person_img = Image.open("experiment/All_cards/"+str(card_no)+".jpg")

    img_w, img_h = baseImg.size

    bday_person_img = resizeByWidth(bday_person_img, img_w, padding)

    # greeting_text break into lines and count lines. and get dimension of height is requires. 
    greeting_text, text_h = breakTextIntoLines(greeting_text)
    print("bi", baseImg.size)
    
    # if bday_person_img size [1] // height of reesized leaves space less then the text - crop the bday_person_img image 
    # by height (irrespective of content it loses in height)

    if (bday_person_img.size[1] + text_h + (2 * padding) > img_h):
        # Special case when text is too long and it needs to be fixed.
        new_h = img_h - text_h

        if (bday_person_img.size[1] - new_h) > (bday_person_img.size[1] // 2):
            # Resize by height - if file needs to crops by more than 50%.
            print(bday_person_img.size)
            bday_person_img = resizeByWidth(bday_person_img, new_h, padding)
            pasteImage(baseImg, bday_person_img, (padding//2 + (baseImg.size[0]//2 - bday_person_img.size[0]//2), padding//2))

        else:
            # crops height if crop is less than 50%.
            bday_person_img = cropImageByHeight(bday_person_img, (img_h - text_h - (4 * padding)))
            pasteImage(baseImg, bday_person_img, (padding//2, padding//2))
    else:
        # General case
        pasteImage(baseImg, bday_person_img, (padding//2, padding//2))
            
        # bday_person_img = cropImageByHeight(bday_person_img, (img_h - text_h - (2 * padding)))
        print(bday_person_img.size)

    newX = padding
    newY = bday_person_img.size[1] + padding
    writeGreeting(baseImg, (newX, newY), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)

    for i in range (1, random.randint(20, 60)):
        # write random number of emojis
        a, b = random.randint(0, baseImg.size[0]), random.randint(0, baseImg.size[1])
        # print("a,b", a, b)
        writeEmojis(baseImg, (a, b), getEmoji(), fontPathSymbola, random.randint(FONT_SIZE, 140), random_color())
    

    # writeGreeting(baseImg, (newX, newY), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)
    # (100, 2170)

    # baseImg.save(f'output/{bday_person_name}.jpg')
    # print(f'{bday_person_name} saved!')
    return baseImg

# path, dirs, files = next(os.walk("All_cards"))
# file_count = len(files)

# path1, dirs1, files1 = next(os.walk("All_font"))
# file_count1 = len(files1)
# rand_font = random.randint(0,file_count1)

# with open("bday_person_name.txt", "r") as f:
#     all_name = [row for row in csv.reader(f,delimiter=',')]


# def main(bday_person_name, user_name, greeting_text):
def main(bday_person_name, user_names, greeting_texts, user_photo_urls):
    # rand_quotes = random.randint(1, len(quotes))
    # rand_quotes = "This is a greeting from a brother. Happy Birthdayy my bro."
    # rand_card = random.randint(1, file_count)
    # rand_font = random.randint(0, file_count1-1)
    # rand_font = 'All_font/Great Wishes.otf'
    # print(bday_person_name, user_name, rand_card, greeting_text) #, files1[rand_font])
    img = []
    for user_name, greeting_text, url in zip(user_names, greeting_texts, user_photo_urls):
        img.append(Card_Prep(bday_person_name=bday_person_name, user_name=user_name, url=url, card_no=random.randint(1, 9), greeting_text=greeting_text)) # , path1 + '/' + files1[rand_font])

    # Save all images to gif.
    pathlib.Path('output').mkdir(parents=True, exist_ok=True) 

    img[0].save(f'output/{bday_person_name}.gif', save_all=True, append_images=img[1:], duration=1300, loop=0)

    # print(bday_person_name, rand_card, rand_quotes, rand_font)
    # Card_Prep(str(bday_person_name), rand_card, quotes[rand_quotes], rand_font)
    print("Done for {bday_person_name}".format(bday_person_name = bday_person_name))
#

# bday_person_name = "Prateek"
# user_names = ["UserFriend", "UserFriend2", "UserFriend3"]  
# greeting_texts = ["This is a greeting from a brother. Happy Birthdayy my bro.", "this is second message", "this is third message"]
# user_photo_urls = ["https://birthday-engine.s3-us-west-1.amazonaws.com/prateekro/folderpng-1590942671917.png", "https://birthday-engine.s3-us-west-1.amazonaws.com/prateekro/folderpng-1590942671917.png"]

# greeting_text = "Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro. \
# Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 \
# This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from \
# a brother.. Prateek UserFriend 10 This is a greeting from a brother.. Prateek UserFriend 10 This is a greeting from a brother. . Prateek UserFriend 10 This is a greeting from a brother. . Prateek UserFriend 10 This is a greeting from a brother."

# main(bday_person_name, user_names, greeting_texts, user_photo_urls)