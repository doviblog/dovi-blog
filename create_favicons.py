#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon(size, output_path):
    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient circle
    center = size // 2
    radius = size // 2 - 2
    
    for i in range(radius, 0, -1):
        # Gradient from #6366f1 to #8b5cf6
        ratio = i / radius
        r = int(99 + (139 - 99) * ratio)
        g = int(102 + (92 - 102) * ratio)
        b = int(241 + (246 - 241) * ratio)
        
        x1 = center - i
        y1 = center - i
        x2 = center + i
        y2 = center + i
        
        draw.ellipse([x1, y1, x2, y2], fill=(r, g, b, 255))
    
    # Draw letter D
    try:
        # Try to use a nice font
        font_size = int(size * 0.55)
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw D centered
    text = "D"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - bbox[1]  # Adjust for baseline
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    img.save(output_path, 'PNG')
    return output_path

def create_ico(sizes, output_path):
    images = []
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        radius = size // 2 - 1
        
        # Gradient circle
        for i in range(radius, 0, -1):
            ratio = i / radius
            r = int(99 + (139 - 99) * ratio)
            g = int(102 + (92 - 102) * ratio)
            b = int(241 + (246 - 241) * ratio)
            
            draw.ellipse([center-i, center-i, center+i, center+i], fill=(r, g, b, 255))
        
        # Draw D
        try:
            font_size = int(size * 0.55)
            font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "D"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - bbox[1]
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        images.append(img)
    
    # Save as ICO
    images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
    return output_path

if __name__ == "__main__":
    output_dir = os.path.expanduser("~/dovi-blog/static")
    
    # Create favicon.ico (16, 32, 48)
    create_ico([16, 32, 48], os.path.join(output_dir, "favicon.ico"))
    print("✓ favicon.ico")
    
    # Create PNG favicons
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
    }
    
    for filename, size in sizes.items():
        create_favicon(size, os.path.join(output_dir, filename))
        print(f"✓ {filename}")
    
    print("\n✅ All favicons created!")
