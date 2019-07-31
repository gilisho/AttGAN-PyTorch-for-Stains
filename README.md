# AttGAN-PyTorch for Stains
Workshop in Machine Learning Applications for Computer Graphics, Tel-Aviv University, 2019.

## Authors

* **Chen Barnoy**
* **Gili Shohat**
* **Michael Glukhman**

## Description
Based on a [PyTorch implementation](https://github.com/elvisyjlin/AttGAN-PyTorch) of AttGAN - [Arbitrary Facial Attribute Editing: Only Change What You Want](https://arxiv.org/abs/1711.10678).

![Teaser](https://github.com/gilisho/GAN-project/blob/master/pics/teaser.jpg)
Test on the CelebA validating set

![Custom](https://github.com/gilisho/GAN-project/blob/master/pics/custom_testing.png)
Test on our custom set

## Requirements

* Python 3
* PyTorch 0.4.0
* TensorboardX

```bash
pip3 install -r requirements.txt
```

If you'd like to train with __multiple GPUs__, please install PyTorch __v0.4.0__ instead of v1.0.0 or above. The so-called stable version of PyTorch has a bunch of problems with regard to `nn.DataParallel()`. E.g. https://github.com/pytorch/pytorch/issues/15716, https://github.com/pytorch/pytorch/issues/16532, etc.

```bash
pip3 install --upgrade torch==0.4.0
```

* [Generated datasets (by stain types/by image dirtiness level](https://drive.google.com/drive/folders/1zEdaw-aJ4m5Wi2dUVro8tJcFwV94FGKG?usp=sharing)
    * Images should be placed in `./data/custom/*.jpg`
    * Attribute labels should be placed in `./data/list_attr_custom.txt`
  
* [Weights](https://drive.google.com/drive/folders/1zEdaw-aJ4m5Wi2dUVro8tJcFwV94FGKG?usp=sharing)

## Usage

#### To train an AttGAN on CelebA 128x128

```bash
CUDA_VISIBLE_DEVICES=0 \
python train.py \
--img_size 128 \
--shortcut_layers 1 \
--inject_layers 1 \
--experiment_name 128_shortcut1_inject1_none \
--gpu
```

#### To train an AttGAN on CelebA-HQ 256x256 with multiple GPUs

```bash
CUDA_VISIBLE_DEVICES=0 \
python train.py \
--data CelebA-HQ \
--img_size 256 \
--shortcut_layers 1 \
--inject_layers 1 \
--experiment_name 256_shortcut1_inject1_none_hq \
--gpu \
--multi_gpu
```

#### To visualize training details

```bash
tensorboard \
--logdir ./output
```

#### To test with single attribute editing

![Test](https://github.com/gilisho/GAN-project/blob/master/pics/sample_testing.jpg)

```bash
CUDA_VISIBLE_DEVICES=0 \
python test.py \
--experiment_name 128_shortcut1_inject1_none \
--test_int 1.0 \
--gpu
```

#### To test with multiple attributes editing

![Test Multi](https://github.com/gilisho/GAN-project/blob/master/pics/sample_testing_multi.jpg)

```bash
CUDA_VISIBLE_DEVICES=0 \
python test_multi.py \
--experiment_name 128_shortcut1_inject1_none \
--test_atts Pale_Skin Male \
--test_ints 0.5 0.5 \
--gpu
```

Example for our case (turning off clean attribute and turning on level 1 of image dirtiness:

```bash
CUDA_VISIBLE_DEVICES=0 \
python3 test_multi.py --experiment_name 128_shortcut1_inject1_none_16000_bytype \
--test_atts Clean  Stain_Level_1 \
--test_ints -1 1 \
--gpu \
--custom_img

```

#### To test with attribute intensity control

![Test Slide](https://github.com/gilisho/GAN-project/blob/master/pics/sample_testing_slide.jpg)

```bash
CUDA_VISIBLE_DEVICES=0 \
python test_slide.py \
--experiment_name 128_shortcut1_inject1_none \
--test_att black \
--test_int_min -1.0 \
--test_int_max 1.0 \
--n_slide 10 \
--gpu
```

#### To test with your custom images (supports `test.py`, `test_multi.py`, `test_slide.py`)

```bash
CUDA_VISIBLE_DEVICES=0 \
python test.py \
--experiment_name 384_shortcut1_inject1_none_hq \
--test_int 1.0 \
--gpu \
--custom_img
```

Your custom images are supposed to be in `./data/custom` and you also need an attribute list of the images `./data/list_attr_custom.txt`. Please crop and resize them into square images in advance.
