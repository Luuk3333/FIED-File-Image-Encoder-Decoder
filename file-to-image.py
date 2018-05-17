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
    byte = f.read(1)
    print("Converting bytes to colors..")
    if verbose: pbar = tqdm(total=filesize) # If verbose set to true, show progress bar
    while byte:
        # Do stuff with byte.
        byte = f.read(1)
        #print(byte)

        # Convert byte to image
        decimal = int.from_bytes(byte, byteorder='little')  
        #print(decimal)

        # Add decimal value to list
        decimals.append(decimal)
        if verbose: pbar.update(1)
    if verbose: pbar.close()

# Create new image
print("Generating image..")
resolution = (filesize, 1) # Set width of image to file size (amount of bytes)
im = Image.new('L', resolution) # Create a grayscale image
im.putdata(decimals) # Set pixel colors (https://stackoverflow.com/a/2111223)
file_output = file + "._penc_.png" # Pixel ENCoder
print("Saving image as \"" + file_output + "\"..")
im.save(file_output)
print("Finished!")
