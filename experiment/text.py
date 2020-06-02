from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from imageutil import resizeByWidth, pasteImage, writeGreeting, cropImageByHeight
from textutil import breakTextIntoLines

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
    print()

    bday_person_img = resizeByWidth(bday_person_img, img_w, padding)
    greeting_text, text_h = breakTextIntoLines(greeting_text)
    print("bi", baseImg.size)
    print(bday_person_img.size[1] + text_h + (2 * padding))
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
            bday_person_img = cropImageByHeight(bday_person_img, (img_h - text_h - (2 * padding)))
            pasteImage(baseImg, bday_person_img, (padding//2, padding//2))
    else:
        # General case
        pasteImage(baseImg, bday_person_img, (padding//2, padding//2))
            

        # bday_person_img = cropImageByHeight(bday_person_img, (img_h - text_h - (2 * padding)))
        print(bday_person_img.size)

    # print(greeting_text)
    # baseImg.paste(bday_person_img, (padding//2, padding//2))
    
    # TODO - if bday_person_img size [1] // height of reesized leaves space less then the text - crop the bday_person_img image 
    # by height (irrespective of content it loses in height)

    # TODO - greeting_text break into lines and count lines. and get dimension of height is requires. 

    newX = padding
    # newY = bday_person_img.size[1] + (2 * padding)
    newY = bday_person_img.size[1] + padding
    writeGreeting(baseImg, (newX, newY), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)
    # writeGreeting(baseImg, (100, 2170), (bday_person_name, greeting_text, user_name), fontPath, FONT_SIZE)

    print()
    # baseImg.save('output/test.jpg', "JPEG")

    # 

    # draw = ImageDraw.Draw(baseImg)

    # font = ImageFont.truetype(fontPath, FONT_SIZE)
    # draw.text((100, 2170), f'Dear {bday_person_name},\n{greeting_text}\n     '
    #                        f'                                -From {user_name}.',(0, 0, 0), font=font)
    # baseImg.save(f'output/{bday_person_name}.jpg')
    return baseImg
    print(f'{bday_person_name} saved!')

path, dirs, files = next(os.walk("All_cards"))
file_count = len(files)

# path1, dirs1, files1 = next(os.walk("All_font"))
# file_count1 = len(files1)
# rand_font = random.randint(0,file_count1)

# with open("bday_person_name.txt", "r") as f:
#     all_name = [row for row in csv.reader(f,delimiter=',')]


# def main(bday_person_name, user_name, greeting_text):
def main(bday_person_name, user_names, greeting_texts):
    # rand_quotes = random.randint(1, len(quotes))
    # rand_quotes = "This is a greeting from a brother. Happy Birthdayy my bro."
    rand_card = random.randint(1, file_count)
    # rand_font = random.randint(0, file_count1-1)
    # rand_font = 'All_font/Great Wishes.otf'
    # print(bday_person_name, user_name, rand_card, greeting_text) #, files1[rand_font])
    img = []
    for user_name, greeting_text in zip(user_names, greeting_texts):
        img.append(Card_Prep(bday_person_name, user_name, rand_card, greeting_text)) # , path1 + '/' + files1[rand_font])

    img[0].save(f'output/{bday_person_name}.gif', save_all=True, append_images=img[1:], duration=1300, loop=0)

    # print(bday_person_name, rand_card, rand_quotes, rand_font)
    # Card_Prep(str(bday_person_name), rand_card, quotes[rand_quotes], rand_font)
    print("Done for {bday_person_name}".format(bday_person_name = bday_person_name))
#

bday_person_name = "Prateek"
user_names = ["UserFriend", "UserFriend2", "UserFriend3"]  
greeting_texts = ["This is a greeting from a brother. Happy Birthdayy my bro.", "this is second message", "this is third message"]
# greeting_text = "Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro. \
# Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 \
# This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother.Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from \
# a brother.. Prateek UserFriend 10 This is a greeting from a brother.. Prateek UserFriend 10 This is a greeting from a brother. . Prateek UserFriend 10 This is a greeting from a brother. . Prateek UserFriend 10 This is a greeting from a brother."

main(bday_person_name, user_names, greeting_texts)