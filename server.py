import os
import uuid

from flask import Flask, request, redirect, render_template, send_file, flash
import secrets
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from encoder import encoder
from embedder import embedder

SERVER_TMP = os.path.join(os.path.split(os.path.realpath(__file__))[0], "server_tmp")
UPLOAD_TMP = os.path.join(SERVER_TMP, "upload")
os.makedirs(UPLOAD_TMP, exist_ok=True)

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

        print("secret length: " + str(len(secret)))
        print("placeholder length: " + str(len(placeholder)))

        if len(secret) * 3 > len(placeholder):
            return render_template('hide.html', error='Secret is too long. Make it shorter or the placeholder longer.')
        elif len(secret) > 0:
            file_pdf = os.path.join(SERVER_TMP, 'hidden-secret_{}'.format(uuid.uuid4()))
            file_png = file_pdf + ".png"

            embedder.generate_document(
                document=embedder.embed(
                    embedder.setup_document(),
                    placeholder,
                    encoder.encode(secret, 3)
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

        file.save(os.path.join(UPLOAD_TMP, filename))

        return render_template('expose.html')


if __name__ == "__main__":
    app.run()
