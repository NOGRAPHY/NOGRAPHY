import json
from embedder import embedder
from encoder import encoder 
import os

ENCODING_DECODING_BASE = 3

def lambda_handler(event, context):
    secret = event['secret'].strip()
    placeholder = event['placeholder'].strip()
    show_colors = event['show_colors']

    if len(secret) * ENCODING_DECODING_BASE > len(placeholder):
        return {
            "statusCode": 400,
            "error": "Secret is too long. Make it shorter or the placeholder longer."
            }
    else:
        document = embedder.embed(
                        embedder.setup_document(),
                        placeholder,
                        encoder.encode(secret, ENCODING_DECODING_BASE),
                        show_colors
                    )

        document.generate_pdf('/tmp/pdf', clean_tex=clean_tex, compiler="pdfLaTeX")
        file_generated = os.path.isfile('/tmp/pdf')

        return {
            "statusCode": 200,
            "headers": "{'Content-type' : 'application/pdf'}",
            "body": file_generated
        }