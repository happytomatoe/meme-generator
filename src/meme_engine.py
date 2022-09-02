"""Provides functionality for manipulating memes."""
import logging
import os.path
import random
import textwrap
import uuid

from PIL import Image
from PIL import ImageDraw, ImageFont

log = logging.getLogger(__name__)


class QuoteTooLongException(Exception):
    """Raised when quote is too long."""


class MemeEngine:
    """Provides functionality for manipulating memes."""

    def __init__(
            self,
            output_dir: str,
            font_path="fonts/impact.ttf",
            font_size: int = 30,
            transformed_image_format="GIF",
    ):
        """Create Meme Engine.

        :param output_dir: location where to save transformed images
        :param font_path: location where to the font file
        :param font_size: size of the font
        :param transformed_image_format: file format of the transformed image.
         For possible values please refer to
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#fully-supported-formats
        """
        self.font = ImageFont.truetype(font_path, font_size)
        self.output_dir = output_dir
        self.transformed_image_format = transformed_image_format

    def make_meme(self, image_source, body, author, max_width=500):
        """Create meme.

        :param image_source: A filename (string),
        pathlib.Path object or a file object.
        The file object must implement ``file.read``,
        ``file.seek``, and ``file.tell`` methods,
        and be opened in binary mode.

        :param body: quote body
        :param author: quote author
        :param max_width: if the width of the image_source is greater
        than max_width image will be resized keeping the aspect ratio
        """
        image = Image.open(image_source)
        image = self.__resize_image(image, max_width)
        self.__draw_quote(image, author, body)
        path = os.path.join(
            self.output_dir,
            str(uuid.uuid4()) + "." + self.transformed_image_format.lower(),
        )
        image.save(path, self.transformed_image_format)

        return path

    @staticmethod
    def __resize_image(image, max_width):
        """
        Resize the image if it's width is greater than max_width.

        :param image: The image to resize.
        :param max_width: The maximum width of the resized image.
        """
        if image.width > max_width:
            ratio = max_width / float(image.size[0])
            hsize = int((float(image.size[1]) * float(ratio)))
            image = image.resize((max_width, hsize), Image.ANTIALIAS)
        return image

    def __draw_quote(self, image: Image, author: str,
                     body: str, max_line_width=40):
        """Draw quote on an image.

        :param image:

        :param body: quote body
        :param author: quote author
        :param max_line_width: max character on a single line.
        Will be used if text is longer than max_line_width
        """
        draw_context = ImageDraw.Draw(image)

        lines = textwrap.wrap(body, width=max_line_width)
        lines.extend(textwrap.wrap("- " + author, width=max_line_width))

        lines_sizes = [self.font.getsize(line) for line in lines]

        x, y = self.__pick_starting_coordinates(image, lines, lines_sizes)

        for line in lines:
            height = self.font.getsize(line)[1]
            self.__draw_text_line(
                draw_context, x, y, line,
                font=self.font, fill="white"
            )
            y += height

    @staticmethod
    def __pick_starting_coordinates(image, lines, lines_sizes):
        max_width = max(s[0] for s in lines_sizes)
        height_sum = sum(s[1] for s in lines_sizes)
        text_max_y = image.height - height_sum
        text_max_x = image.width - max_width
        log.debug("height: %s,  width: %s", text_max_y, text_max_x)
        logging.debug("Lines %s", lines)
        if text_max_y < 1 or text_max_x < 1:
            raise QuoteTooLongException("Quote is too long")
        y = random.randint(int(0.1 * text_max_y), int(0.9 * text_max_y))
        x = random.randint(int(0.1 * text_max_x), int(0.9 * text_max_x))
        return x, y

    @staticmethod
    def __draw_text_line(
            draw_context: ImageDraw,
            x: float,
            y: float,
            text: str,
            font: ImageFont,
            fill,
            border_color="black",
            border_thickness=1,
    ):
        """Draw multiline text with border.

        :param: draw: draw context used to draw text
        :param: x: x coordinate of the left top corner of the text
        :param: y: y coordinate of the left top corner of the text
        :param: text: text itself
        :param: font: text font
        :param: border_color: color of the border
        :param: border_thickness: thickness of the border
        """
        draw_context.text(
            (x - border_thickness, y - border_thickness),
            text,
            font=font,
            fill=border_color,
        )
        draw_context.text(
            (x + border_thickness, y - border_thickness),
            text,
            font=font,
            fill=border_color,
        )
        draw_context.text(
            (x - border_thickness, y + border_thickness),
            text,
            font=font,
            fill=border_color,
        )
        draw_context.text(
            (x + border_thickness, y + border_thickness),
            text,
            font=font,
            fill=border_color,
        )
        draw_context.text((x, y), text, font=font, fill=fill)
