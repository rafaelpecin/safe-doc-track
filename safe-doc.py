import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image, text):
    """Add black text over a white box, 20% tranparency."""
    # Transparent layer watermark
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)
    
    try:
        font_size = max(14, int(image.size[0] * 0.025))
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Text size calculation
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
        
    margin = 20
    padding = 6
    
    x = image.size[0] - text_width - margin
    y = image.size[1] - text_height - margin
    
    rect_x1 = x - padding
    rect_y1 = y - padding
    rect_x2 = x + text_width + padding
    rect_y2 = y + text_height + padding
    
    # 20% opacity: 255 * 0.20 = 51
    opacity = 51 
    
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=(255, 255, 255, opacity))
    draw.text((x, y), text, font=font, fill=(0, 0, 0, opacity))
    
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    combined = Image.alpha_composite(image, watermark_layer)
    return combined.convert("RGB")

def inject_metadata(image_path, fmt, message):
    """Set messagen to the image's metadata."""
    if fmt == 'JPEG':
        import piexif
        try:
            exif_dict = piexif.load(image_path)
        except Exception:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        exif_dict["0th"][piexif.ImageIFD.Artist] = message.encode('utf-8')
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = message.encode('utf-8')
        piexif.insert(piexif.dump(exif_dict), image_path)
    elif fmt == 'PNG':
        from PIL import PngImagePlugin
        img = Image.open(image_path)
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Author", message)
        meta.add_text("Description", message)
        img.save(image_path, "PNG", pnginfo=meta)

def process_images(input_dir, output_dir, message):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
    
    for file_name in files:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        img_format = 'PNG' if file_name.lower().endswith('.png') else 'JPEG'
        
        try:
            with Image.open(input_path) as img:
                final_img = add_watermark(img, message)
                final_img.save(output_path, format=img_format, quality=100)
                
            inject_metadata(output_path, img_format, message)
            print(f"[+] Success: {file_name}")
        except Exception as e:
            print(f"[-] Error: {file_name}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-m', '--message', required=True)
    args = parser.parse_args()
    process_images(args.input, args.output, args.message)

