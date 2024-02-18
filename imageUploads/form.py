from django import forms
from django.core.files.images import get_image_dimensions
from .models import Image
from PIL import Image as PilImage
from io import BytesIO

# Define a list of RGB tuples representing "happy" colors
HAPPY_COLORS = [
    (255, 255, 0),  # Yellow
    (255, 192, 203),  # Pink
    (0, 255, 0),  # Green
    (0, 191, 255),  # Blue
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (255, 255, 255),  # White
    (0, 0, 0),  # Black
]

# Color tolerance threshold for considering a color as "happy"
COLOR_TOLERANCE = 200


def color_distance(rgb1, rgb2):
    """Calculate the Euclidean distance between two RGB colors."""
    return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("caption", "image")

    def clean_image(self):
        """Custom validation for the 'image' field."""
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("No image provided.")

        width, height = get_image_dimensions(image)
        if width != 512 or height != 512:
            raise forms.ValidationError("The image must be 512x512 pixels in size.")

        image_file = BytesIO(image.read())
        image_pil = PilImage.open(image_file).convert('RGBA')
        pixels = image_pil.load()

        # Verify that non-transparent pixels are within a circular area
        for x in range(width):
            for y in range(height):
                distance = ((x - 256) ** 2 + (y - 256) ** 2) ** 0.5
                if distance > 255.5 and pixels[x, y][3] != 0:
                    raise forms.ValidationError("All non-transparent pixels must be within a circular area.")

        # Count the number of pixels that match the "happy" colors
        happy_color_count = sum(
            1 for x in range(width) for y in range(height)
            if pixels[x, y][3] > 0 and any(
                color_distance(pixels[x, y][:3], happy_color) < COLOR_TOLERANCE for happy_color in HAPPY_COLORS
            )
        )

        total_pixels = width * height
        happy_percentage = happy_color_count / total_pixels
        if happy_percentage < 0.5:
            raise forms.ValidationError(f"Insufficient 'happy' colors: {happy_percentage:.2%} of the image.")

        image_file.seek(0)
        image.file = image_file

        return image
