import os
import argparse
from pdf2image import convert_from_path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# USAGE:
# python app.py -input_pdf /path/to/file.pdf -image_output_folder /path/to/destimagedir -markdown_output_folder /path/to/filedestdir --quality 60 --viewsize 350

# Set default directories (Overwritten if debug enabled)
# Note Initial directories below are only used for tkinter UI
try:
    from local_config import VAULT_INITDIR, PDF_INITDIR
except ImportError:
    print("Warning: No config.py file found. Using defaults.")
    VAULT_INITDIR = os.getcwd()
    PDF_INITDIR = os.getcwd()

def select_folder(root, title="Select Folder", initialdir=VAULT_INITDIR):
    """Opens a folder selection dialog and returns the selected folder."""
    messagebox.showinfo("Next Step", f"{title}")
    return filedialog.askdirectory(parent=root, initialdir=initialdir)

def select_pdf_file(root, initialdir=PDF_INITDIR):
    """Opens a file selection dialog for PDFs and returns the selected file path."""
    return filedialog.askopenfilename(parent=root, title="Select PDF file", initialdir=initialdir, 
                                      filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])

def get_image_quality():
    """Prompts the user to enter an image quality level (1-100)."""
    while True:
        try:
            return int(input("Enter the image quality (1-100, where 100 is best): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")

def get_image_viewsize():
    """Prompts the user to enter an optional image view size for Markdown (e.g., ![[image.png | VIEW_SIZE]])."""
    while True:
        image_viewsize = input("Enter the markdown viewing size (leave blank for normal): ")
        if image_viewsize == "":
            return None
        try:
            return int(image_viewsize)
        except ValueError:
            print("Invalid input. Please enter a number or leave blank for normal.")

def convert_pdf_to_images(pdf_path, image_output_folder, pdf_base_name, image_quality):
    """Converts PDF pages to images and saves them as JPEGs with specified quality."""
    images = convert_from_path(pdf_path)
    total_size = 0
    
    if not os.path.exists(image_output_folder):
        os.makedirs(image_output_folder)
    
    for i, image in enumerate(images):
        image_filename = f'{pdf_base_name}_page_{i + 1}.jpg'
        image_path = os.path.join(image_output_folder, image_filename)
        image.save(image_path, 'JPEG', quality=image_quality)
        total_size += os.path.getsize(image_path)
    
    return images, total_size

def write_markdown_file(markdown_file_path, images, pdf_base_name, image_output_folder, image_viewsize):
    """Creates a Markdown file with references to the saved images."""
    with open(markdown_file_path, 'w') as md_file:
        for i in range(len(images)):
            image_filename = f'{pdf_base_name}_page_{i + 1}.jpg'
            if image_viewsize:
                md_file.write(f"![[{image_filename} | {image_viewsize}]]\n\n")
            else:
                md_file.write(f"![[{image_filename}]]\n\n")

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert a PDF to images and generate a Markdown file with references.")
    parser.add_argument("-i", "--input_pdf", type=str, help="Path to the input PDF file.")
    parser.add_argument("-d", "--image_output_folder", type=str, help="Destination folder for images.")
    parser.add_argument("-o", "--markdown_output_folder", type=str, help="Destination folder for Markdown file.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("--quality", type=int, default=70, help="jpeg Image Compression Quality Factor [0-100] 100 is best quality. Good balance of size vs quality is 70.")
    parser.add_argument("--viewsize", type=int, default=None, help="Viewing Size for Obsidian markdown syntax i.e. ![[image.png | VIEW_SIZE]]")

    return parser.parse_args()

def main():
    """Main function to handle user input, PDF conversion, and Markdown generation."""
    args = parse_args()

    # Enable debug mode if specified
    global DEBUG
    if args.debug:
        DEBUG = True
        print("DEBUG MODE ENABLED")
        VAULT_INITDIR = "/Users/s/11_code/00_scripting-inbox/obsidian-import-pdf-as-images/sandbox"
        PDF_INITDIR = os.getcwd()

    # ✅ Create and manage a **single** Tk instance for dialogs
    root = None
    if not args.input_pdf or not args.image_output_folder or not args.markdown_output_folder:
        root = tk.Tk()
        root.withdraw()  # Hide the main window, keep dialogs functional

    # Select the PDF file (either from CLI or interactive)
    pdf_path = args.input_pdf if args.input_pdf else select_pdf_file(root)
    if not pdf_path:
        print("No file selected. Exiting...")
        return

    # Select Image Output Folder (either from CLI or interactive)
    image_output_folder = args.image_output_folder if args.image_output_folder else select_folder(root, title="Select Image Folder")
    if not image_output_folder:
        print("No folder selected. Exiting...")
        return

    # Select Markdown File Output Folder (either from CLI or interactive)
    markdown_output_folder = args.markdown_output_folder if args.markdown_output_folder else select_folder(root, title="Select Markdown Output Folder")
    if not markdown_output_folder:
        print("No folder selected. Exiting...")
        return

    # Process the PDF
    pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    markdown_file_path = os.path.join(markdown_output_folder, f"{pdf_base_name}.md")

    # Get optional user inputs
    if all(v is None for v in [args.input_pdf]):
        print("No arguments provided. Switching to interactive mode...")
        image_quality = get_image_quality()
        image_viewsize = get_image_viewsize()
    else:
        image_quality = args.quality
        image_viewsize = args.viewsize

    # Convert PDF pages to images
    images, total_size = convert_pdf_to_images(pdf_path, image_output_folder, pdf_base_name, image_quality)

    # Generate Markdown file
    write_markdown_file(markdown_file_path, images, pdf_base_name, image_output_folder, image_viewsize)

    # Print summary
    print(f"PDF pages have been converted and saved as images in '{image_output_folder}'.")
    print(f"Markdown file with image references created at '{markdown_file_path}'.")
    print(f"Image quality factor = {image_quality}.")
    if image_viewsize: print(f"Image viewsize changed to {image_viewsize}.")
    print(f"Total size of images: {total_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
