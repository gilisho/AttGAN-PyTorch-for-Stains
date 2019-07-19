# CONSTANTS FOR GENERATING INPUT IMAGES

img_mode = 'RGB'
img_size = (128, 128)  # size of image
img_background_color = 'white'  # background color of image

txt_path = 'assets/alice_in_wonderland.txt'
spot_path = 'assets/spots'
font_path = 'assets/fonts'
eligible_image_formats = ('.jpg', 'jpeg', '.png', '.webp', '.gif', '.tif', '.tiff')

min_text_lines = 4
max_text_lines = 15

min_font_size = 12
max_font_size = 24

spot_base_min_height = 10  # in % of the image height
spot_base_max_height = 10
spot_grow_factor = 2

spot_min_opacity = 35  # in %
spot_max_opacity = 75

spots_base_num = 4  # mean number of spots for the lowest dirt level
spots_extra_num = 8  # mean number of spots to add to each next dirt level

random_spot_num = False
intensity_levels = 3

spot_types = ['black', 'coffee']
num_spots_by_types = 8
dirt_level_by_types = 2
