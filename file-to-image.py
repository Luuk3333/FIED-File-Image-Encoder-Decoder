from PIL import Image
import os

# Convert any file to an image
# Store each byte as a pixel with a color from 0 (black) to 255 (white)

file = "myfile.txt"

# Get amount of bytes
filesize = os.path.getsize(file)
print("File size: " + str(filesize) + " bytes")

decimals = [] # Create empty list will hold decimal values of bytes later on

# open file (https://stackoverflow.com/a/1035360)
print("Opening file: " + file + "..")
with open(file, "rb") as f:
    byte = f.read(1)
    print("Converting bytes to colors..")
    while byte:
        # Do stuff with byte.
        byte = f.read(1)
        #print(byte)

        # Convert byte to image
        decimal = int.from_bytes(byte, byteorder='little')  
        #print(decimal)

        # Add decimal value to list
        decimals.append(decimal)

# Create new image
print("Generating image..")
resolution = (filesize, 1) # Set width of image to file size (amount of bytes)
im = Image.new('L', resolution) # Create a grayscale image
im.putdata(decimals) # Set pixel colors (https://stackoverflow.com/a/2111223)
print("Saving image..")
im.save(file + "output.png")
print("Finished!")
