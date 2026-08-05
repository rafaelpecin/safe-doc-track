# safe-doc-track
Track who leaked your documents. Add discreet watermarks and hidden data to your documents that will allow you to identify who leaked your data.
The [safe-doc.py](safe-doc.py) script creates a copy of the original image with a semi-tranparent layer with an user defined message in black font over a white box on the right botton corner of the original image. In addition to this, EXIT information are set with the message, so it's easy to check using standard image software. The original image keeps unchanged.
The output directory will be created if it doesn't exist.

*Only JPG, BMP and PNG formats are supported - no support for PDF (yet).*

# Installation
Install dependencies:
```
python -m venv .sdt
source .sdt/bin/activate
python -m pip install pillow piexif
```

# Adding secure message to your documents
It will create new images with EXIF
`safe-doc.py -i INPUT_FOLDER -o OUTPUT_FOLDER -m MESSAGE`

## Example:
```
$ python safe-doc.py -i original/ -o track -m "This is for Safe Doc Track test only"
[+] Success: Lenna.png

```

# Checking for the secure message
You can run the `safe-check.py` script to extract the EXIF information (which should display your tracking message) and to generate a version of the image easier to read.
`safe-check.py -i TRACKED_IMAGE_FOLDER -o OUTPUT_FOLDER -m MESSAGE`

## Example
```
$ python safe-check.py -i track/ -o check

[File]: Lenna.png
  ├── EXIF metadata (Author): 'This is for Safe Doc Track test only'
  ├── EXIF metadata (Description): 'This is for Safe Doc Track test only'
  └── [Visual]: Adaptative border map generated on -> check\Lenna_check.png
```

[Processed images](Lenna.png)

