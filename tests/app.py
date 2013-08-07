from __future__ import unicode_literals

from flask import Flask, render_template, send_from_directory
from werkzeug.routing import BaseConverter


app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


@app.route('/')
def qunit():
    return render_template('views/qunit.html')


@app.route('/jquery.pjaxr.js')
def pjaxr():
    return send_from_directory('../', 'jquery.pjaxr.js')


@app.route('/<regex("[\w]+\.html"):view>/')
def view(view):
    return render_template('views/{view}'.format(view=view))


@app.route('/<regex("/libs/[\w]+\.[js|css]"):lib>/')
def lib(lib):
    return send_from_directory('libs/', lib)


@app.route('/<regex("/qunit/[\w]+\.js"):test>/')
def test(test):
    return send_from_directory('qunit/', test)


if __name__ == '__main__':
    app.run()
