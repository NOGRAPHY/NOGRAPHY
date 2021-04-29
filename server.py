import os
import uuid
import secrets
from distutils import dir_util

from flask import Flask, request, redirect, render_template, send_file, flash
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from embedder import embedder
from encoder import encoder
from decoder import decoder
from ocr import ocr
from cnn.single_model.cnn_single_model import SingleModel


SERVER_TMP = os.path.join(os.path.split(os.path.realpath(__file__))[0], "server_tmp")
UPLOAD_TMP = os.path.join(SERVER_TMP, "upload")
os.makedirs(UPLOAD_TMP, exist_ok=True)
dir_util.copy_tree(os.path.join(os.path.split(os.path.realpath(__file__))[0], "embedder/fonts"),
                   os.path.join(SERVER_TMP, "fonts"))

ENCODING_DECODING_BASE = 3

cnn_model = SingleModel()

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route('/')
def index():
    return redirect('/hide')


@app.route('/hide', methods=['GET', 'POST'])
def hide():
    if request.method == 'GET':
        return render_template('hide.html')
    if request.method == 'POST':
        secret = request.form.get('secret', '').strip()
        placeholder = request.form.get('placeholder', '').strip()
        show_colors = request.form.get('show_colors') is not None

        print("secret length: " + str(len(secret)))
        print("placeholder length: " + str(len(placeholder)))

        if len(secret) * ENCODING_DECODING_BASE > len(placeholder):
            return render_template('hide.html', error='Secret is too long. Make it shorter or the placeholder longer.')
        elif len(secret) > 0:
            file_pdf = os.path.join(SERVER_TMP, 'hidden-secret_{}'.format(uuid.uuid4()))
            file_png = file_pdf + ".png"

            embedder.generate_document(
                document=embedder.embed(
                    embedder.setup_document(),
                    placeholder,
                    encoder.encode(secret, ENCODING_DECODING_BASE),
                    show_colors
                ),
                file_name=file_pdf
            )
            images_from_path = convert_from_path(file_pdf + ".pdf", dpi=900)
            images_from_path[0].save(file_png)

            return send_file(file_png, as_attachment=True)

        return render_template('hide.html')


@app.route('/expose', methods=['GET', 'POST'])
def expose():
    if request.method == 'GET':
        return render_template('expose.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No or empty file uploaded.')
            return render_template('expose.html')

        file = request.files['file']
        filename = os.path.splitext(secure_filename(file.filename))
        filename = "{}_{}{}".format(filename[0], uuid.uuid4(), filename[1])

        filepath = os.path.join(UPLOAD_TMP, filename)
        file.save(filepath)

        try:
            characters, boxes = ocr.recognizeCharacters(filepath)
            glyphs = ocr.createLetterImages(characters, boxes, filepath, 200, save_files=False)
        except IndexError as exception:
            flash(exception)
            return render_template('expose.html')

        font_indexes, _, confidence = cnn_model.predict(glyphs)
        exposed_message = decoder.decode_from_font_indexes(font_indexes, ENCODING_DECODING_BASE)

        print(font_indexes)
        print(exposed_message)
        print(confidence)

        return render_template('expose.html', exposed_message=exposed_message, confidence=confidence)


if __name__ == "__main__":
    app.run()
