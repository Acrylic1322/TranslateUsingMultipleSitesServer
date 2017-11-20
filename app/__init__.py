from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
