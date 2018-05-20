# FIED-File-Image-Encoder-Decoder
Converts any file to/from a grayscale image.

### How it works
This Python script converts any file to a 1-pixel high grayscale png image. The width of the image will be the size of the original file in bytes. The bytes (2^8 = 256) from the original file are converted to pixels with a color from 0 (black) to 255 (white). When decoding, the color of every pixel is converted back to a byte which is written to a file.

### Installation
You'll need to install the following packages:
```
pip install pillow tqdm
```

### Usage
##### Encoding a file:
```
python main.py --encode myfile.zip
```
A png image will be created ending with `._fied_.png`. Opening this image with your avarage image editor will likely not work because of its odd resolution.

###### Multiple parts:
If a file is larger than 128 MB it will be split up in multiple parts. You can change the part file size with the option `--max-part-size 128000000` with the file size in bytes. Multiple part files end with (for example) `._fied_7-11_.png`, where 7 means the part number and 11 the total amount of parts.

It is also possible to disable the generation of multiple parts with the option `--disable-parts`. Note that when using this option a memory error is likely to occur with files larger than a few hundred megabytes.

##### Decoding a file:
```
python main.py --decode myfile.zip._fied_.png
```
Or a multiple part file (any part will work):
```
python main.py --decode myfile.zip._fied_7-11_.png
```
When decoding, `.\_penc\_.png` will be removed from the filename, so `myfile.zip` will be created.
If you don't want the original file to be overwritten (for example, while testing) you can set a custom name with the '\-\-output' option:
```
python main.py --decode myfile.zip._fied_.png --output alternative.txt
```

##### Verbose mode:
If you want to see more info you can turn on verbose mode with '\-\-verbose':
```
python main.py --encode myfile.zip --verbose
```
Performance may be degraded with verbose mode enabled.

### Notes
- This code is not optimized. It might perform not as great as you expect.
- Tested with Python 3, not with Python 2. It may not work with Python 2.

Feel free to report and contribute to any bugs, feature ideas and improvements!

### License
FIED-File-Image-Encoder-Decoder is licensed under the [GNU General Public License v3.0](https://github.com/Luuk3333/FIED-File-Image-Encoder-Decoder/blob/master/LICENSE).
