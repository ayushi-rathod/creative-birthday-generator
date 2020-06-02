from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
# from resizeimage import resizeimage

from imageutil import resizeByWidth, pasteImage, writeGreeting

# from helper import quotes,font_size_sort
import random
import os
import csv


fontPath = "Sofia-Regular.otf"
FONT_SIZE = 70

padding = 100

def Card_Prep(bday_person_name, user_name, card_no, greeting_text): # ,font_path):
    # img = Image.open("All_cards/"+str(card_no)+".jpg")
    baseImg = Image.open("blank.jpg")

    # 
    bday_person_img = Image.open("bdayimg.jpg")
    b_w, b_h = bday_person_img.size
    img_w, img_h = baseImg.size
    # bday_person_img = resizeimage.resize_height(bday_person_img, (img_h - 50))
    print()

    bday_person_img = resizeByWidth(bday_person_img, img_w, padding)
    # baseImg.paste(bday_person_img, (padding//2, padding//2))
    
    # TODO - if bday_person_img size [1] // height of reesized leaves space less then the text - crop the bday_person_img image 
    # by height (irrespective of content it loses in height)

    # TODO - greeting_text break into lines and count lines. and get dimension of height is requires.

    pasteImage(baseImg, bday_person_img, (padding//2, padding//2))

    newX = padding
    newY = bday_person_img.size[1] + (2 * padding)
    writeGreeting(baseImg, (newX, newY), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)
    # writeGreeting(baseImg, (100, 2170), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)

    print()
    baseImg.save('output/test.jpg', "JPEG")

    # 

    draw = ImageDraw.Draw(baseImg)

    font = ImageFont.truetype(fontPath, FONT_SIZE)
    draw.text((100, 2170), f'Dear {bday_person_name},\n{greeting_text}\n     '
                           f'                                -From {user_name}.',(0, 0, 0), font=font)
    baseImg.save(f'output/{bday_person_name}.jpg')
    print(f'{bday_person_name} saved!')

path, dirs, files = next(os.walk("All_cards"))
file_count = len(files)

# path1, dirs1, files1 = next(os.walk("All_font"))
# file_count1 = len(files1)
# rand_font = random.randint(0,file_count1)

# with open("bday_person_name.txt", "r") as f:
#     all_name = [row for row in csv.reader(f,delimiter=',')]


def main(bday_person_name, user_name, greeting_text):
    # rand_quotes = random.randint(1, len(quotes))
    # rand_quotes = "This is a greeting from a brother. Happy Birthdayy my bro."
    rand_card = random.randint(1, file_count)
    # rand_font = random.randint(0, file_count1-1)
    # rand_font = 'All_font/Great Wishes.otf'
    print(bday_person_name, user_name, rand_card, greeting_text) #, files1[rand_font])
    Card_Prep(bday_person_name, user_name, rand_card, greeting_text) # , path1 + '/' + files1[rand_font])
    # print(bday_person_name, rand_card, rand_quotes, rand_font)
    # Card_Prep(str(bday_person_name), rand_card, quotes[rand_quotes], rand_font)
    print("Done for {bday_person_name}".format(bday_person_name = bday_person_name))
#

bday_person_name = "Prateek"
user_name = "UserFriend"
greeting_text = "This is a greeting from a brother. Happy Birthdayy my bro."
main(bday_person_name, user_name, greeting_text)