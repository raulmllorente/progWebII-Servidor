from flask import Blueprint, render_template

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

@module002.route('/')
def module002_index():
    return render_template("module002_index.html")


@module002.route('/test')
def module002_test():
    return 'OK'
