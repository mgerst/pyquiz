from flask import Blueprint, render_template, flash, request, redirect, url_for


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')
