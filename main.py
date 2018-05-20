from os.path import exists
from PIL import Image
from tqdm import tqdm
import argparse
import array
import os
import math
import re

# Set command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--encode', help='Select file to encode.', dest="file_encode")
parser.add_argument('--decode', help='Select file to decode.', dest="file_decode")
parser.add_argument('--verbose', help='Turn verbose mode on/off. Note: Performance may be degraded if this option is used.', dest="verbose", action="store_true", default=False)
parser.add_argument('--overwrite', help='Danger! Overwrite file without any warning!', dest="overwrite", action="store_true", default=False)
parser.add_argument('--output', help='Set output filename when decoding a file.', dest="file_output")
parser.add_argument('--disable-parts', help='Forces generated image not being split up in parts.', dest="disable_parts", action="store_true", default=False)
parser.add_argument('--max-part-size', help='Max file size of parts in bytes. The generated image will be split up in parts if it is larger. Default is 128000000 bytes.', dest="max_part_size", default=128000000)
args = parser.parse_args()

file_encode = args.file_encode
file_decode = args.file_decode
verbose = args.verbose
overwrite = args.overwrite
output = args.file_output
max_part_size = int(args.max_part_size)
disable_parts = args.disable_parts

# Disable PIL.Image.DecompressionBombError
Image.MAX_IMAGE_PIXELS = None

def encode(file):
    if (output != None):
        print("NOTICE: '-O, --output' only works when decoding a file. It will be ignored for now.")

    # Get amount of bytes
    filesize = os.path.getsize(file)

    # open file (https://stackoverflow.com/a/1035360)
    print("Opening file: " + file + "..")
    print("File size: " + str(filesize) + " bytes (" + str(filesize/1000) + " kB / " + str(filesize/1000000) + " MB / " + str(filesize/1000000000) + " GB)")

    f = open(file,'rb')
    tmp_bytes = f.read(max_part_size)
    count = 1
    number_of_parts = math.ceil(filesize / max_part_size)

    if (number_of_parts > 1):
        print("Splitting file up in " + str(math.ceil(filesize / max_part_size)) + " parts of max " + str(max_part_size)+" bytes (" + str(max_part_size/1000) + " kB / " + str(max_part_size/1000000) + " MB)")

    if verbose: print("Max part size is " + str(max_part_size) + " bytes (" + str(max_part_size/1000) + " kB / " + str(max_part_size/1000000) + " MB)")

    while tmp_bytes:
        if (number_of_parts == 1): # If file is under the max size limit (there's no need to split the file up in multiple parts)
            if verbose: print("Not going to split up generated file in parts because the file size is lower than the max part size.")
            print("Generating image..")
        elif (disable_parts): # If user disabled splitting file up in parts
            if verbose: print("Not going to split up generated file in parts (--disable-parts option used).")
            print("Generating image..")
        else:
            print("Generating image " + str(count) + "/" + str(number_of_parts) + "..")

        decimals = [] # Create empty list will hold decimal values of bytes

        print("    Converting bytes to colors.. (this may take some time)")
        # Add decimal value to list
        if (verbose): 
            for byte in tqdm(tmp_bytes): 
                decimals.append(byte)
        else:
            for byte in tmp_bytes: 
                decimals.append(byte)

        # Create image
        resolution = (len(tmp_bytes), 1) # Set width of image to file size (amount of bytes)
        im = Image.new('L', resolution) # Create a grayscale image
        im.putdata(decimals) # Set pixel colors (https://stackoverflow.com/a/2111223)
        if (number_of_parts == 1 or disable_parts):
            file_output = file + "._fied_.png"
        else:
            file_output = file + "._fied_" + str(count) + "-" + str(number_of_parts) + ".png"
        print("    Saving image as \"" + file_output + "\"..")
        im.save(file_output)

        tmp_bytes = f.read(max_part_size)
        count += 1

    print("Finished!\n")

# Check if file already exists
def decode_overwrite(filename, number_of_parts):
    if (exists(filename)):
        if (overwrite): # If command-line option was used
            print("'-O, --overwrite' option was used, overwriting file..")
        else:
            if (number_of_parts == 1):
                # Ask user to overwrite file
                print("File \"" + filename + "\" already exists! Do you want to overwrite it? yes/no")
                while True:
                    text = input("> ")
                    if (text == "yes"):
                        break
                    if (text == "no"):
                        print("Not going to overwrite file. Exiting..\n")
                        exit()
                    else:
                        print("File already exists! Do you want to overwrite it? yes/no")
            else:
                print("File \"" + filename + "\" already exists! Exiting..\n")
                exit()

def decode(file):
    match_single = re.match(r'(.+)\._fied_\.png', file, re.M|re.I) # match single file
    match_parts = re.match(r'(.+)\._fied_(\d+)-(\d+)\.png', file, re.M|re.I) # match multiple part file

    # Check if command-line option was used
    if (output != None and output != ""):
        original_filename = output

    elif match_single:
        original_filename = match_single.group(1)
        print("Original filename: " + original_filename)

        # Open image
        print("Opening image..")
        im = Image.open(file)
        
        # Get decimal pixel values and convert it to a bytearray
        print("    Converting pixels to bytes..")
        pixels = bytes(im.getdata())
        
        # Save file
        print("    Saving file as '" + original_filename + "'..")
        decode_overwrite(original_filename, 1)
        open(original_filename, 'wb').write(pixels)

        print("Finished!\n")

    elif match_parts:
        original_filename = match_parts.group(1)
        number_of_parts = int(match_parts.group(3))
        print("Detected multi-part file. " + str(number_of_parts) + " parts found.")

        decode_overwrite(original_filename, number_of_parts)

        for part in range(1, number_of_parts + 1):
            # Open image
            file_part = original_filename + "._fied_" + str(part) + "-" + str(number_of_parts) + ".png"
            print("Opening image '" + file_part + "'..")

            im = Image.open(file_part)

            # Get decimal pixel values and convert it to a bytearray
            print("    Converting pixels to bytes..")
            pixels = bytes(im.getdata())

            print("    Saving file as '" + original_filename + "'..")
            open(original_filename, 'ab').write(pixels) # Append bytes to file


        print("Finished!\n")

    else:
        print("ERROR: Could not decode the png image because the format is incorrect.\n")


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
