import json
from embedder import embedder
from encoder import encoder
import os
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import string

FONT_SIZE = 18

def lambda_handler(event, context):
    placeholder = "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."
    secret = "LOTR is better than GOT"
    encoded_secret = [int(c, 2) for c in encoder.encode(secret)]

    image = Image.new("RGB", (500, 200), 'white')

    letters_and_fonts = get_letters_and_fonts(placeholder, encoded_secret)

    fit_text(image, letters_and_fonts, 'black', margin=50)

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_str = base64.b64encode(buffered.getvalue())
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'image/png'
        },
        "body": image_str,
        "isBase64Encoded": True
    }

    #placeholder = event['placeholder'].strip()
    #show_colors = event['show_colors']

    # if len(secret) * ENCODING_DECODING_BASE > len(placeholder):
    #    return {
    #        "statusCode": 400,
    #        "error": "Secret is too long. Make it shorter or the placeholder longer."
    #    }
    # else:

    # encoded_secret = encoder.encode(secret, ENCODING_DECODING_BASE)
    # document = embedder.embed(
    #                 embedder.setup_document(),
    #                 placeholder,
    #                 encoded_secret,
    #                 show_colors
    #             )


def get_letters_and_fonts(placeholder, encoded_secret):
    letters_and_fonts = []
    index = 0
    while index < len(placeholder):
        if placeholder[index] in string.ascii_letters:
            if index < len(encoded_secret):
                letters_and_fonts.append(
                    (placeholder[index], encoded_secret[index]))
            else:
                letters_and_fonts.append((placeholder[index], 0))
            index = index + 1
        else:
            letters_and_fonts.append((placeholder[index], 0))
            # slicing out the non-ASCII character, so it won't block the index
            placeholder = placeholder[:index] + placeholder[index+1:]
    return letters_and_fonts


# based on https://stackoverflow.com/questions/58041361/break-long-drawn-text-to-multiple-lines-with-pillow
def break_into_lines(letters_and_fonts, width, font, draw):

# letters = ''.join([i[0] for i in letters_and_fonts])


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


def fit_text(img, letters_and_fonts, color, margin):
    width = img.size[0] - 2 - margin
    draw = ImageDraw.Draw(img)
    measure_font = ImageFont.truetype('./assets/0.ttf', FONT_SIZE)
    pieces = list(break_into_lines(letters_and_fonts, width, measure_font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        for letter, font in t:
            draw.text((x, y), letter,
                      font=ImageFont.truetype('./assets/'+str(font)+'.ttf', FONT_SIZE), fill=color)
            x = x + draw.textsize(letter)[0]
        y += h
