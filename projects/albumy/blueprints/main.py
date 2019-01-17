from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload():
    return render_template('main/upload.html')
