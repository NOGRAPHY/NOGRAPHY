from flask import *
app = Flask(__name__)

placeholder = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'

@app.route('/')
def index():
    message = request.args.get('message', '').strip()
    if len(message) > 10:
        return render_template('hide.html', error = 'That message is to long. Please enter no more than 10 characters.')
    return render_template('hide.html')

if __name__ == "__main__":
    app.run()
