"""Provides functionality for manipulating memes."""

import os.path
import uuid

from PIL import Image
from PIL import ImageDraw, ImageFont


class MemeEngine:
    """Provides functionality for manipulating memes."""

    def __init__(
            self,
            output_dir: str,
            font_path="fonts/impact.ttf",
            font_size: int = 30,
            transformed_image_format="GIF"):
        """Create Meme Engine.

        :param output_dir: location where to save transformed images
        :param font_path: location where to the font file
        :param font_size: size of the font
        :param transformed_image_format: file format of the transformed image. For possible values please refer to
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#fully-supported-formats
        """
        self.font = ImageFont.truetype(font_path, font_size)
        self.output_dir = output_dir
        self.transformed_image_format = transformed_image_format

    def make_meme(self, image_source, body, author, max_width=500):
        """Create meme.

        :param image_source: A filename (string), pathlib.Path object or a file object.
        The file object must implement ``file.read``,
        ``file.seek``, and ``file.tell`` methods,
        and be opened in binary mode.

        :param body: quote body
        :param author: quote author
        :param max_width: if the width of the image_source is greater than max_width
        image will be resized keeping the aspect ratio
        """
        image = Image.open(image_source)
        if image.width > max_width:
            ratio = (max_width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(ratio)))
            image = image.resize((max_width, hsize), Image.ANTIALIAS)

        draw_context = ImageDraw.Draw(image)
        MemeEngine.__draw_text(draw_context, 20, 60, body + "\n- " + author,
                               font=self.font, fill="white")
        path = os.path.join(self.output_dir, str(uuid.uuid4()) + "." + self.transformed_image_format.lower())
        image.save(path, self.transformed_image_format)

        return path

    @staticmethod
    def __draw_text(
            draw_context: ImageDraw,
            x: float,
            y: float,
            text: str,
            font: ImageFont,
            fill,
            border_color='black',
            border_thickness=1):
        """Draw multiline text with border.

        :param: draw: draw context used to draw text
        :param: x: x coordinate of the left top corner of the text
        :param: y: y coordinate of the left top corner of the text
        :param: text: text itself
        :param: font: text font
        :param: border_color: color of the border
        :param: border_thickness: thickness of the border
        """
        draw_context.multiline_text(
            (x - border_thickness,
             y - border_thickness),
            text,
            font=font,
            fill=border_color)
        draw_context.multiline_text(
            (x + border_thickness,
             y - border_thickness),
            text,
            font=font,
            fill=border_color)
        draw_context.multiline_text(
            (x - border_thickness,
             y + border_thickness),
            text,
            font=font,
            fill=border_color)
        draw_context.multiline_text(
            (x + border_thickness,
             y + border_thickness),
            text,
            font=font,
            fill=border_color)
        draw_context.multiline_text((x, y), text, font=font, fill=fill)
