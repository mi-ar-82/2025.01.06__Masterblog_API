from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    This function handles the root route ('/') of the Flask application.

    It renders the 'index.html' template,
    which is assumed to be located in the 'templates' folder.

    Returns:
        str: The rendered HTML content of 'index.html'.
    """
    return render_template("index.html")  # Render the index.html template


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
