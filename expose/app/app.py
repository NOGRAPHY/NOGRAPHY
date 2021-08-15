import json
from ocr import ocr
from cnn.glyph_recognizer import GlyphRecognizer
from decoder import decoder


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
    image = body.get('image', '')

    if image == '':
        return client_error("No image found.")

    # ocr
    boxes = ocr.recognize_boxes(image)
    glyph_images = ocr.create_glyph_images(boxes, image, 200)

    # cnn
    glyph_recognizer = GlyphRecognizer()
    font_indexes, confidence = glyph_recognizer.predict(glyph_images)

    # decode
    try:
        exposed_message = decoder.decode_from_font_indexes(font_indexes)

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "exposed_message": exposed_message,
                    "font_indexes": font_indexes,
                    "confidence": confidence,
                }
            ),
        }
    except UnicodeDecodeError as e:
        return client_error("The secret message could not be exposed.")


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
    print(lambda_handler({"body": "{}"}, None)["body"])
