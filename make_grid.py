from PIL import Image
import os
import argparse

def split_image(image_path, rows=3, cols=4, line_width_percent=1, output_dir='split_images'):
    # Read the image
    img = Image.open(image_path)
    
    # Get image dimensions
    width, height = img.size
    
    # Calculate sub-image dimensions
    sub_width = width // cols
    sub_height = height // rows
    
    # Calculate line width
    line_width = int(width * line_width_percent / 100)
    
    # Calculate new dimensions for the grid image (including white lines)
    grid_width = (cols * sub_width) + (line_width * (cols - 1))
    grid_height = (rows * sub_height) + (line_width * (rows - 1))
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split image into sub-images
    for i in range(rows):
        for j in range(cols):
            # Calculate coordinates
            left = j * sub_width
            top = i * sub_height
            right = left + sub_width
            bottom = top + sub_height
            
            # Extract and save sub-image
            sub_image = img.crop((left, top, right, bottom))
            output_path = os.path.join(output_dir, f'sub_image_{i}_{j}.jpg')
            sub_image.save(output_path)
    
    # Create new image with white background and adjusted dimensions
    grid_img = Image.new('RGB', (grid_width, grid_height), 'white')
    
    # Paste sub-images with spacing
    for i in range(rows):
        for j in range(cols):
            # Calculate coordinates with line spacing
            left = j * (sub_width + line_width)
            top = i * (sub_height + line_width)
            
            # Extract original sub-image
            orig_left = j * sub_width
            orig_top = i * sub_height
            orig_right = orig_left + sub_width
            orig_bottom = orig_top + sub_height
            sub_image = img.crop((orig_left, orig_top, orig_right, orig_bottom))
            
            # Paste into new image
            grid_img.paste(sub_image, (left, top))
    
    # Save the grid image
    grid_output_path = os.path.join(output_dir, 'grid_image.jpg')
    grid_img.save(grid_output_path)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Split an image into a grid with white lines between sub-images')
    parser.add_argument('--image', type=str, default='Crab_Nebula.jpg',
                      help='Input image path (default: Crab_Nebula.jpg)')
    parser.add_argument('--rows', type=int, default=3,
                      help='Number of rows in the grid (default: 3)')
    parser.add_argument('--cols', type=int, default=4,
                      help='Number of columns in the grid (default: 4)')
    parser.add_argument('--line-width', type=float, default=1,
                      help='Width of white lines as percentage of image width (default: 1)')
    parser.add_argument('--output-dir', type=str, default='split_images',
                      help='Output directory for split images (default: split_images)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with parsed arguments
    split_image(args.image, args.rows, args.cols, args.line_width, args.output_dir)
