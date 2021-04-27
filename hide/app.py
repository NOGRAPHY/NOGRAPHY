import json
from embedder import embedder
from encoder import encoder
import os
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO


ENCODING_DECODING_BASE = 3


def lambda_handler(event, context):
    placeholder = "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."
    image = Image.new("RGB", (500, 200), 'white')
    Font = ImageFont.truetype('./assets/Gidole-Regular.ttf', 18)
    fit_text(image, placeholder, (0, 0, 0), Font, 50)

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


# based on https://stackoverflow.com/questions/58041361/break-long-drawn-text-to-multiple-lines-with-pillow
def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font, margin):
    width = img.size[0] - 2 - margin
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, fill=color)
        y += h


