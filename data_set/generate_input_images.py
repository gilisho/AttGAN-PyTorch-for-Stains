import os

from numpy import random
from PIL import Image, ImageDraw, ImageFont  # PIL is actually Pillow-SIMD (requires apt install zlib1g-dev libjpeg-dev)
from tqdm import tqdm
import argparse

import consts as defaults
import utils


class Selector():
    def __init__(self, font_path, spot_path, txt_path, eligible_image_formats, min_text_lines, max_text_lines,
                 min_font_size, max_font_size):
        self.font_files = self.__upload_font_files_from_path(font_path)
        self.spot_images = self.__upload_spot_files_from_path(spot_path, eligible_image_formats)
        self.text_cache = self.__upload_txt_file_from_path(
            txt_path)  # text_cache is a list containing lines of text read beforehand from a text file
        self.min_text_lines = min_text_lines
        self.max_text_lines = max_text_lines
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size

    @staticmethod
    def __upload_font_files_from_path(font_path):
        font_files = []
        for root, _, files in os.walk(font_path):
            for file in files:
                if file.endswith('.ttf'):
                    font_files.append(os.path.join(root, file))
        return font_files

    @staticmethod
    def __upload_spot_files_from_path(spot_path, eligible_image_formats):
        spot_images = []
        for root, _, files in os.walk(spot_path):
            for file in files:
                if file.endswith(eligible_image_formats):
                    spot_images.append(Image.open(os.path.join(root, file)).convert("RGBA"))
        return spot_images

    @staticmethod
    def __upload_txt_file_from_path(txt_path):
        # cache lines from the text file which we use for the images
        with open(txt_path, "r") as text_file:
            text_cache = text_file.readlines()
            return text_cache

    def select_text_for_image(self):
        output_text = ''
        num_lines_in_source = len(self.text_cache)
        num_lines_in_output = random.randint(self.min_text_lines, self.max_text_lines + 1)
        for _ in range(num_lines_in_output):
            line_num = random.randint(0, num_lines_in_source)  # take randomly a line and add it to output_text
            output_text += self.text_cache[line_num]
        return output_text

    def select_text_font_for_image(self):
        font_size = random.randint(self.min_font_size, self.max_font_size + 1)  # size of font is randomly picked
        font = ImageFont.truetype(random.choice(self.font_files), font_size)
        return font

    def select_spot_for_image(self):
        spot_idx = random.randint(len(self.spot_images))
        spot = self.spot_images[spot_idx].copy()
        return spot


class ImageCreator():
    def __init__(self, args):
        self.img_num = args.img_num
        self.img_background_color = args.img_background_color
        self.img_mode = args.img_mode
        self.img_size = args.img_size
        self.spot_min_opacity = args.spot_min_opacity
        self.spot_max_opacity = args.spot_max_opacity
        self.spot_base_min_height = args.spot_base_min_height
        self.spot_base_max_height = args.spot_base_max_height
        self.spots_base_num = args.spots_base_num
        self.spots_extra_num = args.spots_extra_num
        self.intensity_levels = args.intensity_levels
        self.selector = Selector(args.font_path, args.spot_path, args.txt_path, args.eligible_image_formats,
                                 args.min_text_lines, args.max_text_lines,
                                 args.min_font_size, args.max_font_size)
        self.attribute_metadata = f'{args.img_num}\nClean Stain_Level_1 Stain_Level_2 Stain_Level_3\n'  # add header for attribute metadata file
        self.output_folder_name = "custom_test" if (args.for_testing in args) else "custom"
        self.output_attr_filename = "list_attr_custom_test.txt" if args.for_testing else "list_attr_custom.txt"
        self.__clean_output()

    def __clean_output(self):
        self.__clean_output_folder()
        self.__clean_output_attr_file()

    def __clean_output_folder(self):
        for file in os.scandir(f'output/{self.output_folder_name}'):
            os.remove(file.path)

    def __clean_output_attr_file(self):
        file_path = f'output/{self.output_attr_filename}'
        if os.path.exists(file_path):
            os.remove(file_path)

    def generate_clean_image(self, image_index):
        img_text = self.selector.select_text_for_image()
        img_font = self.selector.select_text_font_for_image()
        img = Image.new(self.img_mode, self.img_size, self.img_background_color)  # create new image object

        # select text color (in HSV, for better control of what colors we get)
        # saturation > 0.5 guarantees text color won't be too pale
        text_color = utils.hsv2rgb(random.uniform(0, 1), random.uniform(0.5, 1), random.uniform(0, 1))

        # draw text on image
        image_with_text = Image.new(self.img_mode, size=self.img_size, color=self.img_background_color)
        d = ImageDraw.Draw(image_with_text)
        d.multiline_text((0, 0), text=img_text, font=img_font, fill=text_color)

        # rotate image
        angle = random.randint(-90, 91)
        image_with_text = image_with_text.rotate(angle, expand=1, fillcolor=self.img_background_color)

        # paste image_with_text on img
        px, py = 0, 0
        sx, sy = image_with_text.size
        img.paste(image_with_text, (px, py, px + sx, py + sy))

        # save 'clean' image
        img.save(f'./output/{self.output_folder_name}/{image_index:06}.jpg', format="jpeg")

        # write attribute metadata
        self.attribute_metadata += (f'{image_index:06}.jpg 1 ' + self.intensity_levels * '-1 ')[
                                   :-1] + '\n'

        return img

    def superimpose_random_spot(self, target_image, dirt_level):
        spot = self.selector.select_spot_for_image()

        # make the spot randomly sized, while keeping aspect ratio
        spotW, spotH = spot.size
        img_width, img_height = target_image.size
        newH = int(img_height * random.randint(self.spot_base_min_height * dirt_level,
                                               self.spot_base_max_height + 10 * (dirt_level - 1) + 1) / 100)
        newW = int(newH * spotW / spotH)
        spot = spot.resize((newW, newH), Image.ANTIALIAS)

        # add the spot at random position
        randX = random.randint(0, img_width)
        randY = random.randint(0, img_height)

        # apply random transparency to spot
        pixel_data = spot.load()
        opacity = random.randint(self.spot_min_opacity + 10 * (dirt_level - 1), self.spot_max_opacity + 1) / 100
        if spot.mode == "RGBA":
            for y in range(newH):  # For each row ...
                for x in range(newW):  # For each column ...
                    pixel_data[x, y] = (pixel_data[x, y][0], pixel_data[x, y][1],
                                        pixel_data[x, y][2], int(pixel_data[x, y][3] * opacity))

        x, y = spot.size
        target_image.paste(spot, (randX, randY, randX + x, randY + y), spot)

    def generate_dirty_images(self, img, image_index):
        # add spots and save dirty images
        for lev in range(1, self.intensity_levels + 1):
            temp = img.copy()

            num_spots = random.normal(self.spots_base_num + self.spots_extra_num * (lev - 1), 1)
            for _ in range(int(round(num_spots))):
                self.superimpose_random_spot(temp, dirt_level=lev)

            temp.save(f'./output/{self.output_folder_name}/{image_index + lev:06}.jpg', format="jpeg")

            # write attribute metadata
            self.attribute_metadata += (f'{image_index + lev:06}.jpg -1 ' + (lev - 1) * '-1 ' + '1 ' + (
                    self.intensity_levels - lev) * '-1 ')[:-1] + '\n'

    def dump_attr_metadata_to_file(self):
        with open(f'output/{self.output_attr_filename}', "w+") as attr_file:
            attr_file.write(self.attribute_metadata)


