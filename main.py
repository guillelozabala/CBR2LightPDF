
"""
Convert .cbr or .cbz to .pdf
Usage: python main.py input_file output_file [--max-width MAX_WIDTH] [--max-height MAX_HEIGHT] [--quality QUALITY] [--grayscale]
Guillermo Martínez - 03/2025

"""

import os
import patoolib
import tempfile
import fitz  # PyMuPDF is required
from PIL import Image
import argparse
import shutil

def extract_images_from_archive(archive_path, temp_dir):
    """Extracts images from a .cbz or .cbr file to a temporary directory using patool"""
    try:
        patoolib.extract_archive(archive_path, outdir=temp_dir)
    except Exception as e:
        raise RuntimeError(f"Extraction failed: {e}")

    images = sorted(
        [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    )
    return images

def create_pdf(images, output_pdf, max_size, quality, grayscale):
    """Converts extracted images to a compressed PDF file"""
    if not images:
        raise ValueError("No images found to create PDF.")
    
    # Create a new PDF document
    pdf_document = fitz.open()
    
    for img_path in images:
        img = Image.open(img_path)
        if grayscale:
            # Convert to grayscale
            img = img.convert("L")
        else:
            # Ensure correct format
            img = img.convert("RGB")

        # Resize the image
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Save the compressed image in a temporary location
        temp_img_path = img_path + "_compressed.jpg"
        # Lower quality reduces size
        img.save(temp_img_path, "JPEG", quality=quality) 
        
        # Blank PDF page with the same dimensions as the resized image
        img_width, img_height = img.size
        page = pdf_document.new_page(width=img_width, height=img_height)
        
        # Insert the compressed image into the page
        page.insert_image(page.rect, filename=temp_img_path)

    # Save the final PDF
    pdf_document.save(output_pdf)
    pdf_document.close()

def convert_cbr_cbz_to_pdf(input_file, output_file, max_size, quality, grayscale):
    """Main function that handles conversion"""
    temp_dir = tempfile.mkdtemp()
    
    try:
        images = extract_images_from_archive(input_file, temp_dir)
        create_pdf(images, output_file, max_size, quality, grayscale)
    finally:
        # Cleanup temporary files
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .cbr or .cbz to a compressed .pdf")
    parser.add_argument("input", help="Path to .cbr or .cbz file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--max-width", type=int, default=1600, help="Max width of images in PDF (default: 1600px)")
    parser.add_argument("--max-height", type=int, default=1600, help="Max height of images in PDF (default: 1600px)")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality (default: 85)")
    parser.add_argument("--grayscale", action="store_true", help="Convert images to grayscale to reduce size")

    args = parser.parse_args()
    max_size = (args.max_width, args.max_height)
    
    convert_cbr_cbz_to_pdf(args.input, args.output, max_size, args.quality, args.grayscale)
