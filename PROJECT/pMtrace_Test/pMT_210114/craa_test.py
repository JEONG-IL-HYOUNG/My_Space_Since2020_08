from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import gb_account

import config

db = SQLAlchemy()

aa = gb_account.query.order_by().all()

print(aa)