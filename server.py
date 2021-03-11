import os
import uuid

from flask import Flask, request, render_template, send_file
from pdf2image import convert_from_path

from encoder import encoder
from embedder import embedder

SERVER_TMP = "server_tmp"
os.makedirs(SERVER_TMP, exist_ok=True)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
            file_pdf = os.path.join(SERVER_TMP, 'hidden_secret-{}'.format(uuid.uuid4()))
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


if __name__ == "__main__":
    app.run()
