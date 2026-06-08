#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_site_logo(width, height, output_path):
    # Create a wide logo with icon + text
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Icon circle size
    icon_size = int(height * 0.85)
    icon_x = 10
    icon_y = (height - icon_size) // 2
    
    # Draw gradient circle
    center_x = icon_x + icon_size // 2
    center_y = icon_y + icon_size // 2
    radius = icon_size // 2 - 1
    
    for i in range(radius, 0, -1):
        ratio = i / radius
        r = int(99 + (139 - 99) * ratio)
        g = int(102 + (92 - 102) * ratio)
        b = int(241 + (246 - 241) * ratio)
        
        draw.ellipse([center_x-i, center_y-i, center_x+i, center_y+i], fill=(r, g, b, 255))
    
    # Draw letter D
    try:
        font_size = int(icon_size * 0.55)
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "D"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = center_x - text_width // 2
    y = center_y - text_height // 2 - bbox[1]
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Draw text "Dovi" next to icon
    try:
        text_font_size = int(height * 0.5)
        text_font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", text_font_size)
    except:
        text_font = ImageFont.load_default()
    
    text_x = icon_x + icon_size + 15
    text_y = height // 2
    
    draw.text((text_x, text_y), "Dovi", fill=(55, 65, 81, 255), font=text_font, anchor="lm")
    
    img.save(output_path, 'PNG')
    return output_path

if __name__ == "__main__":
    output_dir = os.path.expanduser("~/dovi-blog/static")
    
    # Create site logo (header logo)
    create_site_logo(200, 50, os.path.join(output_dir, "logo.png"))
    print("✓ logo.png (200x50)")
    
    # Create larger logo for about page
    create_site_logo(400, 100, os.path.join(output_dir, "logo-large.png"))
    print("✓ logo-large.png (400x100)")
    
    print("\n✅ Site logos created!")
