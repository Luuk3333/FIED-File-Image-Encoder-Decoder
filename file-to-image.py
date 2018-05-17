from PIL import Image
import os
from tqdm import tqdm
import argparse

## Convert any file to an image by storing each byte as a pixel with a color from 0 (black) to 255 (white)

# Set command-line options
parser = argparse.ArgumentParser()
parser.add_argument('-F', '--file', help='Select file to encode.', dest="file")
parser.add_argument('-V', '--verbose', help='Turn verbose mode on/off. Note: Performance may be degraded if this option is used.', dest="verbose", action="store_true", default=False)
args = parser.parse_args()

file = args.file
verbose = args.verbose

# Get amount of bytes
filesize = os.path.getsize(file)
print("File size: " + str(filesize) + " bytes")

decimals = [] # Create empty list will hold decimal values of bytes later on

# open file (https://stackoverflow.com/a/1035360)
print("Opening file: " + file + "..")
with open(file, "rb") as f:
    print("Converting bytes to colors..")
    
    if (verbose): # If verbose set to true, show progress bar
        for byte in tqdm(f.read()):
            #print(byte)

            # Add decimal value to list
            decimals.append(byte)

    else:
        for byte in f.read():
            #print(byte)

            # Add decimal value to list
            decimals.append(byte)

# Create new image
print("Generating image..")
resolution = (filesize, 1) # Set width of image to file size (amount of bytes)
im = Image.new('L', resolution) # Create a grayscale image
im.putdata(decimals) # Set pixel colors (https://stackoverflow.com/a/2111223)
file_output = file + "._penc_.png" # Pixel ENCoder
print("Saving image as \"" + file_output + "\"..")
im.save(file_output)
print("Finished!")
