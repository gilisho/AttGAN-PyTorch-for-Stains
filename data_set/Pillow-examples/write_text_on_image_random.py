from PIL import Image, ImageDraw, ImageFont
import read_txt_file_utils
import random

img_height, img_width = 500, 500
mode = 'RGB'
size = (img_height, img_width)  # size of image
color = 'white'  # background color

text = read_txt_file_utils.read_txt_file('../assets/alice_in_wonderland.txt')
text_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

img = Image.new(mode, size, color)  # create new image

# select font
fnt_size = random.randint(12, 30)  # size of font is randomly picked
fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', fnt_size)
font_width, font_height = fnt.getsize(text)

# select position of text
px = random.randint(font_height, 3)

# draw text on image
d = ImageDraw.Draw(img)
d.multiline_text((10, 10), text, font=fnt, fill=text_color)

# save image
img.save('./output_images/write_text_on_image_random.png')
