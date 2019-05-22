import os                                           # base python

from numpy import random, mean                      # site-packages
from PIL import Image, ImageDraw, ImageFont         # PIL is actually Pillow-SIMD (requires apt install zlib1g-dev libjpeg-dev)

from consts import *                                # our modules
from utils import *                                         


# ----- global variables -----
font_files = []
spot_images = []
attribute_metadata = ""


def superimpose_random_spot(target_image, dirt_level):
      
    spot_idx = random.randint(len(spot_images))
    spot = spot_images[spot_idx].copy()

    # make the spot randomly sized, while keeping aspect ratio
    spotW, spotH = spot.size
    newH = int(target_image.size[0] * random.randint(base_min_spotheight * dirt_level, base_max_spotheight + 10*(dirt_level-1) + 1) / 100)
    newW = int(newH * spotW / spotH)
    spot = spot.resize((newW, newH), Image.ANTIALIAS)

    # add the spot at random position
    randX = random.randint(0, img_size[0])
    randY = random.randint(0, img_size[1])

    # apply random transparency to spot
    pixel_data = spot.load()
    opacity = random.randint(base_min_spot_opacity + 10*(dirt_level-1), base_max_spot_opacity + 1) / 100
    if spot.mode == "RGBA":
        for y in range(newH):  # For each row ...
            for x in range(newW):  # For each column ...
                pixel_data[x, y] = (pixel_data[x, y][0], pixel_data[x, y][1],
                                    pixel_data[x, y][2], int(pixel_data[x, y][3] * opacity))

    x, y = spot.size
    target_image.paste(spot, (randX, randY, randX + x, randY + y), spot)


def create_dirty_images(text_cache, image_index):
    img = Image.new(img_mode, img_size, img_color)  # create new image object
    text = get_text(text_cache, min_text_lines, max_text_lines)
   
    # select text color (in HSV, for better control of what colors we get)
    # saturation > 0.5 guarantees text color won't be too pale
    text_color = hsv2rgb(random.uniform(0, 1), random.uniform(0.5, 1), random.uniform(0, 1))

    # select font
    fnt_size = random.randint(min_fontsize, max_fontsize + 1)  # size of font is randomly picked
    fnt = ImageFont.truetype(random.choice(font_files), fnt_size)
    # font_width, font_height = fnt.getsize(text)

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
    img.save(f'./output/{image_index:06}.jpg', format="jpeg")

    # write attribute metadata
    global attribute_metadata
    attribute_metadata += (f'{image_index:06}.jpg 1 ' + intensity_levels*'-1 ')[:-1] + '\n'

    if image_index%100==0: print(image_index)      # maintenance only
    create_dirt_levels(img, image_index)


def create_dirt_levels(img, idx):
    # add spots and save dirty images
    for lev in range(1, intensity_levels+1):
        temp = img.copy()

        num_spots = random.normal(base_num_spots + extra_num_spots*(lev-1), 1)
        for _ in range(int(round(num_spots))):
            superimpose_random_spot(temp, dirt_level=lev)

        temp.save(f'./output/{idx+lev:06}.jpg', format="jpeg")

        # write attribute metadata
        global attribute_metadata
        attribute_metadata += (f'{idx+lev:06}.jpg -1 ' + (lev-1)*'-1 ' + '1 ' + (intensity_levels-lev)*'-1 ')[:-1] + '\n'

# ----- main -----

def main():
    # upload font file paths from assets
    for root, _, files in os.walk(font_path):
        for file in files:
            if file.endswith('.ttf'):
                font_files.append(os.path.join(root, file))

    # upload spot file paths from assets
    for root, _, files in os.walk(spot_path):
        for file in files:
            if file.endswith(eligible_image_formats):
                spot_images.append(Image.open(os.path.join(root, file)).convert("RGBA"))

    # cache lines from the text file which we use for the images
    with open(txt_path, "r") as text_file:
        text_cache = text_file.readlines()

    # add header for attribute metadata file
    global attribute_metadata
    attribute_metadata = f'{NUMBER_OF_IMAGES}\nClean Stain_Level_1 Stain_Level_2 Stain_Level_3\n'

    for image_index in range(0, NUMBER_OF_IMAGES, intensity_levels+1):      # +1 for clean image (i.e. no dirt intensity)
        create_dirty_images(text_cache, image_index) 

    # dump attribute metadata to file 
    with open("list_attr_custom.txt", "w+") as attr_file:
        attr_file.write(attribute_metadata)

if __name__ == "__main__":
    main()
