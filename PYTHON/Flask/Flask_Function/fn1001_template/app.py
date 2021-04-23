from flask import Flask
from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    from views import main_views
    app.register_blueprint(main_views.bp)


    return app