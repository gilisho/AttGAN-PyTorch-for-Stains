from PIL import Image, ImageDraw, ImageFont
import read_txt_file_utils
import os
from numpy import random, mean
import colorsys
from consts import *

#----- helper functions -----
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def superimpose_random_spot(target_image, num_spots):
    spot = Image.open(random.choice(spot_files)).convert("RGBA")

    # make the spot randomly sized, while keeping aspect ratio
    spotW, spotH = spot.size
    newH = int(target_image.size[0] * random.randint(min_spotheight, max_spotheight+1) / 100)
    newW = int(newH * spotW / spotH)
    spot = spot.resize((newW, newH), Image.ANTIALIAS)

    # add the spot at random position
    randX = random.randint(0, img_size[0])
    randY = random.randint(0, img_size[1])
      
    # apply random transparency to spot
    pixel_data = spot.load()
    opacity = random.randint(min_spot_opacity, max_spot_opacity+1)
    if spot.mode == "RGBA":
        for y in range(spot.size[1]): # For each row ...
            for x in range(spot.size[0]): # For each column ...
                pixel_data[x,y] = (pixel_data[x,y][0], pixel_data[x,y][1],
                    pixel_data[x,y][2], int(pixel_data[x,y][3] * opacity / 100))

    x, y = spot.size
    target_image.paste(spot, (randX, randY, randX + x, randY + y), spot)

def create_dirty_image():
    img = Image.new(img_mode, img_size, img_color)  # create new image object
    text = read_txt_file_utils.read_txt_file(txt_path, min_text_lines, max_text_lines)

    # select text color (in HSV, for better control of what colors we get)
    # saturation > 0.5 guarantees text color won't be too pale
    text_color = hsv2rgb(random.uniform(0, 1), random.uniform(0.5, 1), random.uniform(0, 1))    

    # select font
    fnt_size = random.randint(min_fontsize, max_fontsize+1)  # size of font is randomly picked
    fnt = ImageFont.truetype(random.choice(font_files), fnt_size)
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

    # save 'clean' image
    img.save(f'./input_images/input-image-{i}-0.png')
    
    # add spots
    create_dirt_levels(img, i)


def create_dirt_levels(img, idx):

    for lev in range(num_levels):
        num_spots = random.normal(mean_spots_per_image + lev*extra_num_spots, 1)
        for _ in range(int(round(num_spots))):
            superimpose_random_spot(img, num_spots)

        img.save(f'./input_images/input-image-{idx}-{lev+1}.png', format="png")


# ------------main-----

#def main():
# upload font file paths from assets
font_files = []
for r, d, f in os.walk(font_path):       # r=root, d=directories, f=files
    for file in f:
        if file.endswith('.ttf'):
            font_files.append(os.path.join(r, file))

# upload spot file paths from assets
spot_files = []
for r, d, f in os.walk(spot_path):       # r=root, d=directories, f=files
    for file in f:
        if file.endswith(eligible_image_formats):
            spot_files.append(os.path.join(r, file))

# create a normal distribution for the number of spots on images
#num_spots = random.normal(mean_spots_per_image, 1, NUMBER_OF_IMAGES + 1)
#num_spots = [int(round(n)) for n in num_spots]

for i in range(NUMBER_OF_IMAGES + 1):
    create_dirty_image()


#if __name__ == "__main__":
#    main()


