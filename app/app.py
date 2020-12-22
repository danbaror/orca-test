from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AccessEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(64))
    xff = db.Column(db.String(64))
    user_agent = db.Column(db.String(1024))
    access_time = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.String(1024))


db.drop_all()
db.create_all()

@app.errorhandler(404)
def index(_):
    remote_addr = request.remote_addr
    xff = request.headers.get("X-Forwarded-For", "")
    user_agent = request.headers.get("User-Agent", "")
    path = request.path

    entry = AccessEntry(ip=remote_addr, xff=xff, user_agent=user_agent, path=path)
    db.session.add(entry)
    db.session.commit()

    entries = AccessEntry.query.order_by(AccessEntry.access_time.desc()).limit(10)
    ret = [
        {
            "ip": entry.ip,
            "xff": entry.xff,
            "user_agent": entry.user_agent,
            "path": entry.path,
            "time": entry.access_time.isoformat(),
        }
        for entry in entries
    ]

    return json.dumps(ret)


@app.route("/_healthz")
def health():
    return json.dumps({"status": "HEALTHY", "count": AccessEntry.query.count()})

@app.route("/_load")
def check_load():

    # Get the load average over the last 1, 5, and 15 minutes
    # using os.getloadavg() method
    load_avg1, load_avg5, load_avg15 = os.getloadavg()
    # host = os.uname()[1]
    # HTML String
    html = """
    <table border=1>
        <tr>
          <th>Load Average 1 min</th>
          <th>Load Average 5 min</th>
          <th>Load Average 15 min</th>
        </tr><tr>
    """
    table_item = "<th>" + str(load_avg1) + "</th><th>" + str(load_avg5) \
               + "</th><th>" + str(load_avg15) + "</th></tr></table>"
    return html + table_item


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
