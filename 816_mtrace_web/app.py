from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)#, satic_folder='static')
    app.config.from_object(config)

    db.init_app(app)

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    import models
    from views import main_views, auth_views, analysis_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(analysis_views.bp)

    return app


