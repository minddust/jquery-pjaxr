from __future__ import unicode_literals

from flask import Flask, render_template, send_from_directory, request
from werkzeug.routing import BaseConverter


app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# thanks @zachwill - https://github.com/zachwill/pjax_flask/blob/master/app.py
def pjax(template):
    if 'X-PJAX' in request.headers:
        return render_template(_pjaxify_template_var(template))
    return render_template(template)


# thanks @jacobian - https://github.com/jacobian/django-pjax/blob/master/djpjax.py
def _pjaxify_template_var(template_var):
    if isinstance(template_var, (list, tuple)):
        template_var = type(template_var)(_pjaxify_template_name(name) for name in template_var)
    elif isinstance(template_var, basestring):
        template_var = _pjaxify_template_name(template_var)
    return template_var


def _pjaxify_template_name(name):
    if '.' in name:
        name = '%s-pjax.%s' % tuple(name.rsplit('.', 1))
    else:
        name += '-pjax'
    return name


@app.route('/')
def qunit():
    return render_template('views/qunit.html')


@app.route('/jquery.pjaxr.js')
def pjaxr():
    return send_from_directory('../', 'jquery.pjaxr.js')


@app.route('/<regex("[\w]+\.html"):view>/')
def view(view):
    return pjax('views/{view}'.format(view=view))


@app.route('/<regex("/libs/[\w]+\.[js|css]"):lib>/')
def lib(lib):
    return send_from_directory('libs/', lib)


@app.route('/<regex("/qunit/[\w]+\.js"):test>/')
def test(test):
    return send_from_directory('qunit/', test)


if __name__ == '__main__':
    app.run()
