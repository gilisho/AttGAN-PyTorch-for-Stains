from colorsys import hsv_to_rgb
import argparse


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def assert_img_num(value):
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


def assert_that_each_spot_type_has_an_image(spot_images_types, spot_types):
    for i in range(len(spot_types)):
        has_image = False
        for j in range(len(spot_images_types)):
            if spot_types[i] == spot_images_types[j]:
                has_image = True
                break
        if not has_image:
            raise argparse.ArgumentTypeError(
                "%s has no spot image in the spots folder! Make sure to add at least one spot there." % spot_types[i])
