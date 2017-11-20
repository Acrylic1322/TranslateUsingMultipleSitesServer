import sys, json
import urllib, urllib.request
from app.site_parser.weblio import Weblio
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def hello():
    return "<h2>Hello, world!</h2>"

@app.route('/weblio/', methods=['GET'])
def weblio():
    src = request.args.get('src')
    if src is None:
        return ""

    url = 'https://translate.weblio.jp/?lp=EJ&lpf=EJ&originalText=' + urllib.parse.quote(src)
    req = urllib.request.Request(url=url)
    res = urllib.request.urlopen(req)

    weblio = Weblio()
    weblio.feed(res.read().decode('utf-8'))
    weblio.close()

    return json.dumps(weblio.result, ensure_ascii=False)


if __name__ == '__main__':
    app.debug = True
    app.run()
