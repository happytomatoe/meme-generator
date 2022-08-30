class MemeEngine:
    # TODO:
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

    def __init__(self, memes_path):
        self.memes_path = memes_path

    def make_meme(self, img, body, author):
        pass
