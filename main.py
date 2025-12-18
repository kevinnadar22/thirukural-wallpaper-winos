#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: main.py
Author: Maria Kevin
Created: 2025-12-19
Description: Generate and set Thirukural wallpaper for Windows desktop
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import ctypes
import os
from datetime import date

from utils import generate_wallpaper

SPI_SETDESKWALLPAPER = 20


def set_wallpaper(image_path: str) -> None:
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, abs_path, 3
    )


if __name__ == "__main__":
    today = date.today().isoformat()
    img_path = f"wallpaper_{today}.png"
    wallpaper_path = generate_wallpaper(img_path)
    set_wallpaper(wallpaper_path)
