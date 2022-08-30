import random
import os
from flask import Flask, render_template, abort, request

from MemeEngine import MemeEngine

"""
The project completes the Flask app starter code in app.py. All @TODO tasks listed in the file have been completed.

app.py uses the Quote Engine module and Meme Generator modules to generate a random captioned image.

app.py uses the requests package to fetch an image from a user submitted URL.

The flask server runs with no errors
"""

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)


def setup():
    """ Load all resources """

    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv'
    ]

    quotes = []
    for f in quote_files:
        from QuoteEngine import Ingestor
        quotes.extend(Ingestor.parse(f))
    print("Quotes:", quotes)
    images_path = "./_data/photos/dog/"

    imgs = []
    for root, _, files in os.walk(images_path):
        norm_root = os.path.normpath(root)
        imgs = [os.path.join(norm_root, name) for name in files]
    print("Imgs", imgs)
    return quotes, imgs


quotes, imgs = setup()


def create_dir_if_not_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    meme_folder = './static'
    create_dir_if_not_exists(meme_folder)
    meme = MemeEngine(meme_folder)
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    path = None

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
