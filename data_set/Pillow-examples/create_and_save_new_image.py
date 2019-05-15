from PIL import Image

mode = 'RGB'
size = (300, 300)  # size of image
color = (73, 109, 137)  # background color

img = Image.new(mode, size, color)
img.save('./output_images/create_and_save_new_image.png')
