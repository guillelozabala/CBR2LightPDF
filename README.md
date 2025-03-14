# CBR/CBZ to PDF converter

Simple Python script to convert `.cbr` and `.cbz` files into a compressed `.pdf`.

## Fearures

There are already some converters out there. This one allows for:

- Resizing of images for smaller `.pdf`s
- Adjustable `.jpeg` quality
- Grayscale conversion for better compression (optional)
- No external dependencies (just Python)

Twisting the parameters should allow you to convert large comics without crashing your laptop, and to obtain reasonably large `.pdf`s.

It should also be able to handle `.png`s

## Usage 

You can run in your terminal

``` sh
python cbr2pdf.py your_comic.cbr output.pdf --max.width 1600 --max-height 1600 --quality 85 --greyscale
``` 

Of course you need some dependencies. Make sure you can import the following packages:

- patoolib
- tempfile
- fitz  
- PyMuPDF
- PIL (pillow)
- argparse
- shutil