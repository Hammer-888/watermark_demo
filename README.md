# Digital image encryption ---- invisible watermark

## Introduction

Invisible watermark contains two algorithms: significant Bit(LSB) and Discrete Cosine Transform(DCT) refer [guofei9987](github.com/guofei9987) , importantly , the DCT algorithm needs **the carrier image size  should  16 times greater than watermark**, or it doesn't work.

## Requirements

These scripts need python 3.6+ and the following libraries:

```python
numpy==1.19.5
opencv-python==4.5.1.48
PyWavelets==1.1.1
```

You can easy to install these libraries by :

```python
pip install -r requirements.txt
```

## Running

First of all, you need satisfy the environment requirements, then run

```python
python main.py --ori_filename <carrier image path> --wm_filename <watermark path>
```

you can get a image include watermark, the default path under***./img/***.

### Encode

Above-mentioned is the most convenient way encode, but formally,  you need to run this

```python
python main.py --ori_filename <carrier image path> --wm_filename <watermark path> --coder encoder
```

For example

```python
python main.py --ori_filename ./img/carrier.png  --wm_filename ./img/watermark.png --coder encoder
```

In addition, you can use ```-wm_method```  to choose DCT algorithm (default) or LSB algorithm to encode the watermark, you can just run like this

```python
python main.py --ori_filename ./img/carrier.png  --wm_filename ./img/watermark.png --coder encoder --wm_method LSB
```

Furthermore,it also support the usual attack method to destroy image,you need to run this

```python
python main.py --ori_filename ./img/carrier.png  --wm_filename ./img/watermark.png --coder encoder --att_method saltnoise
```

The all attack methods you can look up in **./src/attack.py**, and the watermarked image will be saved under the path ***./img/**.

### Decode

Above all, you need to confirm the watermarked image is encoded by which algorithm, then you can run like this

```python
python main.py --wm_filename ./img/watermark.png --ori_wm_filename ./img/ori_wm.png --coder decoder 
```

 As you see, the all  algorithms  needs the watermark image to decode, because the watermark size we don't know.

