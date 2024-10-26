from PIL import Image
import os
from tkinter import filedialog, Tk

def select_folder():
    """Opens a folder selection dialog and returns the selected folder path."""
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    folder_path = filedialog.askdirectory()
    return folder_path

def slice_and_group_images(folder_path, file_name, grid_size, final_width):
    """
    Slices images in the selected folder into a grid and groups them into final images of the specified width.

    Args:
        folder_path (str): The path of the folder containing images.
        file_name (str): The base file name for the output images.
        grid_size (tuple): A tuple (x, y) specifying the grid size to slice each image.
        final_width (int): The number of slices per row in the output images.
    """
    if folder_path:
        print("Slicing and grouping images in folder:", folder_path)

        # Collect image files in the folder
        image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files: 
            print("No image files found in the folder.")
            return
        
        # Create a subfolder to save grouped images
        subfolder_path = os.path.join(folder_path, "output")
        os.makedirs(subfolder_path, exist_ok=True)
        
        # Initialize a list to store slices for each group
        grouped_images = [[] for _ in range(grid_size[0] * grid_size[1])]

        # Slice and group each image
        for image_file in image_files:
            image = Image.open(image_file)
            width, height = image.size

            # Calculate slice width and height
            slice_width = width // grid_size[0]
            slice_height = height // grid_size[1]

            # Resize image to match the exact grid
            image = image.resize((slice_width * grid_size[0], slice_height * grid_size[1]))

            # Slice the image into grid
            slices = []
            for i in range(grid_size[1]):
                for j in range(grid_size[0]):
                    left = j * slice_width
                    upper = i * slice_height
                    right = left + slice_width
                    lower = upper + slice_height
                    slice_image = image.crop((left, upper, right, lower))
                    slices.append(slice_image)

            # Group the slices
            for i, slice_image in enumerate(slices):
                grouped_images[i].append(slice_image)

        # Save each grouped image
        for i, slices in enumerate(grouped_images):
            num_rows = len(slices) // final_width + (1 if len(slices) % final_width != 0 else 0)
            row_height = max(slice_img.height for slice_img in slices)
            final_height = num_rows * row_height

            # Create a blank canvas for the final image
            final_image = Image.new('RGBA', (final_width * slice_width, final_height), (0, 0, 0, 0))

            # Paste slices into the final image
            x_offset = 0
            y_offset = 0
            for slice_img in slices:
                final_image.paste(slice_img, (x_offset, y_offset))
                x_offset += slice_width
                if x_offset >= final_width * slice_width:
                    x_offset = 0
                    y_offset += row_height

            # Save the final grouped image
            final_image.save(os.path.join(subfolder_path, f"{file_name}_{i}.png"))

if __name__ == "__main__":
    # Ask the user to select a folder
    folder_path = select_folder()

    # User-defined settings
    slice_and_group_images(folder_path, "Cloud", (5, 3), 1)
//