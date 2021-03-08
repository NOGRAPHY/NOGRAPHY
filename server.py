from flask import *
from encoder import encoder
from embedder import embedder
from pdf2image import convert_from_path


app = Flask(__name__)

@app.route('/')
def index():
    secret = request.args.get('secret', '').strip()
    placeholder = request.args.get('placeholder', '').strip()
    print("secret length: " + str(len(secret)))
    print("placeholder length: " + str(len(placeholder)))

    if len(secret) * 3 > len(placeholder):
        return render_template('hide.html', error = 'Secret is too long. Make it shorter or the placeholder longer.')
    elif len(secret) > 0:
        embedder.generate_document(
            embedder.embed(
                embedder.setup_document(),
                placeholder,
                encoder.encode(secret, 3)), 'hidden_secret')
        images_from_path = convert_from_path('hidden_secret.pdf')
        images_from_path[0].save('hidden_secret.png')
        return send_file('hidden_secret.png', as_attachment=True)
    return render_template('hide.html')

if __name__ == "__main__":
    app.run()
