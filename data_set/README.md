# Dataset
The dataset is created by us, using Pillow library for Python 3.
Images are in size 400x400px.

The `assets` folder contains all the data files required to create the dataset images:
* Alice in Wonderland text file, `assets/alice_in_wonderland.txt` - used in order to generate sentences in English that will be put in the images.
* Images found on the internet of transparent spots or stains - located in `assets/images` folder.

## Input Images
We create the input images by taking a random sentence from the .txt file and putting it in a random position of the image.

## Output Images
We take the input image, and add to it a random image of spot/stain taken from the `assets/images` folder.

We randomize some parameters:
 * Position of the added spot/stain
 * Angle of the image

After that, the output is saved.
