"""
Provides functionality to create meme from command line.

The program takes three OPTIONAL arguments:
- A string quote body
- A string quote author
- An image path

The program returns a path to a generated image.
If any argument is not defined, a random selection is used.
"""
import argparse
import os
import random

from meme_engine import MemeEngine
from quote_engine.models import QuoteModel
from helper import find_images_in_folder, ingest_quotes

MEMES_FOLDER = './tmp'
if not os.path.exists(MEMES_FOLDER):
    os.makedirs(MEMES_FOLDER)
meme_engine = MemeEngine(MEMES_FOLDER)


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote."""
    if path is None:
        images_folder = "./_data/photos/dog/"
        imgs = find_images_in_folder(images_folder)
        print(imgs)
        if imgs is None or len(imgs) == 0:
            raise Exception("Could not find images in folder", images_folder)
        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv'
        ]
        quotes = ingest_quotes(quote_files)
        print("Quotes:", quotes)
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    path = meme_engine.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a motivational meme')
    parser.add_argument('--path', type=str, help='path to an image file')
    parser.add_argument(
        '--body',
        type=str,
        help='quote body to add to the image')
    parser.add_argument(
        '--author',
        type=str,
        help='quote author to add to the image')

    args = parser.parse_args()
    meme_path = generate_meme(args.path, args.body, args.author)
    meme_path = meme_path.replace(".", os.getcwd(), 1)
    print(meme_path)
