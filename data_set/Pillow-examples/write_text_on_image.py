from PIL import Image, ImageDraw, ImageFont

mode = 'RGB'
size = (400, 400) # size of image
color = (73, 109, 137) # background color

img = Image.new(mode, size, color) # create new image

# select font
fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)

# draw text on image
text = "Hello World hdfakhdohf o dho\n ifohao hoh osi hiodhioshiof os oiadoh\n oifhioshiof a"
d = ImageDraw.Draw(img)
d.multiline_text((10,10), text, font=fnt, fill=(255,255,0))

# save image
img.save('./output_images/write_text_on_image.png')
