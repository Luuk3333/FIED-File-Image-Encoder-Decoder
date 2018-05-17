from PIL import Image
import array
import argparse

# Set command-line options
parser = argparse.ArgumentParser()
parser.add_argument('-F', '--file', help='Select file to decode.', dest="file")
parser.add_argument('-V', '--verbose', help='Turn verbose mode on/off. Note: Performance may be degraded if this option is used.', dest="verbose", action="store_true", default=False)
args = parser.parse_args()

file = args.file
verbose = args.verbose

# Open image
print("Opening image..")
image = Image.open(file)

# Remove '._penc_.png' to get original filename
original_filename = file.split('._penc_.png')[0]

# Get decimal pixel values and convert it to a bytearray
print("Converting pixels to bytes..")
pixels = bytes(image.getdata())

if verbose: print(pixels) # Show bytes if verbose is set to true

# Save file
print("Saving file..")
open(original_filename, 'wb').write(pixels)

print("Finished!")
