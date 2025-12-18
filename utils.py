#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: Maria Kevin
Created: 2025-12-19
Description: Utility functions for generating Thirukural wallpapers
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import json
import random

from PIL import Image, ImageDraw, ImageFont


def load_thirukural_data(json_path: str = "thirukural.json") -> list:
    """
    Load Thirukural data from JSON file.
    
    Args:
        json_path: Path to the thirukural.json file
        
    Returns:
        List of kural features
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['features']


def get_random_kural(kurals: list) -> dict:
    """
    Get a random Thirukural from the list.
    
    Args:
        kurals: List of kural features
        
    Returns:
        Random kural properties dictionary
    """
    random_kural = random.choice(kurals)
    return random_kural['properties']


def create_wallpaper_image(
    kural_data: dict,
    output_path: str,
    width: int = 1920,
    height: int = 1080
) -> str:
    """
    Create a beautiful wallpaper image with Thirukural text.
    
    Args:
        kural_data: Dictionary containing kural properties
        output_path: Path to save the generated image
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        Path to the generated image
    """
    # Create image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Create gradient background (dark blue to darker blue)
    for y in range(height):
        # Calculate color for this row
        ratio = y / height
        r = int(26 + (15 - 26) * ratio)
        g = int(26 + (33 - 26) * ratio)
        b = int(46 + (62 - 46) * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Add subtle overlay for depth
    overlay = Image.new('RGBA', (width, height), (15, 52, 96, 77))
    img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Extract kural text
    kural_line1 = kural_data.get('kural_tamil1', '').split('\n')[0] if '\n' in kural_data.get('kural_tamil1', '') else kural_data.get('kural_bamini1', '')
    kural_line2 = kural_data.get('kural_tamil1', '').split('\n')[1] if '\n' in kural_data.get('kural_tamil1', '') and len(kural_data.get('kural_tamil1', '').split('\n')) > 1 else kural_data.get('kural_bamini2', '')
    
    # If Tamil text not available, use Bamini
    if not kural_line1:
        kural_line1 = kural_data.get('kural_bamini1', '')
        kural_line2 = kural_data.get('kural_bamini2', '')
    
    kural_explanation = kural_data.get('kuralvilakam_english', '')
    kural_number = kural_data.get('kural_no', '')
    adhikaram = kural_data.get('adhikarm_english', '')
    
    # Try to load fonts that support Tamil Unicode
    # Windows typically has Nirmala.ttc (Collection) or Nirmala.ttf
    tamil_fonts = [
        "C:\\Windows\\Fonts\\Nirmala.ttc",   # Nirmala UI Collection (Standard on Win 10/11)
        "C:\\Windows\\Fonts\\Nirmala.ttf",   # Nirmala UI
        "C:\\Windows\\Fonts\\Latha.ttf",     # Latha (Legacy Windows Tamil font)
        "C:\\Windows\\Fonts\\Vijaya.ttf",    # Vijaya
    ]
    
    # Try each Tamil font
    tamil_font_loaded = False
    for font_path in tamil_fonts:
        try:
            # For .ttc files, we can specify an index, but default (0) usually works
            font_title = ImageFont.truetype(font_path, 42)    # Large for English Title
            font_subtitle = ImageFont.truetype(font_path, 28) # Medium for Tamil Subtitle
            font_label = ImageFont.truetype(font_path, 24)    # Small for Headers
            font_tiny = ImageFont.truetype(font_path, 18)     # Tiny for branding
            tamil_font_loaded = True
            print(f"Using Tamil font: {font_path}")
            break
        except (OSError, IOError):
            continue
    
    # Fallback to default if no Tamil font found
    if not tamil_font_loaded:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # Inner decorative rectangle with semi-transparent fill (Glassmorphism effect)
    inner_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    inner_draw = ImageDraw.Draw(inner_overlay)
    
    # Draw a clean, borderless semi-transparent card
    card_margin = 150
    inner_draw.rounded_rectangle(
        [(card_margin, card_margin), (width - card_margin, height - card_margin)],
        radius=30,
        fill=(15, 52, 96, 160) # A bit more opaque for better readability
    )
    img.paste(inner_overlay, (0, 0), inner_overlay)
    draw = ImageDraw.Draw(img)
    
    # Helper function to draw centered text with wrapping
    def draw_wrapped_centered_text(text, y_center, font, color, max_width):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Check length of line if word added
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        # Draw each line
        line_height = font.size * 1.3
        total_height = len(lines) * line_height
        start_y = y_center - (total_height / 2)
        
        for i, line in enumerate(lines):
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            x = (width - line_width) // 2
            draw.text((x, start_y + (i * line_height)), line, fill=color, font=font)
        
        return total_height

    # 1. Header: Kural Number and Chapter (English)
    header_y = card_margin + 60
    draw_wrapped_centered_text(
        f"THIRUKKURAL {kural_number} • {adhikaram.upper()}",
        header_y,
        font_label,
        (244, 162, 97), # Warm orange
        width - (card_margin * 2 + 100)
    )
    
    # 2. Main Title: English Explanation
    # Placed in the center of the card
    title_height = draw_wrapped_centered_text(
        kural_explanation,
        height // 2 - 40,
        font_title,
        (255, 255, 255), # Pure white
        width - (card_margin * 2 + 150)
    )
    
    # 3. Subtitle: Tamil Kural (fewer words/less prominent)
    # Placed below the English title
    tamil_y = height // 2 + (title_height / 2) + 50
    # Just show the first line of the kural or combined but smaller
    full_kural = f"{kural_line1}\n{kural_line2}"
    
    draw_wrapped_centered_text(
        full_kural,
        tamil_y,
        font_subtitle,
        (168, 218, 220, 200), # Muted teal with slight transparency
        width - (card_margin * 2 + 200)
    )
    
    # 4. Footer: Author Name
    footer_y = height - card_margin - 80
    draw_wrapped_centered_text(
        "~ THIRUVALLUVAR ~",
        footer_y,
        font_tiny,
        (233, 69, 96), # Logo pink/red
        width - (card_margin * 2)
    )
    
    # Save the image
    img.save(output_path, 'PNG')
    return output_path


def generate_wallpaper(output_path: str | None = None) -> str:

    kurals = load_thirukural_data()

    kural = get_random_kural(kurals)

    if output_path is None:
        from datetime import date
        today = date.today().isoformat()
        output_path = f"wallpaper_{today}.png"

    return create_wallpaper_image(kural, output_path)
