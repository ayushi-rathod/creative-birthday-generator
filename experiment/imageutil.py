from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# author: Prateek Rokadiya

# Example usage
# img = resizeByWidth(img, w, p)
# where, w = wanted width, p = padding (decreases more width)
def resizeByWidth(img, toWidth, padding = 20):
    new_width  = toWidth - padding
    new_height = new_width * img.size[1] // img.size[0] # Dimension w = img.size[0], h = img.size[1]
    return img.resize((new_width, new_height), Image.ANTIALIAS)

# Example usage
# img = resizeByHeight(img, h, p)
# where, w = wanted height, p = padding (decreases more height)
def resizeByHeight(img, toHeight, padding = 20):
    new_height = toHeight - padding
    new_width  = new_height * img.size[0] // img.size[1] # Dimension w = img.size[0], h = img.size[1]
    return img.resize((new_width, new_height), Image.ANTIALIAS)

def pasteImage(baseImage, overlayImage, pasteAtXY_tuple):
    baseImage.paste(overlayImage, pasteAtXY_tuple)
    # return baseImage.copy()

def writeGreeting(baseImage, XY, T, fontPath, FONT_SIZE, FONT_COLOR=(0, 0, 0)):

    def writeOnImage(baseImage, XY, text, fontPath, FONT_SIZE, FONT_COLOR=(0, 0, 0)):
        draw = ImageDraw.Draw(baseImage)

        font = ImageFont.truetype(fontPath, FONT_SIZE)
        draw.text(XY, text,fill=FONT_COLOR, font=font)
        del draw

    to, txt, frm = T
    # txt - break to a specific character length
    text = f'Dear {to},\n{txt}\n\t\t\t\t -From {frm}.'

    writeOnImage(baseImage, XY, text, fontPath, FONT_SIZE, FONT_COLOR)
