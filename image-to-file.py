from PIL import Image
import array

filename = 'myfile.txt._penc_.png'

# Open image
print("Opening image..")
image = Image.open(filename)

# Remove '._penc_.png' to get original filename
original_filename = filename.split('._penc_.png')[0]

# Get decimal pixel values and convert it to a bytearray
print("Converting pixels to bytes..")
pixels = bytes(image.getdata())

#print(pixels)

# Save file
print("Saving file..")
open("_decoded_" + original_filename, 'wb').write(pixels)

print("Finished!")
