import os

import numpy as np
from numpy import random
from PIL import Image, ImageDraw, ImageFont  # PIL is actually Pillow-SIMD (requires apt install zlib1g-dev libjpeg-dev)
from tqdm import tqdm
import argparse

import consts as defaults
import utils


class Selector():
    def __init__(self, font_path, spot_path, txt_path, eligible_image_formats, min_text_lines, max_text_lines,
                 min_font_size, max_font_size, spot_types, by_spot_types):
        self.spot_images_types = []
        self.font_files = self.__upload_font_files_from_path(font_path)        
        self.text_cache = self.__upload_txt_file_from_path(
            txt_path)  # text_cache is a list containing lines of text read beforehand from a text file
        self.min_text_lines = min_text_lines
        self.max_text_lines = max_text_lines
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size
        self.spot_types = spot_types.copy()
        self.spot_types.append('multi')
        if by_spot_types:
            utils.assert_that_each_spot_type_has_an_image(self.spot_images_types, spot_types)
        self.spot_images = self.__upload_spot_files_from_path(spot_path, eligible_image_formats, spot_types)

    @staticmethod
    def __upload_font_files_from_path(font_path):
        font_files = []
        for root, _, files in os.walk(font_path):
            for file in files:
                if file.endswith('.ttf'):
                    font_files.append(os.path.join(root, file))
        return font_files

    def __upload_spot_files_from_path(self, spot_path, eligible_image_formats, spot_types):
        spot_images = []
        for root, _, files in os.walk(spot_path):
            for file in files:
                file_spot_type = file.split('-')[0]
                if file.endswith(eligible_image_formats) and file_spot_type in spot_types:
                    self.spot_images_types.append(file_spot_type)
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

    def select_spot_for_image_by_type(self, desired_spot_type):
        spot_idx = random.randint(len(self.spot_images))
        spot = self.spot_images[spot_idx].copy()
        chosen_spot_type = self.spot_images_types[spot_idx]
        if desired_spot_type != 'multi':
            while chosen_spot_type != desired_spot_type:  # choose spot type until the desired type is chosen
                spot_idx = random.randint(len(self.spot_images))
                spot = self.spot_images[spot_idx].copy()
                chosen_spot_type = self.spot_images_types[spot_idx]
        return spot, chosen_spot_type

    def get_spot_types_order(self):
        shuffled = sorted(self.spot_types, key=lambda k: random.random())
        random.shuffle(shuffled)
        return shuffled


