# CONSTANTS FOR GENERATING INPUT IMAGES

NUMBER_OF_IMAGES = 3  # number of images to generate

img_mode = 'RGB'
img_size = (500, 500)  # size of image
img_color = 'white'  # background color of image

txt_path = 'assets/alice_in_wonderland.txt'
spot_path = 'assets/spots'
font_path = 'assets/fonts'
eligible_image_formats = ('.png', '.webp', '.gif', '.tif', '.tiff')

min_text_lines = 5
max_text_lines = 20

min_fontsize = 15
max_fontsize = 30

min_spotheight = 5  # in % of the image height
max_spotheight = 50

min_spot_opacity = 30  # in %
max_spot_opacity = 70

mean_spots_per_image = 3  # for normal distribution
extra_num_spots = 10  # num of spots to add to each dirt level

num_levels = 3
