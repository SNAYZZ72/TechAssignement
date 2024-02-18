from django import forms
from django.core.files.images import get_image_dimensions
from .models import Image
from PIL import Image as PilImage
from io import BytesIO
from PIL import ImageDraw as PilImageDraw

HAPPY_COLORS = [
    (255, 255, 0),  # Yellow
    (255, 192, 203),  # Pink
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (173, 216, 230),  # Light Blue
    (192, 192, 192),  # Silver
    (255, 215, 0),  # Gold
    (255, 255, 255),  # White
]
COLOR_TOLERANCE = 200


def color_distance(rgb1, rgb2):
    """Calculate Euclidean distance between two RGB colors."""
    return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5


def validate_image_dimensions(width, height):
    """Ensure the image is of the correct dimensions."""
    if width != 512 or height != 512:
        raise forms.ValidationError("Image dimensions must be 512x512 pixels.")



try:
    # Pour Pillow >= 7.0.0
    resample_filter = PilImage.Resampling.LANCZOS
except AttributeError:
    # Pour les versions antérieures de Pillow
    resample_filter = PilImage.ANTIALIAS

def resize_and_convert_to_circle(image_pil):
    """Resize image to 512x512 and convert to a circle with transparent background."""
    # Utiliser 'resample_filter' déterminé selon la version de Pillow
    image_pil = image_pil.resize((512, 512), resample_filter)
    mask = PilImage.new('L', (512, 512), 0)
    PilImageDraw.Draw(mask).ellipse((0, 0, 512, 512), fill=255)
    result = PilImage.new('RGBA', (512, 512), (255, 255, 255, 0))
    result.paste(image_pil, (0, 0), mask)
    return result

def validate_pixels_within_circle(pixels, width, height):
    """Verify that non-transparent pixels are within a circular area."""
    for x in range(width):
        for y in range(height):
            if ((x - 256) ** 2 + (y - 256) ** 2) ** 0.5 > 255.5 and pixels[x, y][3] != 0:
                raise forms.ValidationError("Non-transparent pixels must be within a 256-pixel radius circle.")


def count_happy_colors(pixels, width, height):
    """Count pixels that are considered 'happy' colors."""
    return sum(
        1 for x in range(width) for y in range(height)
        if pixels[x, y][3] > 0 and any(
            color_distance(pixels[x, y][:3], happy_color) < COLOR_TOLERANCE for happy_color in HAPPY_COLORS
        )
    )


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("caption", "image")

    def clean_image(self):
        """Custom validation for the 'image' field."""
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("An image is required.")

        image_file = BytesIO(image.read())
        image_pil = PilImage.open(image_file).convert('RGBA')


        width, height = image_pil.size
        if width != 512 or height != 512:
            image_pil = resize_and_convert_to_circle(image_pil)
        else:
            pixels = image_pil.load()
            validate_pixels_within_circle(pixels, width, height)

        happy_color_count = count_happy_colors(image_pil.load(), 512, 512)

        happy_percentage = happy_color_count / (512 * 512)
        if happy_percentage < 0.5:
            raise forms.ValidationError(f"Image must contain at least 50% 'happy' colors, current: {happy_percentage:.2%}.")

        final_image_file = BytesIO()
        image_pil.save(final_image_file, format='PNG')
        final_image_file.seek(0)

        image.file = final_image_file

        return image
