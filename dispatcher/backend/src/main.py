import os
from flask import Flask

from routes import auth, schedules, users, workers, languages, tags, errors, tasks
from utils.json import Encoder
from prestart import Initializer
from utils.zmq import socket


flask = Flask(__name__)
flask.json_encoder = Encoder

flask.register_blueprint(auth.Blueprint())
flask.register_blueprint(schedules.Blueprint())
flask.register_blueprint(tasks.Blueprint())
flask.register_blueprint(users.Blueprint())
flask.register_blueprint(workers.Blueprint())
flask.register_blueprint(languages.Blueprint())
flask.register_blueprint(tags.Blueprint())

errors.register_handlers(flask)

print(f"started socket at {socket}")


if __name__ == "__main__":
    Initializer.create_initial_user()

    is_debug = os.getenv('DEBUG', False)
    flask.run(host='0.0.0.0', debug=is_debug, port=80, threaded=True)
