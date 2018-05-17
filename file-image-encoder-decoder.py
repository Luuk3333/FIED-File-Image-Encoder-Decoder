from os.path import exists
from PIL import Image
from tqdm import tqdm
import argparse
import array
import os

# Set command-line options
parser = argparse.ArgumentParser()
parser.add_argument('-ENC', '--encode', help='Select file to encode.', dest="file_encode")
parser.add_argument('-DEC', '--decode', help='Select file to decode.', dest="file_decode")
parser.add_argument('-V', '--verbose', help='Turn verbose mode on/off. Note: Performance may be degraded if this option is used.', dest="verbose", action="store_true", default=False)
parser.add_argument('--overwrite', help='Danger! Overwrite file without any warning!', dest="overwrite", action="store_true", default=False)
parser.add_argument('-O', '--output', help='Set output filename when decoding a file.', dest="file_output")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

file_encode = args.file_encode
file_decode = args.file_decode
verbose = args.verbose
overwrite = args.overwrite
output = args.file_output


def encode(file):
	if (output != None):
		print("NOTICE: '-O, --output' only works when decoding a file. It will be ignored for now.")

	# Get amount of bytes
	filesize = os.path.getsize(file)

	decimals = [] # Create empty list will hold decimal values of bytes later on

	# open file (https://stackoverflow.com/a/1035360)
	print("Opening file: " + file + "..")
	print("File size: " + str(filesize) + " bytes")
	with open(file, "rb") as f:
	    print("Converting bytes to colors.. (this may take some time)")
	    
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

def decode(file):
	# Open image
	print("Opening image..")
	image = Image.open(file)

	# Check if command-line option was used
	if (output != None and output != ""):
	    original_filename = output
	else:
	    # Remove '._penc_.png' to get original filename
	    original_filename = file.split('._penc_.png')[0]

	# Get decimal pixel values and convert it to a bytearray
	print("Converting pixels to bytes..")
	pixels = bytes(image.getdata())

	if verbose: print(pixels) # Show bytes if verbose is set to true

	# Save file
	print("Saving file as '" + original_filename + "'..")
	# Check if file already exists
	if (exists(original_filename)):
	    if (overwrite): # If command-line option was used
	        print("'-O, --overwrite' option was used, overwriting file..")
	    else:
	        # Ask user to overwrite file
	        print("File already exists! Do you want to overwrite it? yes/no")
	        while True:
	            text = input("> ")
	            if (text == "yes"):
	                break
	            if (text == "no"):
	                print("Not going to overwrite file. Exiting..")
	                exit()
	            else:
	                print("File already exists! Do you want to overwrite it? yes/no")

	open(original_filename, 'wb').write(pixels)
	print("Finished!")


# Check which command-line options are set
if (file_encode != None and file_decode == None):
	# Encode
	encode(file_encode)
elif (file_encode == None and file_decode != None):
	# Decode
	decode(file_decode)
elif (file_encode != None and file_decode != None):
	print("Both files to encode and decode selected. Please use one function at a time.")
elif (file_encode == None and file_decode == None):
	print("No file to encode or decode selected! Check --help for more info.")
