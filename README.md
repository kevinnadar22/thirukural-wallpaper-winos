# Thirukural Wallpaper for Windows

A Python application that generates beautiful daily wallpapers featuring random verses from Thirukkural, the ancient Tamil literary masterpiece by Thiruvalluvar.

## Installation

```bash
# Clone the repository
git clone https://github.com/kevinnadar22/thirukural-wallpaper-winos.git
cd thirukural-wallpaper-winos

# Install dependencies using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

## Usage

```bash
# Run with uv
uv run main.py

# Or with python directly
python main.py
```

The script will:
1. Load Thirukkural data from `thirukural.json`
2. Select a random verse
3. Generate a wallpaper image (saved as `wallpaper_YYYY-MM-DD.png`)
4. Set it as your Windows desktop wallpaper

## Requirements

- Python 3.10+
- Windows OS
- Dependencies: Pillow, requests

## Building Executable

```bash
# Install dev dependencies
uv sync --group dev

# Build with PyInstaller
pyinstaller --onefile --icon=favicon.ico main.py
```

## License

This project uses Thirukkural verses which are in the public domain.

## Author

Maria Kevin
