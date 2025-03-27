def apply_noise_mask_tiled(main_data, noise_data):
    cleaned = []

    noise_height = len(noise_data)
    noise_width = len(noise_data[0]) if noise_height > 0 else 0

    for y in range(len(main_data)):
        row = []
        for x in range(len(main_data[0])):
            main_val = main_data[y][x]

            # Get corresponding noise position (tiled)
            noise_y = y % noise_height
            noise_x = x % noise_width
            noise_val = noise_data[noise_y][noise_x]

            # Apply noise mask
            cleaned_val = 0 if noise_val == 1 else main_val
            row.append(cleaned_val)
        cleaned.append(row)

    return cleaned

main_data = load_list_of_lists_file("rgb_output.txt")
noise_data = image_to_binary_matrix("noise_pattern.jpg")  # or .png, etc.

cleaned = apply_noise_mask_tiled(main_data, noise_data)

# Save cleaned data
with open("denoised_output.txt", "w") as f:
    for row in cleaned:
        f.write(" ".join(str(v) for v in row) + "\n")

with open("extracted_noise_pattern.txt", "w") as f:
    for row in noise_data:
        f.write(" ".join(str(v) for v in row) + "\n")