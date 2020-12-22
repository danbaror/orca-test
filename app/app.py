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
      
    # Get the load average over 
    # the last 1, 5, and 15 minutes  
    # using os.getloadavg() method 
    load1, load5, load15 = os.getloadavg() 
        
    # Print the load average over 
    # the last 1, 5, and 15 minutes  
    print("Load average over the last 1 minute:", load1) 
    print("Load average over the last 5 minute:", load5) 
    print("Load average over the last 15 minute:", load15) 

    return json.dumps({"Load Avg 1m": "Load Avg 5m", "Load Avg 5m": load1, load5, load15})

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
