# Dataset
The dataset is created by us, using Pillow library for Python 3.

Images are in size 00x400px.
* Using an Alice in Wonderland text file, `alice_in_wonderland.txt`, in order to generate sentences in English that will be put in the images.
* Using images found on the internet of transparent spots or stains - found on `images` folder.

## Input Images
We create the input images by taking a random sentence from the .txt file and putting it in a random position of the image.

## Output Images
We take the input image, and add to it a random image of spot/stain taken from the `images` folder.

We randomize some parameters:
 * Position of the added spot/stain
 * Angle of the image

After that, the output is saved.
