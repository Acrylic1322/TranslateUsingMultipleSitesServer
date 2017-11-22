import sys, json
import urllib, urllib.request
from app.site_parser.weblio import Weblio
from flask import Flask, render_template, send_from_directory, request, abort

app = Flask(__name__)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def hello():
    return "<h2>Hello, world!</h2>"

@app.route('/weblio/<src>/<dst>/', methods=['GET'])
def weblio(src, dst):
    codeset = {
        "en": "E",
        "jp": "J"
    }

    text = request.args.get('text')
    if text is None:
        return ""

    src_for_url = ''
    if src in codeset:
        src_for_url = codeset[src]

    dst_for_url = ''
    if dst in codeset:
        dst_for_url = codeset[dst]

    if len(src_for_url) == 0 or len(dst_for_url) == 0:
        abort(400)

    translate_code = src_for_url + dst_for_url

    url = 'https://translate.weblio.jp/?lp=' + translate_code + '&lpf=' + translate_code + '&originalText=' + urllib.parse.quote(text)
    req = urllib.request.Request(url=url)
    res = urllib.request.urlopen(req)

    weblio = Weblio(dst)
    weblio.feed(res.read().decode('utf-8'))
    weblio.close()

    return json.dumps(weblio.results, ensure_ascii=False)


if __name__ == '__main__':
    app.debug = True
    app.run()
