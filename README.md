# 5-Prong Image Transformation

A Streamlit web application that allows users to transform images through five powerful transformation tools: vertical stretch, horizontal stretch, rotation, vertical flip, and horizontal flip.

## Features

### Image Transformations
- **Vertical Stretch**: Stretch images vertically with customizable factors (1x-5x)
- **Horizontal Stretch**: Stretch images horizontally with customizable factors (1x-5x)
- **Rotate**: Rotate images 90 degrees clockwise or counterclockwise
- **Vertical Flip**: Mirror images along the horizontal axis
- **Horizontal Flip**: Mirror images along the vertical axis

### Image Management
- **Upload**: Support for JPG, PNG, and JPEG formats
- **Download**: Save transformed images to your local machine with custom filenames
- **Caption**: Add optional captions to your images
- **The Collection**: Save and organize transformations in a persistent database

### Smart Features
- Size validation to prevent memory overflow (10,000 pixel limit per dimension)
- Real-time image preview
- Interactive dialogs for transformation parameters
- Caption-based filename generation for downloads

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd image_transformation
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your browser to `http://localhost:8501`

3. Upload an image using the file uploader

4. Apply transformations using the five transformation buttons

5. Download your transformed image or save it to The Collection

## Project Structure
```
image_transformation/
├── src/
│   └── app.py              # Main application file
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Dependencies

- `streamlit` - Web application framework
- `numpy` - Array operations for image manipulation
- `Pillow` (PIL) - Image processing library

## Transformation Details

### Stretch Operations
- Uses NumPy's `repeat` function to duplicate pixels
- Configurable stretch factors from 1x to 5x
- Automatic size validation to prevent oversized images

### Rotation
- 90-degree increments only
- Uses NumPy's `rot90` function
- Interactive dialog for direction selection

### Flip Operations
- Instant vertical and horizontal mirroring
- Uses NumPy's `flip` function along specified axes

## The Collection

The Collection feature allows you to:
- Save transformed images to a persistent database
- Browse previously saved images
- Organize your transformations with captions
- Retrieve and continue editing saved images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created by Griffin Kuchar as an introduction to AL/ML undergraduate research

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Image processing powered by [NumPy](https://numpy.org/) and [Pillow](https://pillow.readthedocs.io/)