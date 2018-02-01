from flask import Flask
app = Flask(__name__)
app.secret_key = '2435#$5@#45#$5345'
from flaskgames import views