def check_img_num(value):
    '''
    check whether number of images to generate divides in 4 (the intensity level)
    :param value: the arg for img_num to pass
    :return: the value inserted by user, if value is ok. else, an error is thrown.
    '''
    ivalue = int(value)
    if ivalue % 4 != 0:
        raise argparse.ArgumentTypeError(
            "Make sure img_num divides in 4. %s is an invalid images number to generate." % value)
    return ivalue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_num', dest='img_num', type=check_img_num, required=True, help='# of images to generate')
    parser.add_argument('--img_mode', dest='img_mode', type=str, default=defaults.img_mode)
    parser.add_argument('--img_size', dest='img_size', type=tuple, default=defaults.img_size)
    parser.add_argument('--img_background_color', dest='img_background_color', type=str,
                        default=defaults.img_background_color)

    parser.add_argument('--min_text_lines', dest='min_text_lines', type=int, default=defaults.min_text_lines)
    parser.add_argument('--max_text_lines', dest='max_text_lines', type=int, default=defaults.max_text_lines)
    parser.add_argument('--min_font_size', dest='min_font_size', type=int, default=defaults.min_font_size)
    parser.add_argument('--max_font_size', dest='max_font_size', type=int, default=defaults.max_font_size)

    parser.add_argument('--spot_min_opacity', dest='spot_min_opacity', type=int, default=defaults.spot_min_opacity,
                        help='% of min opacity of added spots')
    parser.add_argument('--spot_max_opacity', dest='spot_max_opacity', type=int, default=defaults.spot_max_opacity,
                        help='% of max opacity of added spots')
    parser.add_argument('--spot_base_min_height', dest='spot_base_min_height', type=int,
                        default=defaults.spot_base_min_height,
                        help='% of the min height the added spots will take image added spots')
    parser.add_argument('--spot_base_max_height', dest='spot_base_max_height', type=int,
                        default=defaults.spot_base_max_height, help='% of the max height of added spots')
    parser.add_argument('--spots_base_num', dest='spots_base_num', type=int, default=defaults.spots_base_num,
                        help='number of spots for the lowest dirt level')
    parser.add_argument('--spots_extra_num', dest='spots_extra_num', type=int, default=defaults.spots_extra_num,
                        help='number of spots to add to each next intensity level')
    parser.add_argument('--intensity_levels', dest='intensity_levels', type=int, default=defaults.intensity_levels,
                        help='number of levels of dirtiness (excluding clean level)')

    parser.add_argument('--font_path', dest='font_path', type=str, default=defaults.font_path)
    parser.add_argument('--spot_path', dest='spot_path', type=str, default=defaults.spot_path)
    parser.add_argument('--txt_path', dest='txt_path', type=str, default=defaults.txt_path)
    parser.add_argument('--img_formats', dest='eligible_image_formats', nargs='+',
                        default=defaults.eligible_image_formats)

    parser.add_argument('--by_stain_levels', dest='by_stain_levels', action='store_true')
    parser.add_argument('--for_testing', dest='for_testing', default=False, action='store_true',
                        help='indicates whether dataset is for testing')

    arguments = parser.parse_args()

    img_creator = ImageCreator(arguments)

    for img_index in tqdm(range(0, arguments.img_num,
                                arguments.intensity_levels + 1)):  # +1 for clean image (i.e. no dirt intensity)
        clean_image = img_creator.generate_clean_image(img_index)
        img_creator.generate_dirty_images(clean_image, img_index)

    img_creator.dump_attr_metadata_to_file()