class ImageCreator():
    def __init__(self, args):
        self.img_num = args.img_num
        self.img_background_color = args.img_background_color
        self.img_mode = args.img_mode
        self.img_size = args.img_size
        self.random_spot_num = args.random_spot_num
        self.spot_min_opacity = args.spot_min_opacity
        self.spot_max_opacity = args.spot_max_opacity
        self.spot_base_min_height = args.spot_base_min_height
        self.spot_base_max_height = args.spot_base_max_height
        self.spot_grow_factor = args.spot_grow_factor
        self.spots_base_num = args.spots_base_num
        self.spots_extra_num = args.spots_extra_num
        self.intensity_levels = args.intensity_levels
        self.selector = Selector(args.font_path, args.spot_path, args.txt_path, args.eligible_image_formats,
                                 args.min_text_lines, args.max_text_lines,
                                 args.min_font_size, args.max_font_size, args.spot_types, args.by_spot_types)
        self.by_spot_types = args.by_spot_types
        self.spot_types = args.spot_types

        self.attribute_metadata = self.__get_attributes_metadata_header()
        self.output_folder_name = "custom_test" if args.for_testing else "custom"
        self.output_attr_filename = "list_attr_custom_test.txt" if args.for_testing else "list_attr_custom.txt"
        self.gaussian_noise = args.gaussian_noise
        self.__clean_output()

    def __get_attributes_metadata_header(self):
        ''' Adds header for attribute metadata file '''
        attr_metadata_header = f'{self.img_num}\n'
        if self.by_spot_types:
            attr_metadata_header += ' '.join(self.spot_types) + '\n'
        else:
            attr_metadata_header += 'Clean'
            for i in range(1, self.intensity_levels + 1):
                attr_metadata_header += f' Stain_Level_{i}'
            attr_metadata_header += '\n'
        return attr_metadata_header

    def __clean_output(self):
        ''' Cleans the output folders before creating the dataset '''
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

        temp = img.copy()
        # add noise
        if self.gaussian_noise:
            temp = self.add_gaussian_noise(temp)
        # save 'clean' image
        temp.save(f'./output/{self.output_folder_name}/{image_index:06}.jpg', format="jpeg")

        # write attribute metadata
        if self.by_spot_types:
            self.attribute_metadata += f'{image_index:06}.jpg ' + (len(self.spot_types) * '-1 ')[:-1] + '\n'
        else:
            self.attribute_metadata += (f'{image_index:06}.jpg 1 ' + self.intensity_levels * '-1 ')[
                                       :-1] + '\n'

        return img

    def superimpose_random_spot(self, target_image, dirt_level, desired_spot_type=''):

        if self.by_spot_types:
            spot, chosen_spot_type = self.selector.select_spot_for_image_by_type(desired_spot_type)
        else:
            spot = self.selector.select_spot_for_image()

        # make the spot randomly sized, while keeping aspect ratio
        spotW, spotH = spot.size
        img_width, img_height = target_image.size
        newH = int(img_height * (random.randint(self.spot_base_min_height, self.spot_base_max_height+1)+self.spot_grow_factor*(dirt_level-1))/100)
        newW = int(newH * spotW / spotH)
        spot = spot.resize((newW, newH), Image.ANTIALIAS)

        # add the spot at random position
        randX = random.randint(0, img_width)
        randY = random.randint(0, img_height)

        # apply random transparency to spot
        pixel_data = spot.load()
        opacity = random.randint(self.spot_min_opacity, self.spot_max_opacity + 1) / 100
        if spot.mode == "RGBA":
            for y in range(newH):  # For each row ...
                for x in range(newW):  # For each column ...
                    pixel_data[x, y] = (pixel_data[x, y][0], pixel_data[x, y][1],
                                        pixel_data[x, y][2], int(pixel_data[x, y][3] * opacity))

        x, y = spot.size
        target_image.paste(spot, (randX, randY, randX + x, randY + y), spot)
        return chosen_spot_type if self.by_spot_types else None

    def generate_dirty_images(self, img, image_index):
        '''
        Adds spots and save dirty images.
        :param img: clean image to add spots to
        :param image_index: index of the clean image
        '''
        if self.by_spot_types:
            self.generate_dirty_images_by_type(img, image_index)
        else:
            self.generate_dirty_images_by_intensity_level(img, image_index)

    def generate_dirty_images_by_type(self, img, image_index):
        '''
        Adds spots and save dirty images - by types dataset.
        In this function, all dirty output images are on the same dirtiness level.
        :param img: clean image to add spots to
        :param image_index: index of the clean image
        '''
        spot_types_including_multi = self.selector.get_spot_types_order()

        for i in range(len(spot_types_including_multi)):
            desired_spot_type = spot_types_including_multi[i]
            temp = img.copy()
            added_spots_vector = [0] * len(self.spot_types)

            # add gaussian noise
            if self.gaussian_noise:
                temp = self.add_gaussian_noise(temp)

            for _ in range(defaults.num_spots_by_types):
                added_spot_type = self.superimpose_random_spot(temp, dirt_level=defaults.dirt_level_by_types,
                                                               desired_spot_type=desired_spot_type)
                added_spots_vector[self.spot_types.index(added_spot_type)] += 1

            # write attribute metadata
            self.attribute_metadata += f'{image_index + (i + 1):06}.jpg ' + ' '.join(
                [('1' if n > 0 else '-1') for n in added_spots_vector]) + '\n'

            temp.save(f'./output/{self.output_folder_name}/{image_index + (i + 1):06}.jpg', format="jpeg")

    def generate_dirty_images_by_intensity_level(self, img, image_index):
        '''
        Adds spots and save dirty images - by intensity level dataset.
        In this function, we pick a random number of spots to add from a normal distribution, depending on the wanted
        intensity level.
        :param img: clean image to add spots to
        :param image_index: index of the clean image
        '''

        for lev in range(1, self.intensity_levels + 1):
            temp = img.copy()
            if self.random_spot_num:
                num_spots = random.normal(self.spots_base_num + self.spots_extra_num * (lev - 1), 1)
            else:
                num_spots = self.spots_base_num + self.spots_extra_num * (lev - 1)            

            # add gaussian noise
            if self.gaussian_noise:
                temp = self.add_gaussian_noise(temp)

            for _ in range(int(round(num_spots))):
                self.superimpose_random_spot(temp, dirt_level=lev)

            # write attribute metadata
            self.attribute_metadata += (f'{image_index + lev:06}.jpg -1 ' + (lev - 1) * '-1 ' + '1 ' + (
                    self.intensity_levels - lev) * '-1 ')[:-1] + '\n'

            temp.save(f'./output/{self.output_folder_name}/{image_index + lev:06}.jpg', format="jpeg")

    def dump_attr_metadata_to_file(self):
        ''' Creates a new file in output folder and dumps to it the attribute metadata '''
        with open(f'output/{self.output_attr_filename}', "w+") as attr_file:
            attr_file.write(self.attribute_metadata)
        attr_file.close()

    @staticmethod
    def add_gaussian_noise(img):
        '''
        Adds gaussian noise to the image.
        :param img: image to add gaussian noise to.
        :return: the input image after adding gaussian noise to it.
        '''
        img2arr = np.asarray(img)
        gauss_grayscale = [[[y]*3 for y in x] for x in random.normal(0, 0.4, img2arr.shape[:2])]
        img2arr = img2arr + gauss_grayscale
        img = Image.fromarray(np.uint8(img2arr))
        return img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_num', dest='img_num', type=utils.assert_img_num, required=True,
                        help='# of images to generate')
    parser.add_argument('--img_mode', dest='img_mode', type=str, default=defaults.img_mode)
    parser.add_argument('--img_size', dest='img_size', type=tuple, default=defaults.img_size)
    parser.add_argument('--img_background_color', dest='img_background_color', type=str,
                        default=defaults.img_background_color)

    parser.add_argument('--min_text_lines', dest='min_text_lines', type=int, default=defaults.min_text_lines)
    parser.add_argument('--max_text_lines', dest='max_text_lines', type=int, default=defaults.max_text_lines)
    parser.add_argument('--min_font_size', dest='min_font_size', type=int, default=defaults.min_font_size)
    parser.add_argument('--max_font_size', dest='max_font_size', type=int, default=defaults.max_font_size)

    parser.add_argument('--spot_min_opacity', dest='spot_min_opacity', type=int, default=defaults.spot_min_opacity,
                        help='%% of min opacity of added spots')
    parser.add_argument('--spot_max_opacity', dest='spot_max_opacity', type=int, default=defaults.spot_max_opacity,
                        help='%% of max opacity of added spots')
    parser.add_argument('--spot_base_min_height', dest='spot_base_min_height', type=int,
                        default=defaults.spot_base_min_height, help='min %% of the image height an added spot will take')
    parser.add_argument('--spot_base_max_height', dest='spot_base_max_height', type=int,
                        default=defaults.spot_base_max_height, help='max %% of the image height an added spot will take')
    parser.add_argument('--spot_grow_factor', dest='spot_grow_factor', type=int,
                        default=defaults.spot_grow_factor, help='additional %% of the image height spot take, per dirtiness level')

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

    parser.add_argument('--by_spot_types', dest='by_spot_types', action='store_true',
                        help='indicates whether the attributes are set by spot type or by intensity level of dirtiness')
    parser.add_argument('--spot_types', dest='spot_types', nargs='+', default=defaults.spot_types)
    parser.add_argument('--for_testing', dest='for_testing', default=False, action='store_true',
                        help='indicates whether dataset is for testing')

    parser.add_argument('--random_spot_num', dest='random_spot_num', default=defaults.random_spot_num,
                        action='store_true',
                        help='indicates whether the spot number is normally distributed or constant for each level')

    parser.add_argument('--gaussian_noise', dest='gaussian_noise', action='store_true',
                        help='indicates whether to add gaussian noise to all images')

    arguments = parser.parse_args()

    img_creator = ImageCreator(arguments)

    img_index_step = len(
        arguments.spot_types) + 1 if arguments.by_spot_types else arguments.intensity_levels  # +1 for 'multi' spot type
    img_index_step += 1  # +1 for clean image type

    for img_index in tqdm(range(0, arguments.img_num, img_index_step)):
        clean_image = img_creator.generate_clean_image(img_index)
        img_creator.generate_dirty_images(clean_image, img_index)

    img_creator.dump_attr_metadata_to_file()
