# Dataset
The dataset is created by us, using the Pillow library for Python 3.
Images are in size 128x128px.

The `assets` folder contains all the data files required to create the dataset images:
* Alice in Wonderland text file, `assets/alice_in_wonderland.txt` - used in order to generate sentences in English that will be put in the images.
* Images found on the internet of transparent spots or stains - located in `assets/spots` folder.
* Fonts for texts in images - located in `assets/fonts` folder.

## Generated Images
We create the images by taking random sentences from the .txt file and putting it in a random position of the image.
We take a clean generated image and add to it a random image of spot taken from the `assets/spots` folder.

We randomize some parameters:
 * Position of the added spot/stain
 * Angle of the image
 * The number of spots is selected from a normal distribution (configurable)
 
## Attribute List
We save a .txt file describing the attributes for every image created.
The file format is:
  * Number of images in batch
  * Names of the attributes
  * Image name and for each attribute, 1 if the image has it or -1 if not.
  
For example:
```
3

Clean Stain_Level_1 Stain_Level_2 Stain_Level_3

000000.jpg 1 -1 -1 -1

000001.jpg -1 1 -1 -1

000002.jpg -1 -1 1 -1
```


After that, the output is saved in the `data` folder.

## Usage

#### To create a new dataset containing 12000 images with two intensity (dirtiness of image) levels

```bash
python3 generate_input_images.py \
--img_num 12000
--intensity_levels 2
```

#### To create a new dataset containing 12000 images, classified by stain types, with gaussian noise in all images

```bash
python3 generate_input_images.py \
--img_num 12000
--by_spot_types
--gaussian_noise
```
