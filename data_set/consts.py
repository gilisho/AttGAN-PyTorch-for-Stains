# CONSTANTS FOR GENERATING INPUT IMAGES

img_mode = 'RGB'
img_size = (128, 128)  # size of image
img_color = 'white'  # background color of image

txt_path = 'assets/alice_in_wonderland.txt'
spot_path = 'assets/spots'
font_path = 'assets/fonts'
eligible_image_formats = ('.jpg', 'jpeg', '.png', '.webp', '.gif', '.tif', '.tiff')

min_text_lines = 4
max_text_lines = 15

min_fontsize = 12
max_fontsize = 24

base_min_spotheight = 5     # in % of the image height
base_max_spotheight = 30

base_min_spot_opacity = 30  # in %
base_max_spot_opacity = 75

base_num_spots = 3          # mean number of spots for the lowest dirt level
extra_num_spots = 5         # mean number of spots to add to each next dirt level

intensity_levels = 3  

NUMBER_OF_IMAGES = 1000 * (intensity_levels+1)  # number of images to generate
