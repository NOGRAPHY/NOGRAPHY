import json
from encoder import encoder
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import string
import os
import copy

FONT_SIZE = 72
IMAGE_WIDTH = 2480
MARGIN_LEFT_RIGHT = 248
MARGIN_TOP_BOTTOM = 248
ENCODING_DECODING_BASE = 3
CHARACTER_SPACING = 6
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
        image = Image.new("RGB", (IMAGE_WIDTH, estimate_image_height(
            dummy, FONT_SIZE, LINE_SPACING, IMAGE_WIDTH, MARGIN_TOP_BOTTOM)), 'white')

        fit_text(image, letters_and_fonts, 'black', FONT_SIZE,
                 CHARACTER_SPACING, LINE_SPACING, MARGIN_LEFT_RIGHT)
        with BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_str = str(base64.b64encode(buffer.getvalue()))[2:][:-1]

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'image/png',
                'Access-Control-Allow-Origin': '*'
            },
            "body": "{\"image\":\"" + image_str + "\"}",
            "isBase64Encoded": True
        }


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


# based on https://stackoverflow.com/questions/58041361/break-long-drawn-text-to-multiple-lines-with-pillow
def fit_text(img, letters_and_fonts, color, font_size, character_spacing, line_spacing, margin):
    width = img.size[0] - margin * 2
    draw = ImageDraw.Draw(img)
    path, _ = os.path.split(os.path.abspath(__file__))
    measure_font = ImageFont.truetype(
        os.path.join(path, 'assets', '0.ttf'), font_size)

    lines = break_into_lines(letters_and_fonts, width,
                             measure_font, font_size, character_spacing, line_spacing, draw)
    height = sum(l[2] for l in lines)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")

    y = (img.size[1] - height) // 2
    for t, w, h in lines:
        x = margin
        for letter, font in t:
            draw.text((x, y), letter, font=font, fill=color)
            x = x + draw.textsize(letter, font=font)[0] + character_spacing
        y += h


def break_into_lines(letters_and_fonts, width, measure_font, font_size, character_spacing, line_spacing, draw):
    if not letters_and_fonts:
        return
    words = split_into_words(letters_and_fonts)
    lines = []
    line = []
    current_line_width = 0
    for word in words:
        required_width, _ = draw.textsize(
            ''.join([letter_and_font[0] for letter_and_font in word]), font=measure_font)
        required_width += len(word) * character_spacing
        if current_line_width + required_width <= width:
            current_line_width += required_width
            line.extend(word)
        else:
            lines.append((copy.copy(line), required_width,
                         font_size * line_spacing))
            line.clear()
            line.extend(word)
            current_line_width = required_width
    lines.append((copy.copy(line), required_width, font_size * line_spacing))
    return lines


def split_into_words(letters_and_fonts):
    words = []
    word = []

    for letter_and_font in letters_and_fonts:
        word.append(letter_and_font)
        if letter_and_font[0] == " ":
            words.append(copy.copy(word))
            word.clear()
    words.append(word)
    return words


def secret_fits_in_dummy(secret, dummy):
    return len(secret) * 5 <= len(dummy)


def estimate_image_height(dummy, font_size, line_spacing, image_width, margin):
    # if the character spacing or the margin is changed, these values need to be recalibrated!
    letters_per_line = (image_width - 2 * margin / font_size) // 45
    number_of_lines = len(dummy) // letters_per_line
    height_without_margin = line_spacing * font_size * number_of_lines
    return int(height_without_margin) + 2 * margin


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
