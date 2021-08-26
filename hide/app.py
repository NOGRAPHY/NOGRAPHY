import json
from encoder import encoder
from text_to_image import text_to_image
from PIL import ImageFont
import base64
from io import BytesIO
import string
import os

FONT_SIZE = 72
FONT_COLOR = 'black'
IMAGE_WIDTH = 2480
MARGIN_LEFT_RIGHT = 248
MARGIN_TOP_BOTTOM = 248
ENCODING_DECODING_BASE = 3
CHARACTER_SPACING = 1
LINE_SPACING = 1.1


def lambda_handler(event, context):
    if 'body' not in event:
        return client_error("Missing request body.")
    body = json.loads(event['body'])
    if body.get('wake-up', False):
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    secret = body.get('secret', '')
    dummy = body.get('dummy', '')
    if secret == '':
        return client_error('No secret found.')
    if dummy == '':
        return client_error('No dummy found.')

    if len(dummy) > 1600:
        return client_error("Dummy is too long. Max is 1600 characters.")
    if len(secret) > 320:
        return client_error("Secret is too long. Max is 320 characters.")
    if not secret_fits_in_dummy(secret, dummy):
        return client_error("Secret is too long. Make it shorter or the dummy longer.")
    else:
        fonts = load_fonts_from_fs(FONT_SIZE)
        encoded_secret = encoder.to_ints(
            encoder.encode(secret, ENCODING_DECODING_BASE))
        letters_and_fonts = get_letters_and_fonts(
            dummy, encoded_secret, fonts)
        image = text_to_image.fit_text(letters_and_fonts, FONT_COLOR, FONT_SIZE, IMAGE_WIDTH,
                 CHARACTER_SPACING, LINE_SPACING, MARGIN_LEFT_RIGHT, MARGIN_TOP_BOTTOM)
        with BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'image/png',
                'Access-Control-Allow-Origin': '*'
            },
            "body": "{\"image\":\"" + image_str + "\"}",
            "isBase64Encoded": True
        }


def secret_fits_in_dummy(secret, dummy):
    return len(secret) * 5 <= len(dummy)


def load_fonts_from_fs(font_size):
    path, _ = os.path.split(os.path.abspath(__file__))
    return {
        0: ImageFont.truetype(os.path.join(path, 'assets', '0.ttf'), font_size),
        1: ImageFont.truetype(os.path.join(path, 'assets', '1.ttf'), font_size),
        2: ImageFont.truetype(os.path.join(path, 'assets', '2.ttf'), font_size),
        3: ImageFont.truetype(os.path.join(path, 'assets', '3.ttf'), font_size),
        4: ImageFont.truetype(os.path.join(path, 'assets', '4.ttf'), font_size),
        5: ImageFont.truetype(os.path.join(path, 'assets', '5.ttf'), font_size),
        6: ImageFont.truetype(os.path.join(path, 'assets', '6.ttf'), font_size),
        7: ImageFont.truetype(os.path.join(path, 'assets', '7.ttf'), font_size),
        8: ImageFont.truetype(os.path.join(path, 'assets', '8.ttf'), font_size)
    }


def get_letters_and_fonts(dummy, encoded_secret, fonts):
    letters_and_fonts = []
    index = 0
    while index < len(dummy):
        if dummy[index] in string.ascii_letters:
            if index < len(encoded_secret):
                letters_and_fonts.append(
                    (dummy[index], fonts[encoded_secret[index]]))
            else:
                letters_and_fonts.append((dummy[index], fonts[8]))
            index = index + 1
        else:
            letters_and_fonts.append((dummy[index], fonts[8]))
            # slicing out the non-ASCII character, so it won't block the index
            dummy = dummy[:index] + dummy[index + 1:]
    return letters_and_fonts


def client_error(error_message):
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps({"error": error_message})
    }


if __name__ == "__main__":
    #print(lambda_handler({"body": "{}"}, None)["body"])
    print(lambda_handler({"body": "{\"dummy\": \"In a hole in the ground there lived a hobbit. "
                                  "Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, "
                                  "nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: "
                                  "it was a hobbit-hole, and that means comfort.\","
                                  " \"secret\": \"LOTR is better than GOT\"}"}, None)["body"])
