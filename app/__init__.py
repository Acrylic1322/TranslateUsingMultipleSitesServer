import sys, json
import urllib, urllib.request
from app.site_parser.weblio import Weblio
from app.site_parser.excite import Excite
from flask import Flask, render_template, send_from_directory, request, abort, make_response

app = Flask(__name__)

@app.route('/')
def hello():
    res = make_response("<h2>Hello, world!</h2>")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/excite/<src>/<dst>/', methods=['GET'])
def excite(src, dst):
    codeset = {
        "en": "EN",
        "jp": "JA"
    }

    foreign_language_set = {
        "en": 'english'
    }

    if src == dst:
        abort(400)
    elif not src in codeset or not dst in codeset:
        abort(501)

    text = request.args.get('text')
    if text is None:
        return ""

    foreign_language_for_url = ''

    src_for_url = ''
    if src in codeset:
        src_for_url = codeset[src]

        if dst != 'jp':
            foreign_language_for_url = foreign_language_set[dst]

    dst_for_url = ''
    if dst in codeset:
        dst_for_url = codeset[dst]

        if dst != 'jp':
            foreign_language_for_url = foreign_language_set[dst]

    translate_code = src_for_url + dst_for_url

    url = 'https://translate.weblio.jp/?lp=' + translate_code + '&lpf=' + translate_code + '&originalText=' + urllib.parse.quote(text)
    url = 'http://www.excite.co.jp/world/' + foreign_language_for_url + '/?before=' + urllib.parse.quote(text) + '&wb_lp=' + translate_code
    req = urllib.request.Request(url=url)
    res = urllib.request.urlopen(req)

    excite = Excite()
    excite.feed(res.read().decode('utf-8'))
    excite.close()

    res = make_response(json.dumps(excite.results, ensure_ascii=False))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/weblio/<src>/<dst>/', methods=['GET'])
def weblio(src, dst):
    codeset = {
        "en": "E",
        "jp": "J"
    }

    if src == dst:
        abort(400)
    elif not src in codeset or not dst in codeset:
        abort(501)

    text = request.args.get('text')
    if text is None:
        return ""

    src_for_url = ''
    if src in codeset:
        src_for_url = codeset[src]

    dst_for_url = ''
    if dst in codeset:
        dst_for_url = codeset[dst]

    translate_code = src_for_url + dst_for_url

    url = 'https://translate.weblio.jp/?lp=' + translate_code + '&lpf=' + translate_code + '&originalText=' + urllib.parse.quote(text)
    req = urllib.request.Request(url=url)
    res = urllib.request.urlopen(req)

    weblio = Weblio(dst)
    weblio.feed(res.read().decode('utf-8'))
    weblio.close()

    res = make_response(json.dumps(weblio.results, ensure_ascii=False))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

if __name__ == '__main__':
    app.debug = True
    app.run()
