from PIL import Image
import os
from tqdm import tqdm

# Convert any file to an image
# Store each byte as a pixel with a color from 0 (black) to 255 (white)

file = "myfile.txt"
verbose = True # Note: Performance may be altered if this option is set to True

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
print("Saving image..")
im.save(file + "output.png")
print("Finished!")
