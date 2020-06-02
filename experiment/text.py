from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
# from helper import quotes,font_size_sort
import random
import os
import csv


fontPath = "Sofia-Regular.otf"
FONT_SIZE = 70

def Card_Prep(bday_person_name, user_name, card_no, greeting_text): # ,font_path):
    img = Image.open("All_cards/"+str(card_no)+".jpg")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(fontPath, FONT_SIZE)
    draw.text((100, 2170), f'Dear {bday_person_name},\n{greeting_text}\n     '
                           f'                                -From {user_name}.',(0, 0, 0), font=font)
    img.save(f'output/{bday_person_name}.jpg')
    print(f'{bday_person_name} saved!')

path, dirs, files = next(os.walk("All_cards"))
file_count = len(files)

path1, dirs1, files1 = next(os.walk("All_font"))
file_count1 = len(files1)
# rand_font = random.randint(0,file_count1)

# with open("bday_person_name.txt", "r") as f:
#     all_name = [row for row in csv.reader(f,delimiter=',')]


def main(bday_person_name, user_name):
    # rand_quotes = random.randint(1, len(quotes))
    rand_quotes = "This is a greeting from a brother. Happy Birthdayy my bro."
    rand_card = random.randint(1, file_count)
    rand_font = random.randint(0, file_count1-1)
    # rand_font = 'All_font/Great Wishes.otf'
    # print(bday_person_name)
    print(bday_person_name, rand_card, rand_quotes, files1[rand_font])
    Card_Prep(bday_person_name, user_name, rand_card, rand_quotes) # , path1 + '/' + files1[rand_font])
    # print(bday_person_name, rand_card, rand_quotes, rand_font)
    # Card_Prep(str(bday_person_name), rand_card, quotes[rand_quotes], rand_font)
    print(f'Done for {bday_person_name}')
#

bday_person_name = "Prateek"
user_name = "UserFriend"
main(bday_person_name, user_name)