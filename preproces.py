import base64
from PIL import Image
from io import BytesIO
from graph import *
import os


def converter(reference_path):
    #open and encode file to base64(decode into utf-8)
    with open(reference_path, "rb") as imageFile:
        encoded_str = base64.b64encode(imageFile.read()).decode("utf-8")

    #output encode to file
    with open("encoded_output.txt", "w") as outFile:
        outFile.write(encoded_str)

    #use PIL lib to convert base64 to RGB values 0-255 bcs .jpg is compressed format
    image_data = base64.b64decode(encoded_str)
    img = Image.open(BytesIO(image_data)).convert("RGB")

    width, height = img.size

    #open converted text file
    data = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y)) #get rgb values from every pixel
            rgb_conv = (r + g + b) / 3 # convert to grayscale
            value = 1 if rgb_conv < 200 else 0 #set range of distortion if is white set pixel to 0 if black set to 1
            row.append(value) #making list of lists
        data.append(row)

    with open("rgb_output.txt", "w") as rgb_file:
        for row in data:
            rgb_file.write(f"{row}\n")

    return data
                # rgb_file.write(f"{(rgb_conv)}") # write pixels to file keep image dimensions
                # if x == width - 1:
                #     rgb_file.write("\n")

def find_lowest_y_and_x(data, target):
    # visualizer = ImageVisualizer(image_path)
    lowest_y = None
    lowest_x = None

    #find the first row (lowest y)
    for y, row in enumerate(data):
        # visualizer.update_rectangle(x, y)
        if target in row:
            lowest_y = y
            break

    #find the first column (lowest x)
    for x in range(len(data[0])):
        for y in range(len(data)):
            if data[y][x] == target:
                lowest_x = x
                break
        if lowest_x is not None:
            break

    return lowest_y, lowest_x



#reference picture for later use to actualy search for pattern

def create_reference(lowest_y, lowest_x, data):
    reference_block = []

    for y in range(lowest_y, lowest_y + 50):
        row = []
        for x in range(lowest_x, lowest_x + 50):
            if (y < len(data) and x < len(data[0])):
                row.append(data[y][x])
        reference_block.append(row)
    with open("reference.txt", "w") as ref:
        for row in reference_block:
            ref.write(f"{row}\n")

def reference(path):

    data = converter(path)
    lowest_y, lowest_x = find_lowest_y_and_x(data, 1)
    #run create reference only if it didnt exists yet.
    if not(os.path.exists("reference.txt")):
        print(f"Creating reference at: ({lowest_x}, {lowest_y})")
        create_reference(lowest_y, lowest_x, data)
    else:
        print("file exists")
    
#check if pictures are same and on what percentage
#the preprocessing of picture can, and for sure is going to cause some deviations
#between reference and actual picture that we are going to compare



