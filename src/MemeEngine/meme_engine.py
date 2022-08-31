import os.path
import uuid

from PIL import Image
from PIL import ImageDraw, ImageFont

FONTS_PATH = "fonts/impact.ttf"


class MemeEngine:
    """
    The project defines a MemeGenerator module with the following responsibilities:

    Loading of a file from disk
    Transform image by resizing to a maximum width of 500px while maintaining the input aspect ratio
    Add a caption to an image (string input) with a body and author to a random location on the image.
    The class depends on the Pillow library to complete the defined, incomplete method signatures
    so that they work with JPEG/PNG files.

    The method signature to make the meme should be: make_meme(self, img_path, text, author, width=500) ->
    str #generated image path

    The init method should take a required argument for where to save the generated images: __init__(self, output_dir...).

    """

    def __init__(self, memes_path: str):
        self.memes_path = memes_path

    def make_meme(self, image_source, body, author, width=500):
        image = Image.open(image_source)
        print("Image size", image.size)
        if image.width > width:
            ratio = (width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(ratio)))
            image = image.resize((width, hsize), Image.ANTIALIAS)

        fnt = ImageFont.truetype(FONTS_PATH, 30)
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        d = ImageDraw.Draw(txt)

        MemeEngine.__draw_text(d, 20, 60, body + "\n- " + author, font=fnt, fill="white")
        out = Image.alpha_composite(image.convert(mode="RGBA"), txt)
        path = os.path.join(self.memes_path, str(uuid.uuid4()) + ".png")
        out.save(path, "PNG")

        return path

    @staticmethod
    def __draw_text(draw: ImageDraw, x: float, y: float, text: str, font: ImageFont, fill, border_color='black'):
        border_thickness = 1
        draw.multiline_text((x - border_thickness, y - border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x + border_thickness, y - border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x - border_thickness, y + border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x + border_thickness, y + border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x, y), text, font=font, fill=fill)
