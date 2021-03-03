from flask import *
from encoder import encoder
from embedder import embedder

app = Flask(__name__)

placeholder = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'
secret_max_length = 50


@app.route('/')
def index():
    secret = request.args.get('secret', '').strip()
    if len(secret) > secret_max_length:
        return render_template('hide.html', error = 'Secret is too long. Enter no more than ' + str(secret_max_length)+ ' characters.')
    elif len(secret) > 0:
        embedder.generate_document(
            embedder.embed(
                embedder.setup_document(),
                placeholder,
                encoder.encode(secret, 3)), 'hidden_secret')
        return send_file('hidden_secret.pdf', as_attachment=True)
    return render_template('hide.html')

if __name__ == "__main__":
    app.run()
