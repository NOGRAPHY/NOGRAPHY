import json
from encoder import encoder
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import string

FONT_SIZE = 36
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 500
MARGIN = 50
ENCODING_DECODING_BASE = 3


def lambda_handler(event, context):
    body = json.loads(event['body'])
    secret = body.get('secret', "LOTR is better than GOT")
    placeholder = body.get('placeholder', "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort.")
    # TODO: check for potential error cases (missing values, wrong types etc.)
    # TODO: catch too many characters in placeholder - define a limit for the user

    if not secret_fits_in_placeholder(secret, placeholder):
        return {
            "statusCode": 400,
            "error": "Secret is too long. Make it shorter or the placeholder longer."
        }
    else:
        fonts = load_fonts_from_fs(FONT_SIZE)
        encoded_secret = encoder.to_ints(
            encoder.encode(secret, ENCODING_DECODING_BASE))
        letters_and_fonts = get_letters_and_fonts(
            placeholder, encoded_secret, fonts)
        image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), 'white')

        fit_text(image, letters_and_fonts, 'black', MARGIN)

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_str = base64.b64encode(buffered.getvalue())

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'image/png',
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Credentials": True
            },
            "body": image_str,
            "isBase64Encoded": True
        }


def load_fonts_from_fs(font_size):
    return {
        0: ImageFont.truetype('./assets/0.ttf', font_size),
        1: ImageFont.truetype('./assets/1.ttf', font_size),
        2: ImageFont.truetype('./assets/2.ttf', font_size),
        3: ImageFont.truetype('./assets/3.ttf', font_size),
        4: ImageFont.truetype('./assets/4.ttf', font_size),
        5: ImageFont.truetype('./assets/5.ttf', font_size),
        6: ImageFont.truetype('./assets/6.ttf', font_size),
        7: ImageFont.truetype('./assets/7.ttf', font_size)
    }


def get_letters_and_fonts(placeholder, encoded_secret, fonts):
    letters_and_fonts = []
    index = 0
    while index < len(placeholder):
        if placeholder[index] in string.ascii_letters:
            if index < len(encoded_secret):
                letters_and_fonts.append(
                    (placeholder[index], fonts[encoded_secret[index]]))
            else:
                letters_and_fonts.append((placeholder[index], fonts[0]))
            index = index + 1
        else:
            letters_and_fonts.append((placeholder[index], fonts[0]))
            # slicing out the non-ASCII character, so it won't block the index
            placeholder = placeholder[:index] + placeholder[index+1:]
    return letters_and_fonts

# based on https://stackoverflow.com/questions/58041361/break-long-drawn-text-to-multiple-lines-with-pillow


def fit_text(img, letters_and_fonts, color, margin):
    width = img.size[0] - 2 - margin
    draw = ImageDraw.Draw(img)
    measure_font = ImageFont.truetype('./assets/0.ttf', FONT_SIZE)

    lines = list(break_into_lines(
        letters_and_fonts, width, measure_font, draw))

    height = sum(l[2] for l in lines)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")

    y = (img.size[1] - height) // 2
    for t, w, h in lines:
        x = (img.size[0] - w) // 2
        for letter, font in t:
            draw.text((x, y), letter,
                      font=font, fill=color)
            x = x + draw.textsize(letter, font=font)[0]
        y += h


def break_into_lines(letters_and_fonts, width, font, draw):
    if not letters_and_fonts:
        return
    lo = 0
    hi = len(letters_and_fonts)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = letters_and_fonts[:mid]
        w, h = draw.textsize(''.join([i[0] for i in t]), font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = letters_and_fonts[:lo]
    w, h = draw.textsize(''.join([i[0] for i in t]), font=font)
    yield t, w, h
    yield from break_into_lines(letters_and_fonts[lo:], width, font, draw)


def secret_fits_in_placeholder(secret, placeholder):
    return len(secret) * ENCODING_DECODING_BASE <= len(placeholder)
