from flask import request, redirect
import json
import os

import tools

DATA_FILE = tools.inst("clicker.json")

def setup_clicker():
    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"clicks":0}, f)

bp = tools.MyBlueprint("clicker", "clicker_app", host="click", setup=setup_clicker)
tools.limiter.limit("500/hour")(bp)

with open(DATA_FILE, "r") as f:
    DATA = json.load(f)

@bp.route("/", methods=["GET", "POST"])
def home():
    global DATA
    if request.method == "POST":
        DATA["clicks"] += 1

        with open(DATA_FILE, "w") as f:
            json.dump(DATA, f, indent=4)

        return redirect(request.url)
        
    return bp.render("clicker.html", clicks=DATA["clicks"])

@bp.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r