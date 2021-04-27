import json
from embedder import embedder
from encoder import encoder
import os
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO


ENCODING_DECODING_BASE = 3


def lambda_handler(event, context):
    image = Image.new("RGB", (200, 200), "green")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "nography")
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
