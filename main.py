from flask import Flask, redirect, request, make_response
from humanfriendly import parse_size, format_size, format_timespan, InvalidSize
from re import match, search, I, X

app = Flask(__name__)

def parse_speed(speed):
    try:
        unit = search(r"[0-9](.+?)(/|p)s", speed, I|X).group(1)
    except AttributeError:
        raise InvalidSize()
    try:
        speed = search(r"([0-9]+?)", speed, I|X).group(1)
    except AttributeError:
        raise InvalidSize()
    if match(r".*bit", unit):
        speed = float(speed) * 0.125
    return parse_size(str(speed) + unit)

def parse_transfer(speed, size):
    return size / speed

@app.before_request
def api_redir():
    if not match(r"^(/.+/.+|/)$", request.path):
        return redirect("/")

@app.route("/")
def api_help():
    HELP = """
TIMETODL HELP
=============

simple api to calculate data transfer times

$ curl timetodl.boniface.tech\t# this help text

/<speed>/<size> # return time to transfer file of <size> at <speed>
/10mbps/100mb => 10 seconds
/57kbps/123 gigbytes => 3 weeks, 3 days and 23 hours
/2mbitps/2mb => 8 seconds
/5mbit/s/3gb => 1 hour and 20 minutes

add `bit` to the unit of <speed> if necessary (e.g. mbit for megabits)
-bit units are usually used to measure internet speeds,
other units are usually for file transfers.
"""
    resp = make_response(HELP[1:])
    resp.headers['Content-Type'] = 'text/plain'
    return resp

@app.route("/<path:speed>/<size>")
def api_main(speed, size):
    try:
        raw_size = parse_size(size) # bytes
    except InvalidSize:
        return make_response(f"Invalid size: {size}", 400)
    try:
        raw_speed = parse_speed(speed) # bytes per second
    except InvalidSize:
        return make_response(f"Invalid speed: {speed}", 400)
    raw_time = parse_transfer(raw_speed, raw_size) # seconds
    return f"Transferring {format_size(raw_size)} at {format_size(raw_speed)}/s => {format_timespan(raw_time)}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8585)
