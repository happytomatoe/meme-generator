import os.path
import uuid

from PIL import Image
from PIL import ImageDraw, ImageFont

FONTS_PATH = "fonts/impact.ttf"


class MemeEngine:

    def __init__(self, output_dir: str):
        """
        Create Meme Engine
        :param output_dir: location where to save transformed images
        """
        self.output_dir = output_dir

    def make_meme(self, image_source, body, author, max_width=500):
        """
        Create meme

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

        fnt = ImageFont.truetype(FONTS_PATH, 30)
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        d = ImageDraw.Draw(txt)

        MemeEngine.__draw_text(d, 20, 60, body + "\n- " + author, font=fnt, fill="white")
        out = Image.alpha_composite(image.convert(mode="RGBA"), txt)
        path = os.path.join(self.output_dir, str(uuid.uuid4()) + ".png")
        out.save(path, "PNG")

        return path

    @staticmethod
    def __draw_text(draw: ImageDraw, x: float, y: float, text: str, font: ImageFont, fill, border_color='black',
                    border_thickness=1):
        """
        Draw multiline text with border

        :param: draw: draw context used to draw text
        :param: x: x coordinate of the left top corner of the text
        :param: y: y coordinate of the left top corner of the text
        :param: text: text itself
        :param: font: text font
        :param: border_color: color of the border
        :param: border_thickness: thickness of the border
        """
        draw.multiline_text((x - border_thickness, y - border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x + border_thickness, y - border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x - border_thickness, y + border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x + border_thickness, y + border_thickness), text, font=font, fill=border_color)
        draw.multiline_text((x, y), text, font=font, fill=fill)
