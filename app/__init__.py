from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

app = Flask(__name__)
app.config.from_object(Config)
conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode="require")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models
