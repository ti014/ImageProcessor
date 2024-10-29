# Image Processor App

This Image Processor App allows users to crop or resize images. It provides an intuitive GUI where you can specify input and output folders, target dimensions, and choose between cropping or resizing your images. The app can automatically detect faces for cropping, and you can also rename processed files using randomly generated UUIDs.

## Features
- **Crop**: Crop images to the target size, centered around the detected face or image center.
- **Resize**: Resize images to the specified dimensions.
- **Auto-Rename**: Rename processed images with a unique UUID.
- **Cancel Operation**: Cancel ongoing image processing at any time.
- **Progress Tracking**: Track the progress of image processing through a progress bar.

## Installation
### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Install dependencies:
To install the required packages, run:
```bash
pip install -r requirements.txt
```

### Running the App
Run the following command to start the application:
```bash
python main.py
```

## Usage
1. **Input Folder**: Browse to select the folder containing the images to process.
2. **Output Folder**: Browse to select the folder where the processed images will be saved.
3. **Action Selection**: Choose between cropping or resizing images.
4. **Target Size**: Specify the target width and height for both cropping and resizing.
5. **Auto Rename**: Optionally, rename processed files with random UUIDs.

## Cancelling Processing
You can cancel the image processing task at any time by pressing the "Cancel" button. The process will stop, and no further images will be processed.
