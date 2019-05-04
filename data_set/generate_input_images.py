from PIL import Image, ImageDraw, ImageFont
import read_txt_file_utils
import random
from consts import *

for i in range(NUMBER_OF_IMAGES + 1):
    text = read_txt_file_utils.read_txt_file(txt_path)
    text_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

    img = Image.new(img_mode, img_size, img_color)  # create new image object

    # select font
    fnt_size = random.randint(15, 30)  # size of font is randomly picked
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', fnt_size)
    font_width, font_height = fnt.getsize(text)

    # draw text on image
    image_with_text = Image.new(img_mode, size=img_size, color=img_color)
    d = ImageDraw.Draw(image_with_text)
    d.multiline_text((0, 0), text=text, font=fnt, fill=text_color)

    # rotate image
    angle = random.randint(-90, 91)
    image_with_text = image_with_text.rotate(angle, expand=1, fillcolor=img_color)

    # paste image_with_text on img
    px, py = 0, 0
    sx, sy = image_with_text.size
    img.paste(image_with_text, (px, py, px + sx, py + sy))

    # save image
    img.save(f'./input_images/input-image-{i}.png')
