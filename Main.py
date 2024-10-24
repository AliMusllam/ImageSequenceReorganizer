from PIL import Image
import os
from tkinter import filedialog

def select_folder():
    # Folder path
    folder_path = filedialog.askdirectory()
    return folder_path

def slice_and_group_images(folder_path, file_name, grid_size, final_width):


    if folder_path:
        print("Slicing and grouping images in folder:", folder_path)


        # Collect only image files in the folder
        image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files: 
            print("No image files found in the folder.")
            return
        
        # Create a subfolder to save grouped images
        subfolder_path = os.path.join(folder_path, "output")
        os.makedirs(subfolder_path, exist_ok=True)
        
        # Slice and group each image
        grouped_images = [[] for _ in range(grid_size[0] * grid_size[1])]  # List to store slices for each group

        for image_file in image_files:
            # Open the image
            image = Image.open(image_file)

            # Resize the image to fit into the grid
            width, height = image.size
            slice_width = width // grid_size[0]
            slice_height = height // grid_size[1]
            image = image.resize((slice_width * grid_size[0], slice_height * grid_size[1]))

            # Slice the image into the grid
            slices = []
            for i in range(grid_size[1]):
                for j in range(grid_size[0]):
                    # Define the bounding box for the slice
                    left = j * slice_width
                    upper = i * slice_height
                    right = left + slice_width
                    lower = upper + slice_height

                    # Crop the slice from the original image
                    slice_image = image.crop((left, upper, right, lower))
                    slices.append(slice_image)

            # Add slices to their corresponding group
            for i, slice_image in enumerate(slices):
                grouped_images[i].append(slice_image)

        # Save each grouped image
        for i, slices in enumerate(grouped_images):
            num_rows = len(slices) // final_width if len(slices) % final_width == 0 else len(slices) // final_width + 1
            row_height = max(slice_img.height for slice_img in slices)
            final_height = num_rows * row_height

            final_image = Image.new('RGBA', (final_width * slice_width, final_height), (0, 0, 0, 0))  # RGBA mode with transparent background

            x_offset = 0
            y_offset = 0
            for slice_img in slices:
                final_image.paste(slice_img, (x_offset, y_offset))
                x_offset += slice_width
                if x_offset >= final_width * slice_width:
                    x_offset = 0
                    y_offset += slice_img.height

            # Save the grouped image in the subfolder
            final_image.save(os.path.join(subfolder_path, f"{file_name}_{i}.png"))

path = select_folder()

# CHANGE THESE VALUES


slice_and_group_images(path, "slice", (12, 4), 6) 
