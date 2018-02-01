#!/usr/bin/env python
from flaskgames import app
application = Flask(__name__)
app.run(host='0.0.0.0', debug=True)
