from preproces import *
from graph import ImageVisualizer
import ast
import csv

def csv_reader(csv_path):
    file = open(csv_path, newline='')
    reader = csv.reader(file, delimiter= ";")
    header = next(reader)
    data = []
    for row in reader:
        file_name = str(row [1])
        x_s = row[3]
        x_y = row[4]
        data.append([file_name, x_s, x_y])
    return data

def create_matrixs(dataset):
    matrix = []
    with open(dataset, "r") as dataFile:
        for line in dataFile:
            row = ast.literal_eval(line.strip())
            matrix.append(row)
    return matrix

def compare_datasets(referenceFile, datasetFile, start_y, start_x):
    same = 0
    ref_rows = len(referenceFile)
    ref_cols = len(referenceFile[0]) if ref_rows > 0 else 0
    full = ref_cols * ref_rows

    for y in range(ref_rows):
        for x in range(ref_cols):
            dataset_y = y + start_y
            dataset_x = x + start_x
            if dataset_y < len(datasetFile) and dataset_x < len(datasetFile[0]):
                if referenceFile[y][x] == datasetFile[dataset_y][dataset_x]:
                    same += 1
    return same, full

def iterate_data(csv_path):
    reference_file = create_matrixs("reference.txt")
    csv_data = csv_reader(csv_path)

    for file_name, x_s, x_y in csv_data:
        image_path = f"../data/basic/dataset/{file_name}"
        dataset_file = converter(image_path)
        dataset_x, dataset_y, percent = find_best_offset_combination(dataset_file, reference_file, image_path)
        print(f"{file_name}: match {percent}% y: {dataset_y} x: {dataset_x}")

def calculate_percent_match(same, full):
    percent = same * 100 / full
    return(percent)

# build a list of x nad y values from sorted_positions
# try every combination of y, x
def find_best_offset_combination(data, reference, image_path, target=1, min_percent=99):
    sorted_positions = find_sorted_positions(data, target)
    visualizer = ImageVisualizer(image_path)
    x_values = sorted(set(x for _, x in sorted_positions))
    y_values = sorted(set(y for y, _ in sorted_positions))

    best_percent = 0
    best_pos = (None, None)

    # Track fallback in case min_percent is not reached
    fallback_percent = 0
    fallback_pos = (None, None)

    for y in y_values:
        for x in x_values:
            same, full = compare_datasets(reference, data, y, x)
            percent = calculate_percent_match(same, full)
            visualizer.update_rectangle(x, y)
            if percent > fallback_percent:
                fallback_percent = percent
                fallback_pos = (y, x)

            if percent >= min_percent and percent > best_percent:
                best_percent = percent
                best_pos = (y, x)
                break

    
   
    if best_pos == (None, None):
        visualizer.highlight_final(fallback_pos[1], fallback_pos[0])
        visualizer.close()
        return fallback_pos[0], fallback_pos[1], fallback_percent
    else:
        visualizer.highlight_final(best_pos[1], best_pos[0])
        visualizer.close()
        return best_pos[0], best_pos[1], best_percent

# # For each unique x column, it finds the lowest y row where data[y][x] == target aka 1.
# #it loops through columns left to right
# #for each column, it finds the first match going down
# #saves only the lowest y for that x
# def find_unique_sorted_positions(data, target):

#     seen_x = set()
#     positions = []

#     for x in range(len(data[0])):  # scan left to right
#         column_positions = []
#         for y in range(len(data)):  # top to bottom
#             if data[y][x] == target and x not in seen_x:
#                 column_positions.append((y, x))
#         if column_positions:
#             lowest_y = min(column_positions, key=lambda pos: pos[0])
#             positions.append(lowest_y)
#             seen_x.add(x)

#     return positions

#finds all positions in data where the value equals "1" and sorts them by x first, then y.
#extract all possible x values from these positions to try in combinations later.
def find_sorted_positions(data, target):
    positions = []
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == target:
                positions.append((y, x))
    # Sort by x first, then y
    positions.sort(key=lambda pos: (pos[1], pos[0]))
    return positions

reference("../data/basic/dataset/emoji_0.jpg")
# referenceFile = create_matrixs("reference.txt")
# datasetFile = converter("../data/basic/dataset/emoji_29.jpg")
# dataset_y, dataset_x, data = find_lowest_y_and_x(datasetFile, 1)
# same, full = compare_datasets(referenceFile, datasetFile, dataset_y, dataset_x)
csv_path = "../data/basic/labels.csv"
iterate_data(csv_path)
# print(f"{same}")
# print(f"{full}")


