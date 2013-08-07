from __future__ import unicode_literals

import os

from flask import Flask, render_template, send_from_directory, request


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


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
def md_qunit():
    return render_template('qunit.html')


@app.route('/favicon.ico')
def md_favicon():
    return send_from_directory(PROJECT_ROOT, 'favicon.ico')


@app.route('/jquery.pjaxr.js')
def md_pjaxr():
    return send_from_directory(os.path.join(PROJECT_ROOT, '..'), 'jquery.pjaxr.js')


@app.route('/<path:filename>/')
def md_template(filename):
    return pjax('{filename}.html'.format(filename=filename))


@app.route('/libs/<path:filename>')
def md_lib(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'libs'), filename)


@app.route('/qunit/<path:filename>')
def md_test(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'qunit'), filename)


if __name__ == '__main__':
    app.run()
