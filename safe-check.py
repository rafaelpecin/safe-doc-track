import argparse
import os
import cv2
import piexif
from PIL import Image

def extract_metadata(image_path):
    results = {}
    if image_path.lower().endswith('.png'):
        try:
            with Image.open(image_path) as img:
                for key, value in img.info.items():
                    if key in ['Author', 'Description']:
                        results[f"EXIF metadata ({key})"] = value
        except Exception: pass
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        try:
            exif_dict = piexif.load(image_path)
            artist = exif_dict["0th"].get(piexif.ImageIFD.Artist, b"").decode('utf-8', errors='ignore').strip('\x00')
            desc = exif_dict["0th"].get(piexif.ImageIFD.ImageDescription, b"").decode('utf-8', errors='ignore').strip('\x00')
            if artist: results["EXIF Artist"] = artist
            if desc: results["EXIF Description"] = desc
        except Exception: pass
    return results


def generate_visual_check_image(input_path, output_path):
    """Adaptative threshold to reveal the watermark."""
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False
    # Adaptative Threshold highlights low opacity texts
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite(output_path, thresh)
    return True

def process_checking(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
    

    for file_name in files:
        input_path = os.path.join(input_dir, file_name)
        name_part, ext_part = os.path.splitext(file_name)
        output_path = os.path.join(output_dir, f"{name_part}_check{ext_part}")
        
        print(f"\n[File]: {file_name}")
        
        meta_data = extract_metadata(input_path)
        for key, val in meta_data.items():
            print(f"  ├── {key}: '{val}'")
            
            
        if generate_visual_check_image(input_path, output_path):
            print(f"  └── [Visual]: Adaptative border map generated on -> {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    process_checking(args.input, args.output)

